"""Reliability and performance indicators computed from the export datasets."""
import csv

# AlarmWord1 bits that make a pump unavailable: low flow, then pump fault.
PUMP_BITS = {1: (3, 5), 2: (4, 6)}

KPI_KEYS = [
    "sim_hours", "station_availability_pct", "fault_share_pct",
    "pump1_availability_pct", "pump2_availability_pct",
    "run_hours_p1", "run_hours_p2", "duty_p1_pct", "duty_p2_pct",
    "starts_p1", "starts_p2", "starts_per_hour",
    "mean_flow_pumping_m3h", "volume_m3", "energy_kwh", "specific_energy_kwh_m3",
    "failures_p1", "failures_p2", "mtbf_p1_h", "mtbf_p2_h", "mttr_p1_h", "mttr_p2_h",
]


def load_rows(path):
    """Read a dataset, skipping incomplete lines (the last one may be half written)."""
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for raw in csv.DictReader(f):
            if None in raw or None in raw.values():
                continue
            try:
                rows.append({k: v if k == "Timestamp" else float(v) for k, v in raw.items()})
            except ValueError:
                continue
    return rows


def _unavailable(row, pump):
    word = int(row["AlarmWord1"])
    return any((word >> bit) & 1 for bit in PUMP_BITS[pump])


def _intervals(rows):
    """Yield each sample with the duration of the interval that starts at it."""
    for a, b in zip(rows, rows[1:]):
        dt = b["SimTime_s"] - a["SimTime_s"]
        if dt > 0:
            yield a, dt


def _pump_events(rows, pump):
    """Count failures and list the durations of completed repairs, in simulated seconds."""
    failures, repairs, open_s, down = 0, [], 0.0, False
    for a, b in zip(rows, rows[1:]):
        now = _unavailable(a, pump)
        if now and not down:
            failures += 1
            open_s = 0.0
        if down and not now:
            repairs.append(open_s)
        down = now
        if now:
            open_s += max(b["SimTime_s"] - a["SimTime_s"], 0.0)
    return failures, repairs


def compute(rows):
    out = {key: None for key in KPI_KEYS}
    out["rows"] = len(rows)
    if len(rows) < 2:
        return out
    t_total = t_basis = t_fault = 0.0
    t_run = {1: 0.0, 2: 0.0}
    t_down = {1: 0.0, 2: 0.0}
    t_pumping = flow_time = volume = energy = 0.0
    for row, dt in _intervals(rows):
        t_total += dt
        if row["StationState"] != 0:
            t_basis += dt
            if row["StationState"] == 90:
                t_fault += dt
        running = [p for p in (1, 2) if row[f"P{p}_RunFeedback"] >= 0.5]
        for p in running:
            t_run[p] += dt
        for p in (1, 2):
            if _unavailable(row, p):
                t_down[p] += dt
        if running:
            t_pumping += dt
            flow_time += row["Flow_m3h"] * dt
        volume += row["Flow_m3h"] * dt / 3600.0
        energy += row["Power_kW"] * dt / 3600.0
    if t_total <= 0:
        return out

    hours = t_total / 3600.0
    starts = {p: max(0.0, rows[-1][f"P{p}_StartCount"] - rows[0][f"P{p}_StartCount"]) for p in (1, 2)}
    out["sim_hours"] = round(hours, 3)
    if t_basis > 0:
        out["station_availability_pct"] = round(100.0 * (1.0 - t_fault / t_basis), 2)
        out["fault_share_pct"] = round(100.0 * t_fault / t_basis, 2)
    for p in (1, 2):
        failures, repairs = _pump_events(rows, p)
        out[f"pump{p}_availability_pct"] = round(100.0 * (1.0 - t_down[p] / t_total), 2)
        out[f"run_hours_p{p}"] = round(t_run[p] / 3600.0, 4)
        out[f"duty_p{p}_pct"] = round(100.0 * t_run[p] / t_total, 2)
        out[f"starts_p{p}"] = int(starts[p])
        out[f"failures_p{p}"] = failures
        if failures:
            out[f"mtbf_p{p}_h"] = round(t_run[p] / 3600.0 / failures, 4)
        if repairs:
            out[f"mttr_p{p}_h"] = round(sum(repairs) / len(repairs) / 3600.0, 4)
    out["starts_per_hour"] = round((starts[1] + starts[2]) / hours, 3)
    if t_pumping > 0:
        out["mean_flow_pumping_m3h"] = round(flow_time / t_pumping, 3)
    out["volume_m3"] = round(volume, 4)
    out["energy_kwh"] = round(energy, 4)
    if volume > 0.01:
        out["specific_energy_kwh_m3"] = round(energy / volume, 4)
    return out