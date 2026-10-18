"""Explainable anomaly rules for the pumping station datasets.

The rules read measured signals only, never the ground truth columns. Delays are counted on
the sample counter (real seconds), windows and rates on the simulated clock.
"""
from bisect import bisect_right
from statistics import median

PARAMS = {
    "flow_min": 2.0,
    "symptom_delay_s": 5,
    "current_high": 12.0,
    "state_delay_s": 2,
    "settle_s": 2,
    "idle_current_a": 1.0,
    "rise_window_s": 300.0,
    "rise_min_pct_min": 0.5,
    "starts_max": 3,
    "starts_window_s": 3600.0,
    "deviation_pct": 15.0,
    "comparable_pct": 10.0,
    "reference_samples": 5,
}

RANGES = {
    "TankLevel_pct": (0.0, 100.0),
    "SourceLevel_pct": (0.0, 100.0),
    "Flow_m3h": (0.0, 20.5),
    "Pressure_bar": (0.0, 10.0),
    "P1_Current_A": (0.0, 20.0),
    "P2_Current_A": (0.0, 20.0),
}

RULES = {
    "ANO_01": "Pump running with low flow",
    "ANO_02": "Pump running, tank level not rising",
    "ANO_03": "High motor current with low flow",
    "ANO_04": "Too frequent pump starts",
    "ANO_05": "Sensor value out of range or inconsistent",
    "ANO_06": "Abnormal difference between pump 1 and pump 2",
}

LABEL = {1: "pump 1", 2: "pump 2", 3: "both pumps"}


def active_pump(r):
    """1 or 2 when one pump confirms running, 3 when both do, 0 when none."""
    return int(r["P1_RunFeedback"] >= 0.5) + 2 * int(r["P2_RunFeedback"] >= 0.5)


def current_of(r):
    pump = active_pump(r)
    if pump == 1:
        return r["P1_Current_A"]
    if pump == 2:
        return r["P2_Current_A"]
    return max(r["P1_Current_A"], r["P2_Current_A"])


def held(rows, flags, delay):
    """True where the condition has held for at least `delay` counter seconds."""
    out, since = [], None
    for row, flag in zip(rows, flags):
        if flag:
            if since is None:
                since = row["SampleCounter"]
            out.append(row["SampleCounter"] - since >= delay)
        else:
            since = None
            out.append(False)
    return out


def ano_01(rows, p):
    flags = [active_pump(r) != 0 and r["Flow_m3h"] < p["flow_min"] for r in rows]
    out = []
    for r, hit in zip(rows, held(rows, flags, p["symptom_delay_s"])):
        if not hit:
            out.append(None)
            continue
        if current_of(r) > p["current_high"]:
            hint = "motor current high: blockage or friction suspected"
        else:
            hint = "motor current normal: closed valve, dry run or a flow sensor fault are possible"
        out.append(f"{LABEL[active_pump(r)]} running with flow {r['Flow_m3h']:.1f} m3/h, below "
                   f"{p['flow_min']:.1f} for at least {p['symptom_delay_s']} s; {hint}")
    return out


def rise_rates(rows, p):
    """Tank level change in %/min over the trailing window while the same pump ran the whole window."""
    times = [r["SimTime_s"] for r in rows]
    out = [None] * len(rows)
    run_pump, run_start = 0, None
    for i, r in enumerate(rows):
        pump = active_pump(r)
        if pump not in (1, 2):
            run_pump, run_start = 0, None
            continue
        if pump != run_pump:
            run_pump, run_start = pump, r["SimTime_s"]
        if r["SimTime_s"] - run_start < p["rise_window_s"]:
            continue
        j = bisect_right(times, r["SimTime_s"] - p["rise_window_s"]) - 1
        if j < 0 or r["SimTime_s"] - times[j] <= 0:
            continue
        out[i] = (r["TankLevel_pct"] - rows[j]["TankLevel_pct"]) / (r["SimTime_s"] - times[j]) * 60.0
    return out


def ano_02(rows, p):
    out = []
    for r, rate in zip(rows, rise_rates(rows, p)):
        if rate is not None and rate < p["rise_min_pct_min"]:
            out.append(f"{LABEL[active_pump(r)]} running for at least {p['rise_window_s'] / 60:.0f} min but "
                       f"the tank level changed by {rate:+.2f} %/min, expected more than {p['rise_min_pct_min']:.1f}")
        else:
            out.append(None)
    return out


def ano_03(rows, p):
    flags = [active_pump(r) != 0 and current_of(r) > p["current_high"] and r["Flow_m3h"] < p["flow_min"]
             for r in rows]
    out = []
    for r, hit in zip(rows, held(rows, flags, p["symptom_delay_s"])):
        if hit:
            out.append(f"{LABEL[active_pump(r)]} draws {current_of(r):.1f} A, above {p['current_high']:.0f}, "
                       f"with flow {r['Flow_m3h']:.1f} m3/h, below {p['flow_min']:.1f}, for at least "
                       f"{p['symptom_delay_s']} s: blockage or friction suspected")
        else:
            out.append(None)
    return out


def trailing_starts(rows, p):
    """Number of pump starts in the trailing window of simulated time."""
    starts, out, prev = [], [], None
    for r in rows:
        total = r["P1_StartCount"] + r["P2_StartCount"]
        if prev is not None and total > prev:
            starts.extend([r["SimTime_s"]] * int(total - prev))
        prev = total
        limit = r["SimTime_s"] - p["starts_window_s"]
        starts = [t for t in starts if t > limit]
        out.append(len(starts))
    return out


def ano_04(rows, p):
    return [f"{n} pump starts in the last {p['starts_window_s'] / 60:.0f} simulated minutes, "
            f"limit {p['starts_max']}" if n > p["starts_max"] else None
            for n in trailing_starts(rows, p)]


def _range_reason(r):
    for name, (lo, hi) in RANGES.items():
        if not lo <= r[name] <= hi:
            return f"{name} = {r[name]:.2f} outside the physical range {lo:.0f} to {hi:.0f}"
    return None


def _state_reason(r, p):
    if active_pump(r) == 0 and r["Flow_m3h"] >= p["flow_min"]:
        return f"flow {r['Flow_m3h']:.1f} m3/h while no pump confirms running"
    for k in (1, 2):
        if r[f"P{k}_RunFeedback"] < 0.5 and r[f"P{k}_Current_A"] > p["idle_current_a"]:
            return f"pump {k} current {r[f'P{k}_Current_A']:.1f} A while its run feedback is off"
    for k in (1, 2):
        if r[f"P{k}_RunFeedback"] >= 0.5 and r[f"P{k}_RunCmd"] < 0.5:
            return f"pump {k} run feedback on without a run command"
    return None


def ano_05(rows, p):
    ranges = [_range_reason(r) for r in rows]
    states = [_state_reason(r, p) for r in rows]
    range_ok = held(rows, [x is not None for x in ranges], 0)
    state_ok = held(rows, [x is not None for x in states], p["state_delay_s"])
    return [ranges[i] if range_ok[i] else (states[i] if state_ok[i] else None) for i in range(len(rows))]


def deviation_series(rows, p):
    """Excess current of the running pump over the other pump's mean current, in percent."""
    flowing = [r["Flow_m3h"] for r in rows if active_pump(r) in (1, 2) and r["Flow_m3h"] >= p["flow_min"]]
    out = [None] * len(rows)
    if not flowing:
        return out
    ref_flow = median(flowing)
    settled = {k: held(rows, [active_pump(r) == k for r in rows], p["settle_s"]) for k in (1, 2)}
    total, count = {1: 0.0, 2: 0.0}, {1: 0, 2: 0}
    for i, r in enumerate(rows):
        k = active_pump(r)
        if k not in (1, 2) or not settled[k][i]:
            continue
        if abs(r["Flow_m3h"] - ref_flow) > ref_flow * p["comparable_pct"] / 100.0:
            continue
        other = 3 - k
        if count[other] >= p["reference_samples"]:
            reference = total[other] / count[other]
            if reference > 0:
                out[i] = (r[f"P{k}_Current_A"] / reference - 1.0) * 100.0
        total[k] += r[f"P{k}_Current_A"]
        count[k] += 1
    return out


def ano_06(rows, p):
    out = []
    for r, dev in zip(rows, deviation_series(rows, p)):
        if dev is not None and dev > p["deviation_pct"]:
            k = active_pump(r)
            current = r[f"P{k}_Current_A"]
            reference = current / (1.0 + dev / 100.0)
            out.append(f"pump {k} draws {current:.1f} A, {dev:.0f} percent more than pump {3 - k} "
                       f"({reference:.1f} A) at comparable flow ({r['Flow_m3h']:.1f} m3/h); "
                       "the rule cannot tell which of the two deviates")
        else:
            out.append(None)
    return out


RULE_FUNCS = {"ANO_01": ano_01, "ANO_02": ano_02, "ANO_03": ano_03,
              "ANO_04": ano_04, "ANO_05": ano_05, "ANO_06": ano_06}


def run_all(rows, p=None):
    p = p or PARAMS
    return {rule: fn(rows, p) for rule, fn in RULE_FUNCS.items()}


def periods(rows, flags, gap=2):
    """Group flagged samples into periods, a period ends after more than `gap` unflagged samples."""
    out, start, last = [], None, None

    def close(a, b):
        out.append({"start": a, "end": b, "samples": sum(f is not None for f in flags[a:b + 1]),
                    "t_start_min": rows[a]["SimTime_s"] / 60.0, "t_end_min": rows[b]["SimTime_s"] / 60.0,
                    "message": flags[a]})

    for i, message in enumerate(flags):
        if message is None:
            continue
        if start is not None and i - last > gap + 1:
            close(start, last)
            start = None
        if start is None:
            start = i
        last = i
    if start is not None:
        close(start, last)
    return out