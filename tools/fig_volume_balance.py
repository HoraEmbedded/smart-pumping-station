"""Tank volume balance: reference scenario with hysteresis control."""
from common import save
import matplotlib.pyplot as plt

V_TANK = 10.0  # m3
Q_PUMP = 12.0  # m3/h
Q_OUT = 3.0    # m3/h
DT = 0.1       # s
LOW, HIGH, CRIT = 30.0, 80.0, 95.0


def rate(q_in, q_out=Q_OUT):
    """Level change in percent per second."""
    return 100.0 * (q_in - q_out) / (3600.0 * V_TANK)


def simulate(minutes):
    steps = int(minutes * 60 / DT)
    level, pump = LOW, True
    t, lv = [], []
    for k in range(steps):
        if pump and level >= HIGH:
            pump = False
        elif not pump and level <= LOW:
            pump = True
        level += DT * rate(Q_PUMP if pump else 0.0)
        t.append(k * DT / 60.0)
        lv.append(level)
    return t, lv


rise, fall = rate(Q_PUMP), rate(0.0)
fill_s = (HIGH - LOW) / rise
drain_s = (HIGH - LOW) / -fall
cycle_s = fill_s + drain_s
print(f"rise  : {rise:.4f} %/s = {rise * 60:.2f} %/min")
print(f"fall  : {fall:.4f} %/s = {fall * 60:.2f} %/min")
print(f"fill  : {fill_s / 60:.1f} min   drain: {drain_s / 60:.1f} min   cycle: {cycle_s / 60:.1f} min")
print(f"starts: {3600 / cycle_s:.2f} per hour   pump duty: {100 * fill_s / cycle_s:.0f} %")

t, lv = simulate(minutes=400)
fig, ax = plt.subplots(figsize=(11, 5))
ax.plot(t[::10], lv[::10], color="#1f6fb4", label="tank level")
ax.axhline(LOW, color="green", ls="--", label="start threshold (30 %)")
ax.axhline(HIGH, color="orange", ls="--", label="stop threshold (80 %)")
ax.axhline(CRIT, color="red", ls=":", label="critical high (95 %)")
ax.set_xlabel("time (min)")
ax.set_ylabel("tank level (%)")
ax.set_title("Reference scenario: hysteresis cycles (simulated, 10 m3 tank, 12 m3/h pump, 3 m3/h drain)")
ax.legend(loc="lower right")
ax.grid(alpha=0.3)
save(fig, "volume_balance_cycle", formats=("png",))