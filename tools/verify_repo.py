"""Repository verification: hygiene, consistency and automated tests. Exit code 1 if a check fails."""
import argparse
import csv
import re
import subprocess
import sys
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PY = ROOT / "05_iiot_data" / "python"
EVIDENCE = ROOT / "06_tests" / "evidence" / "final"
EM_DASH = "\u2014"
SELF = {"tools/verify_repo.py", "tools/campaign.py", "tools/impact.py"}
TEXT_SUFFIXES = {".md", ".csv", ".scl", ".py", ".txt", ".json"}
TEXT_NAMES = {".gitignore", ".gitattributes", ".editorconfig", "LICENSE"}
EXEMPT_TESTS = {"T66", "T67"}
EXEMPT_REQUIREMENTS = {"REQ-055"}
REQUIRED = ["README.md", "README.fr.md", "LICENSE", "CHANGELOG.md", "CONTRIBUTING.md", ".gitignore",
            "docs/decision_log.md", "docs/glossary.md", "docs/roadmap.md", "docs/runbook.md",
            "01_requirements/requirements.md", "06_tests/test_plan.md", "06_tests/test_results.md",
            "06_tests/defect_log.md", "04_hmi/operator_guide.md", "02_design/io_list.csv",
            "02_design/alarm_matrix.csv", "05_iiot_data/data_dictionary.md"]

PLACEHOLDERS = re.compile(r"TO FILL|TO VERIFY|\(fill in|\(write |\(describe |\(value\)|\(explain |"
                          r"\(For each deviation|Completed after|\bN of \d\b|: N[,)]|\bN samples\b")
INTERNAL_IDS = re.compile(r"\b(REQ|DEC|ASM|UC|ALM|WRN|ANO)[-_]\d+|\bMission\b|\bIteration\b|\bP\d\d\b|"
                          r"\bT\d\d\b|\b\b|\b\b")
RAW_ADDRESS = re.compile(r"%[IQM]\d|%IW|%QW")
SECRET = re.compile(r"(password|secret|token|api[_-]?key)\s*[:=]\s*\S+", re.IGNORECASE)
FORBIDDEN = re.compile(r"\.(env|pem|key|pfx|der|crt|cer|p12)$", re.IGNORECASE)
LINK = re.compile(r"!?\[[^\]]*\]\(([^)\s]+)\)")


def read(path):
    return path.read_text(encoding="utf-8-sig", errors="replace")


def rel(path):
    return path.relative_to(ROOT).as_posix()


def csv_rows(path):
    with path.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


@lru_cache(maxsize=1)
def tracked():
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True, text=True, check=True).stdout
    return [ROOT / line for line in out.splitlines() if line]


def text_files():
    return [p for p in tracked() if p.suffix in TEXT_SUFFIXES or p.name in TEXT_NAMES]


def scan(pattern, files):
    found = []
    for p in files:
        if rel(p) in SELF:
            continue
        for n, line in enumerate(read(p).splitlines(), 1):
            if pattern.search(line):
                found.append(f"{rel(p)}:{n}")
    return found


def check_em_dash():
    bad = [rel(p) for p in text_files() if EM_DASH in read(p)]
    return not bad, ", ".join(bad) or "none"


def check_placeholders():
    found = scan(PLACEHOLDERS, text_files())
    return not found, "; ".join(found[:15]) or "none"


def check_code_conventions():
    found = []
    for p in sorted((ROOT / "03_plc" / "src").glob("*.scl")):
        for n, line in enumerate(read(p).splitlines(), 1):
            if RAW_ADDRESS.search(line) or INTERNAL_IDS.search(line):
                found.append(f"{p.name}:{n}")
    return not found, "; ".join(found[:15]) or "no raw address, no internal identifier"


def check_csv_schemas():
    problems = []
    for name, width in (("02_design/io_list.csv", 10), ("02_design/alarm_matrix.csv", 10),
                        ("01_requirements/requirements_traceability_matrix.csv", 6)):
        with (ROOT / name).open(newline="", encoding="utf-8-sig") as f:
            bad = [i for i, r in enumerate(csv.reader(f), 1) if len(r) != width]
        if bad:
            problems.append(f"{name}: wrong field count on lines {bad[:5]}")
    io = csv_rows(ROOT / "02_design" / "io_list.csv")
    if len(io) != 24:
        problems.append(f"io_list has {len(io)} signals, expected 24")
    tags = [r["Tag"] for r in io]
    if len(tags) != len(set(tags)):
        problems.append("duplicate tag in io_list")
    return not problems, "; ".join(problems) or "io list has 24 signals, field counts consistent"


def check_alarm_matrix():
    rows = csv_rows(ROOT / "02_design" / "alarm_matrix.csv")
    need = ["Probable_Causes", "System_Reaction", "HMI_Text", "Reset", "Operator_Action"]
    bad = [r["ID"] for r in rows if any(not r[k].strip() for k in need)]
    return not bad and len(rows) >= 12, f"{len(rows)} alarms, incomplete: {', '.join(bad) or 'none'}"


def check_traceability():
    reqs = set(re.findall(r"^\| (REQ-\d{3}) \|", read(ROOT / "01_requirements" / "requirements.md"), re.M))
    plan = set(re.findall(r"^\| (T\d\d) \|", read(ROOT / "06_tests" / "test_plan.md"), re.M))
    rows = csv_rows(ROOT / "01_requirements" / "requirements_traceability_matrix.csv")
    matrix = {r["Req_ID"] for r in rows}
    used = {t for r in rows for t in r["Test_IDs"].split(";") if t}
    problems = []
    for label, items in (("requirements missing from the matrix", reqs - matrix),
                         ("matrix rows without a requirement", matrix - reqs),
                         ("requirements without a test", {r["Req_ID"] for r in rows if not r["Test_IDs"].strip()}),
                         ("tests missing from the matrix", plan - used),
                         ("matrix tests missing from the plan", used - plan)):
        if items:
            problems.append(f"{label}: {', '.join(sorted(items))}")
    return not problems, "; ".join(problems) or f"{len(reqs)} requirements, {len(plan)} tests, both directions covered"


def check_decision_log():
    nums = [int(i[4:]) for i in re.findall(r"^\| (DEC-\d{3}) \|", read(ROOT / "docs" / "decision_log.md"), re.M)]
    dup = sorted({n for n in nums if nums.count(n) > 1})
    gaps = sorted(set(range(1, max(nums) + 1)) - set(nums)) if nums else []
    return bool(nums) and not dup and not gaps, f"{len(nums)} decisions, duplicates {dup or 'none'}, gaps {gaps or 'none'}"


def check_secrets():
    found = scan(SECRET, text_files()) + [rel(p) for p in tracked() if FORBIDDEN.search(p.name)]
    return not found, "; ".join(found[:15]) or "none"


def check_links():
    missing = []
    for p in text_files():
        if p.suffix != ".md":
            continue
        for n, line in enumerate(read(p).splitlines(), 1):
            for target in LINK.findall(line):
                if re.match(r"^(https?:|mailto:|#)", target):
                    continue
                path = target.split("#")[0]
                if path and not (p.parent / path).exists():
                    missing.append(f"{rel(p)}:{n} -> {target}")
    return not missing, "; ".join(missing[:10]) or "all local links resolve"


def check_required_files():
    missing = [f for f in REQUIRED if not (ROOT / f).exists()]
    return not missing, ", ".join(missing) or "all present"


def check_changelog_tags():
    tags = subprocess.run(["git", "tag", "--list", "v*"], cwd=ROOT, capture_output=True, text=True).stdout.split()
    log = read(ROOT / "CHANGELOG.md")
    missing = [t for t in tags if f"## [{t[1:]}]" not in log]
    return not missing, f"{len(tags)} tags, changelog sections missing: {missing or 'none'}"


def run_unittest(module):
    r = subprocess.run([sys.executable, "-m", "unittest", module], cwd=PY, capture_output=True, text=True)
    lines = r.stderr.strip().splitlines()
    return r.returncode == 0, f"{module}: {lines[-1] if lines else 'no output'}"


def check_datasets():
    pattern = str(ROOT / "05_iiot_data" / "datasets" / "D0*.csv")
    r = subprocess.run([sys.executable, "validate_dataset.py", pattern], cwd=PY, capture_output=True, text=True)
    return r.returncode == 0, " | ".join(l.strip() for l in r.stdout.splitlines())[:300]


def check_kpi_summary():
    rows = csv_rows(ROOT / "05_iiot_data" / "kpi_summary.csv")
    ok = len(rows) == 6 and all(r["station_availability_pct"] for r in rows)
    return ok, f"{len(rows)} datasets summarized"


def check_anomaly_quiet():
    bad = [r["Rule"] for r in csv_rows(ROOT / "05_iiot_data" / "anomaly_eval.csv")
           if r["Dataset"] == "D01_normal" and r["Status"] != "ok"]
    return not bad, f"flags on the normal dataset: {bad or 'none'}"


def check_explanations():
    rows = csv_rows(ROOT / "05_iiot_data" / "anomaly_flags.csv")
    empty = [r for r in rows if not r["Explanation"].strip()]
    return bool(rows) and not empty, f"{len(rows)} flagged periods, {len(empty)} without an explanation"


def check_defects_closed():
    open_ = re.findall(r"^\|\s*(BUG-\d+)\s*\|.*\|\s*Open\s*\|\s*$", read(ROOT / "06_tests" / "defect_log.md"), re.M)
    return not open_, f"open defects: {open_ or 'none'}"


def check_requirements_verified():
    rows = csv_rows(ROOT / "01_requirements" / "requirements_traceability_matrix.csv")
    left = [r["Req_ID"] for r in rows if r["Status"].strip() != "Verified" and r["Req_ID"] not in EXEMPT_REQUIREMENTS]
    return not left, f"not verified: {left or 'none'}"


def check_campaign_complete():
    import campaign
    rows = campaign.load_sheet()
    left = [r["ID"] for r in rows if r["ID"] not in EXEMPT_TESTS and r["Result"] != "Pass"]
    return bool(rows) and not left, f"{len(rows)} tests in the sheet, not passed: {left or 'none'}"


CHECKS = [
    ("no_em_dash", [], check_em_dash, False),
    ("no_placeholders", [], check_placeholders, False),
    ("code_conventions", [], check_code_conventions, False),
    ("csv_schemas", [], check_csv_schemas, False),
    ("alarm_matrix", ["T24"], check_alarm_matrix, False),
    ("traceability", ["T32"], check_traceability, False),
    ("decision_log", [], check_decision_log, False),
    ("secrets", ["T29"], check_secrets, False),
    ("links", [], check_links, False),
    ("required_files", [], check_required_files, False),
    ("changelog_tags", [], check_changelog_tags, False),
    ("unit_tests_kpi", ["T25"], lambda: run_unittest("test_kpi"), False),
    ("unit_tests_anomaly", ["T58"], lambda: run_unittest("test_anomaly"), False),
    ("datasets", ["T53"], check_datasets, False),
    ("kpi_summary", ["T56"], check_kpi_summary, False),
    ("anomaly_quiet", ["T59"], check_anomaly_quiet, False),
    ("explanations", ["T60"], check_explanations, False),
    ("defects_closed", [], check_defects_closed, True),
    ("requirements_verified", [], check_requirements_verified, True),
    ("campaign_complete", [], check_campaign_complete, True),
]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--final", action="store_true", help="also check the release gates")
    parser.add_argument("--record", action="store_true", help="record the automated tests in the campaign sheet")
    args = parser.parse_args()
    lines, results, failed = [], {}, False
    for name, tests, fn, final_only in CHECKS:
        if final_only and not args.final:
            continue
        try:
            ok, detail = fn()
        except Exception as exc:
            ok, detail = False, f"{type(exc).__name__}: {exc}"
        tag = f"[{','.join(tests)}] " if tests else ""
        lines.append(f"{'PASS' if ok else 'FAIL'} {tag}{name}: {detail}")
        failed = failed or not ok
        for t in tests:
            results[t] = (ok, f"{name}: {detail}")
    print("\n".join(lines))
    print(f"\n{sum(l.startswith('PASS') for l in lines)} of {len(lines)} checks passed")
    if args.record:
        import campaign
        EVIDENCE.mkdir(parents=True, exist_ok=True)
        (EVIDENCE / "automated_checks.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
        for test_id, (ok, detail) in results.items():
            if ok:
                campaign.record(test_id, "Pass", detail[:120].replace(",", ";"),
                                evidence="evidence/final/automated_checks.txt")
            else:
                print(f"{test_id} not recorded: its check failed")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()