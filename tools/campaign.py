"""Final test campaign: initialize the sheet from the test plan, show the next test, record results, show status."""
import argparse
import csv
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "06_tests" / "test_plan.md"
SHEET = ROOT / "06_tests" / "campaign_final.csv"
SUMMARY = ROOT / "06_tests" / "campaign_summary.md"
MATRIX = ROOT / "01_requirements" / "requirements_traceability_matrix.csv"
EVIDENCE_DIR = ROOT / "06_tests" / "evidence" / "final"
FIELDS = ["ID", "Group", "Level", "Test", "Result", "Date", "Observed", "Evidence", "Defect"]


def span(a, b):
    return [f"T{n:02d}" for n in range(a, b + 1)]


GROUPS = {
    "plc": span(1, 9) + span(11, 22) + ["T27"] + span(33, 40) + ["T54"],
    "hmi": ["T23", "T30"] + span(41, 50) + ["T68", "T69"],
    "data": ["T10", "T29", "T51", "T52", "T53", "T55", "T57"],
    "analytics": ["T25", "T26", "T56", "T58", "T59", "T60"],
    "process": ["T24", "T28", "T31", "T32", "T66", "T67"],
    "acceptance": span(61, 65),
}
LEVEL1 = {"T04", "T05", "T06", "T07", "T08", "T09", "T15", "T22", "T35", "T37", "T23", "T43", "T46",
          "T47", "T48", "T10", "T28"} | set(span(61, 67)) | {"T68", "T69"}
LEVEL3 = {"T24", "T25", "T29", "T32", "T53", "T56", "T58", "T59", "T60"}
LEVEL_TEXT = {
    1: "level 1: save a capture or video named Txx_*.png or .mp4 in 06_tests/evidence/final",
    2: "level 2: replay and record the observed values",
    3: "level 3: automatic, run tools/verify_repo.py --record",
}
NOTES = {t: "Procedure: 06_tests/acceptance_scenarios.md" for t in span(61, 65)}
NOTES.update({"T28": "Procedure: docs/runbook.md, section Cold start",
              "T66": "Procedure: docs/runbook.md, section Reproducibility checks",
              "T67": "Procedure: docs/runbook.md, section Reproducibility checks"})


def group_of(test_id):
    return next((g for g, ids in GROUPS.items() if test_id in ids), "other")


def level_of(test_id):
    return 1 if test_id in LEVEL1 else 3 if test_id in LEVEL3 else 2


def read_plan():
    tests = {}
    for line in PLAN.read_text(encoding="utf-8-sig").splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 7 and re.fullmatch(r"T\d\d", cells[0]):
            tests[cells[0]] = {"name": cells[1], "req": cells[2], "setup": cells[4], "expected": cells[5]}
    return tests


def load_sheet():
    if not SHEET.exists():
        return []
    with SHEET.open(newline="", encoding="utf-8-sig") as f:
        return list(csv.DictReader(f))


def save_sheet(rows):
    with SHEET.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def init():
    rows = load_sheet()
    known = {r["ID"] for r in rows}
    for test_id, info in read_plan().items():
        if test_id not in known:
            rows.append({"ID": test_id, "Group": group_of(test_id), "Level": level_of(test_id),
                         "Test": info["name"], "Result": "", "Date": "", "Observed": "",
                         "Evidence": "", "Defect": ""})
    rows.sort(key=lambda r: r["ID"])
    save_sheet(rows)
    print(f"{len(rows)} tests in {SHEET.name}")


def show_next(group):
    plan = read_plan()
    rows = [r for r in load_sheet() if not group or r["Group"] == group]
    pending = [r for r in rows if not r["Result"]]
    if not pending:
        print("nothing pending" + (f" in group {group}" if group else ""))
        return
    r = pending[0]
    info = plan.get(r["ID"], {})
    print(f"{r['ID']}  {r['Test']}  (group {r['Group']}, {len(pending)} pending)")
    print(f"  Requirements:     {info.get('req', '')}")
    print(f"  Setup and action: {info.get('setup', '')}")
    print(f"  Expected:         {info.get('expected', '')}")
    print(f"  Evidence:         {LEVEL_TEXT[int(r['Level'])]}")
    if r["ID"] in NOTES:
        print(f"  {NOTES[r['ID']]}")
    print("  Field signals: while Sim_Inputs is TRUE use the V_ bits of DB_Sim instead of the physical inputs.")


def record(test_id, result, observed="", evidence="", defect=""):
    rows = load_sheet()
    row = next((r for r in rows if r["ID"] == test_id), None)
    if row is None:
        sys.exit(f"{test_id} is not in the sheet: add it to the test plan, then run init")
    files = sorted(f.name for f in EVIDENCE_DIR.glob(f"{test_id}_*")) if EVIDENCE_DIR.exists() else []
    if result == "Fail" and not defect:
        sys.exit("a failed test needs --defect with the defect ID")
    if result == "Pass" and int(row["Level"]) == 1 and not files and not evidence:
        sys.exit(f"{test_id} is level 1: save a file named {test_id}_*.png in 06_tests/evidence/final first")
    row.update(Result=result, Date=date.today().isoformat(), Observed=observed,
               Evidence=evidence or "; ".join(files), Defect=defect)
    save_sheet(rows)
    print(f"{test_id}: {result}")


def status(write):
    rows = load_sheet()
    lines = ["# Campaign Summary", "", "Generated by `tools/campaign.py status --write`.", "",
             "| Group | Tests | Passed | Failed | Pending |", "| --- | --- | --- | --- | --- |"]
    total = [0, 0, 0, 0]
    for group in list(GROUPS) + ["other"]:
        g = [r for r in rows if r["Group"] == group]
        if not g:
            continue
        counts = [len(g), sum(r["Result"] == "Pass" for r in g), sum(r["Result"] == "Fail" for r in g),
                  sum(not r["Result"] for r in g)]
        total = [a + b for a, b in zip(total, counts)]
        lines.append(f"| {group} | " + " | ".join(map(str, counts)) + " |")
    lines.append("| all | " + " | ".join(map(str, total)) + " |")
    failed = [f"{r['ID']} ({r['Defect']})" for r in rows if r["Result"] == "Fail"]
    warnings = []
    for r in rows:
        if r["Result"] == "Pass" and int(r["Level"]) == 1:
            if not (EVIDENCE_DIR.exists() and list(EVIDENCE_DIR.glob(f"{r['ID']}_*"))):
                warnings.append(f"{r['ID']}: level 1 test without an evidence file")
    lines += ["", "Failed tests: " + (", ".join(failed) or "none"),
              "", "Warnings: " + ("; ".join(warnings) or "none")]
    text = "\n".join(lines) + "\n"
    print(text)
    if write:
        SUMMARY.write_text(text, encoding="utf-8")


def update_matrix():
    results = {r["ID"]: r["Result"] for r in load_sheet()}
    with MATRIX.open(newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        fields = reader.fieldnames
        rows = list(reader)
    for r in rows:
        tests = [t for t in r["Test_IDs"].split(";") if t]
        if tests and all(results.get(t) == "Pass" for t in tests):
            r["Status"] = "Verified"
        elif any(results.get(t) == "Fail" for t in tests):
            r["Status"] = "Failed"
    with MATRIX.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    print(f"{sum(r['Status'] == 'Verified' for r in rows)} of {len(rows)} requirements verified")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)
    sub.add_parser("init")
    nxt = sub.add_parser("next")
    nxt.add_argument("--group", choices=list(GROUPS))
    rec = sub.add_parser("record")
    rec.add_argument("id")
    rec.add_argument("result", type=str.capitalize, choices=["Pass", "Fail"])
    rec.add_argument("observed", nargs="?", default="")
    rec.add_argument("--evidence", default="")
    rec.add_argument("--defect", default="")
    stat = sub.add_parser("status")
    stat.add_argument("--write", action="store_true")
    sub.add_parser("matrix")
    args = parser.parse_args()
    if args.cmd == "init":
        init()
    elif args.cmd == "next":
        show_next(args.group)
    elif args.cmd == "record":
        record(args.id, args.result, args.observed, args.evidence, args.defect)
    elif args.cmd == "status":
        status(args.write)
    else:
        update_matrix()


if __name__ == "__main__":
    main()