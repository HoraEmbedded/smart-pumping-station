"""Score the anomaly rules against the injected faults and the scenario table."""
from anomaly_rules import active_pump, periods

TOLERANCE = 3
NOMINAL_PUMP_FLOW = 12.0

EXPECTED = {
    "D01_normal": set(),
    "D02_low_flow_p1": set(),       # ANO_01, ANO_02 cannot fire: injection bypasses the recorded Flow_m3h
    "D03_pump_deviation_p1": {"ANO_06"},
    "D04_blocked_line_p1": set(),   # ANO_01, ANO_03 cannot fire: same limitation as D02
    "D05_leak": {"ANO_02"},
    "D06_frequent_starts": {"ANO_04"},
}


def truth(rows):
    """Per sample truth of the rules that have an injection column, from the ground truth columns."""
    out = {"ANO_01": [], "ANO_02": [], "ANO_03": [], "ANO_06": []}
    for r in rows:
        low = [r[f"GT_Inject_P{k}_LowFlow"] >= 0.5 and r[f"P{k}_RunFeedback"] >= 0.5 for k in (1, 2)]
        high = [r[f"GT_Inject_P{k}_HighCurrent"] >= 0.5 and r[f"P{k}_RunFeedback"] >= 0.5 for k in (1, 2)]
        out["ANO_01"].append(any(low))
        out["ANO_03"].append(any(a and b for a, b in zip(low, high)))
        out["ANO_06"].append(any(high))
        out["ANO_02"].append(active_pump(r) != 0 and (any(low) or r["GT_Drain_m3h"] >= NOMINAL_PUMP_FLOW))
    return out


def events(flags):
    out, start = [], None
    for i, value in enumerate(flags):
        if value and start is None:
            start = i
        if not value and start is not None:
            out.append((start, i - 1))
            start = None
    if start is not None:
        out.append((start, len(flags) - 1))
    return out


def score(rows, flags, truth_flags):
    found = events(truth_flags)
    groups = periods(rows, flags)
    detected, delays = 0, []
    for a, b in found:
        hits = [i for i in range(a, min(b + TOLERANCE, len(rows) - 1) + 1) if flags[i] is not None]
        if hits:
            detected += 1
            delays.append((hits[0] - a, (rows[hits[0]]["SimTime_s"] - rows[a]["SimTime_s"]) / 60.0))
    false = sum(1 for g in groups
                if not any(a - TOLERANCE <= g["end"] and g["start"] <= b + TOLERANCE for a, b in found))
    return {"events": len(found), "detected": detected, "delays": delays,
            "periods": len(groups), "false_periods": false}