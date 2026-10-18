"""Run the anomaly rules on every dataset, score them and write tables and figures."""
import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

from anomaly_eval import EXPECTED, score, truth
from anomaly_rules import (PARAMS, RULE_FUNCS, RULES, active_pump, current_of, deviation_series, held,
                           periods, rise_rates, run_all, trailing_starts)
from kpi import load_rows

ROOT = Path(__file__).resolve().parents[1]
SWEEP = [("ANO_01", "flow_min"), ("ANO_02", "rise_min_pct_min"), ("ANO_03", "current_high"),
         ("ANO_04", "starts_max"), ("ANO_06", "deviation_pct")]
FACTORS = [0.5, 1.0, 1.5, 2.0]
COLORS = plt.cm.tab10.colors


def status(expected, fired):
    if expected:
        return "TP" if fired else "MISS"
    return "FP" if fired else "ok"


def margins(rows, p):
    settled = held(rows, [active_pump(r) in (1, 2) for r in rows], p["settle_s"])
    flows = [r["Flow_m3h"] for r, ok in zip(rows, settled) if ok]
    amps = [current_of(r) for r in rows if active_pump(r) in (1, 2)]
    rates = [x for x in rise_rates(rows, p) if x is not None]
    starts = trailing_starts(rows, p)
    devs = [x for x in deviation_series(rows, p) if x is not None]
    return [
        ("ANO_01 lowest flow while pumping (m3/h)", min(flows) if flows else None, p["flow_min"]),
        ("ANO_03 highest current while pumping (A)", max(amps) if amps else None, p["current_high"]),
        ("ANO_02 lowest level rise (%/min)", min(rates) if rates else None, p["rise_min_pct_min"]),
        ("ANO_04 most starts in the window", max(starts) if starts else None, p["starts_max"]),
        ("ANO_06 largest excess current (%)", max(devs) if devs else None, p["deviation_pct"]),
    ]


def draw(name, rows, flags):
    t = [r["SimTime_s"] / 60.0 for r in rows]
    dt = (t[-1] - t[0]) / max(len(t) - 1, 1)
    fig, ax = plt.subplots(4, 1, figsize=(11, 9), sharex=True, gridspec_kw={"height_ratios": [3, 2, 1, 2]})
    ax[0].plot(t, [r["TankLevel_pct"] for r in rows], color="#1565c0")
    for y, color in ((30, "#2e7d32"), (80, "#ef6c00"), (95, "#c62828")):
        ax[0].axhline(y, color=color, ls="--", lw=1)
    ax[0].set_ylim(0, 100)
    ax[0].set_ylabel("tank level (%)")
    ax[1].plot(t, [r["Flow_m3h"] for r in rows], color="#1565c0", label="flow (m3/h)")
    ax[1].plot(t, [max(r["P1_Current_A"], r["P2_Current_A"]) for r in rows], color="#ef6c00", ls="--",
               label="motor current (A)")
    ax[1].legend(loc="upper right")
    ax[2].step(t, [0.8 * r["P1_RunFeedback"] for r in rows], where="post", color="#1565c0")
    ax[2].step(t, [1.2 + 0.8 * r["P2_RunFeedback"] for r in rows], where="post", color="#ef6c00")
    ax[2].set_yticks([0.4, 1.6])
    ax[2].set_yticklabels(["pump 1", "pump 2"])
    for k, rule in enumerate(RULES):
        for g in periods(rows, flags[rule]):
            ax[3].broken_barh([(g["t_start_min"], max(g["t_end_min"] - g["t_start_min"], dt))],
                              (k - 0.35, 0.7), color=COLORS[k])
    ax[3].set_yticks(range(len(RULES)))
    ax[3].set_yticklabels(list(RULES))
    ax[3].set_ylim(-0.7, len(RULES) - 0.3)
    ax[3].invert_yaxis()
    ax[3].set_xlabel("simulated time (min)")
    fig.suptitle(f"{name}: signals and flagged periods")
    fig.tight_layout()
    fig.savefig(ROOT / "figures" / f"{name}_anomalies.png", dpi=140)
    plt.close(fig)


def mean(values):
    return sum(values) / len(values) if values else None


def main():
    (ROOT / "figures").mkdir(exist_ok=True)
    data = {p.stem: load_rows(p) for p in sorted((ROOT / "datasets").glob("D0*.csv"))}
    flag_lines, eval_lines, matrix, event_lines = [], [], [], []
    for name, rows in data.items():
        flags = run_all(rows)
        found = truth(rows)
        cells = []
        for rule in RULES:
            n = sum(f is not None for f in flags[rule])
            groups = periods(rows, flags[rule])
            st = status(rule in EXPECTED.get(name, set()), n > 0)
            cells.append(f"{st} ({n})")
            for g in groups:
                flag_lines.append([name, rule, round(g["t_start_min"], 1), round(g["t_end_min"], 1),
                                   g["samples"], g["message"]])
            line = [name, rule, st, n, len(groups), "", "", "", "", ""]
            if rule in found:
                s = score(rows, flags[rule], found[rule])
                d_samples = mean([d[0] for d in s["delays"]])
                d_minutes = mean([d[1] for d in s["delays"]])
                line[5:] = [s["events"], s["detected"],
                            "" if d_samples is None else round(d_samples, 1),
                            "" if d_minutes is None else round(d_minutes, 1), s["false_periods"]]
                if s["events"] or s["false_periods"]:
                    delay = "n/a" if d_samples is None else f"{d_samples:.0f} samples ({d_minutes:.0f} min)"
                    event_lines.append(f"| {name} | {rule} | {s['events']} | {s['detected']} | {delay} | {s['false_periods']} |")
            eval_lines.append(line)
        matrix.append((name, cells))
        draw(name, rows, flags)

    with (ROOT / "anomaly_flags.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Dataset", "Rule", "StartSimMin", "EndSimMin", "Samples", "Explanation"])
        w.writerows(flag_lines)
    with (ROOT / "anomaly_eval.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Dataset", "Rule", "Status", "FlaggedSamples", "FlaggedPeriods", "TruthEvents",
                    "DetectedEvents", "MeanDelaySamples", "MeanDelaySimMin", "FalsePeriods"])
        w.writerows(eval_lines)

    md = ["# Anomaly Results", "", "Generated by `python/anomaly_report.py`. Figures are in `figures/`.", "",
          "## Rules fired per dataset", "",
          "TP: expected and fired. MISS: expected, not fired. FP: fired, not expected. ok: neither. "
          "The number is the count of flagged samples. A secondary symptom is listed as expected.", "",
          "| Dataset | " + " | ".join(RULES) + " |", "| --- |" + " --- |" * len(RULES)]
    md += [f"| {name} | " + " | ".join(cells) + " |" for name, cells in matrix]
    md += ["", "## Detection against the injected faults", "",
           "| Dataset | Rule | Fault events | Detected | Mean detection delay | False periods |",
           "| --- | --- | --- | --- | --- | --- |"] + event_lines
    if "D01_normal" in data:
        md += ["", "## Threshold margins on the normal dataset", "",
               "| Check | Extreme on normal data | Threshold |", "| --- | --- | --- |"]
        for label, value, threshold in margins(data["D01_normal"], PARAMS):
            md.append(f"| {label} | {'n/a' if value is None else round(value, 2)} | {threshold} |")
    md += ["", "## Sensitivity to the thresholds", "",
           "Datasets where the rule fires when its threshold is multiplied by the factor.", "",
           "| Rule | Parameter | x0.5 | x1.0 | x1.5 | x2.0 |", "| --- | --- | --- | --- | --- | --- |"]
    for rule, key in SWEEP:
        cells = []
        for factor in FACTORS:
            p = dict(PARAMS)
            p[key] = max(1, round(PARAMS[key] * factor)) if key == "starts_max" else PARAMS[key] * factor
            fired = [n[:3] for n, rows in data.items() if any(x is not None for x in RULE_FUNCS[rule](rows, p))]
            cells.append(", ".join(fired) if fired else "none")
        md.append(f"| {rule} | {key} | " + " | ".join(cells) + " |")
    (ROOT / "anomaly_results.md").write_text("\n".join(md) + "\n", encoding="utf-8")

    print(f"{'dataset':24}" + "".join(f"{r:>12}" for r in RULES))
    for name, cells in matrix:
        print(f"{name:24}" + "".join(f"{c:>12}" for c in cells))
    print("written: anomaly_results.md, anomaly_eval.csv, anomaly_flags.csv, figures/")


if __name__ == "__main__":
    main()