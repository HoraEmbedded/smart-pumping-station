"""Process block diagram: source, pumps, line, tank, consumption, PLC and HMI."""
from common import SIGNAL, WATER, arrow, box, new_canvas, save, title_block

fig, ax = new_canvas(15, 8, xlim=(0, 152), ylim=(-2, 80))
ax.set_title("Process block diagram: utility pumping station", fontsize=12)

names = [
    "Low source\n(T-001)",
    "Pumps P1 / P2\n(duty / standby)",
    "Discharge line",
    "Storage tank\n(T-101)",
    "Simulated\nconsumption",
]
xs = [5, 35, 65, 95, 125]
for x, name in zip(xs, names):
    box(ax, x, 45, 22, 20, name, fc="#e8f1fa")
for x in xs[:-1]:
    arrow(ax, (x + 22, 55), (x + 30, 55), color=WATER, lw=3)

box(ax, 40, 8, 45, 16, "PLC S7-1200\n(control logic)", fc="#fdf2d9")
box(ax, 105, 8, 30, 16, "HMI / SCADA", fc="#e6f4e6")

arrow(ax, (46, 24), (46, 45), SIGNAL, "--")
ax.text(44, 34, "run commands\nP1, P2", ha="right", va="center", fontsize=8)
arrow(ax, (76, 45), (76, 24), SIGNAL, "--")
ax.text(78, 34, "measurements: tank and source level,\nflow, pressure, current,\nrun feedback, faults",
        ha="left", va="center", fontsize=8)
arrow(ax, (85, 16), (105, 16), SIGNAL, "--", both=True)
ax.text(95, 18, "tags", ha="center", va="bottom", fontsize=8)

ax.plot([5, 15], [-1, -1], color=WATER, lw=3)
ax.text(17, -1, "water", va="center", fontsize=8)
ax.plot([35, 45], [-1, -1], color=SIGNAL, lw=1.5, ls="--")
ax.text(47, -1, "signal", va="center", fontsize=8)

title_block(fig, "process_block_diagram")
save(fig, "process_block_diagram")