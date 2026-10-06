"""Simplified P&ID (ISA 5.1 tags) with PLC tag names on every signal."""
from common import (SIGNAL, WATER, arrow, bubble, check, motor, new_canvas, pipe,
                    pump, save, sig, tank, thin, title_block, valve)

fig, ax = new_canvas(17, 9.5, xlim=(-2, 184), ylim=(-6, 100))
ax.set_title("Simplified P&ID: utility pumping station", fontsize=12)

# Tanks
tank(ax, 5, 25, 22, 30, 0.6, "T-001\nLow source")
tank(ax, 135, 25, 22, 30, 0.6, "T-101\nStorage tank")

# Piping
pipe(ax, [(27, 40), (42, 40)])
pipe(ax, [(42, 10), (42, 70)])
pipe(ax, [(108, 10), (108, 70)])
pipe(ax, [(108, 40), (135, 40)])
pipe(ax, [(157, 30), (172, 30)])
arrow(ax, (172, 30), (181, 30), color=WATER, lw=3)

# Two parallel pump branches
for n, y in ((1, 70), (2, 10)):
    pipe(ax, [(42, y), (64, y)])
    pipe(ax, [(76, y), (108, y)])
    valve(ax, 50, y, f"V-10{n}")
    pump(ax, 70, y, f"P-10{n}\nPump {n}", up=(n == 1))
    check(ax, 88, y, f"CV-10{n}")
    valve(ax, 98, y, f"V-10{n + 2}")

valve(ax, 166, 30, "V-105")
ax.text(170, 24, "consumption\n(simulated)", ha="center", va="top", fontsize=7)

# Motors and their signals (pump 1 above the middle zone, pump 2 below it)
motor(ax, 65, 58, 10, 6, "M-101")
sig(ax, 66.5, 58, 51, "DO_P1_RunCmd", into=True)
sig(ax, 70, 58, 51, "DI_P1_RunFeedback")
sig(ax, 73.5, 58, 51, "DI_P1_Fault")
bubble(ax, 86, 61, "II-101")
thin(ax, (82, 61), (75, 61))
sig(ax, 86, 57, 51, "AI_P1_Current_A")

motor(ax, 65, 16, 10, 6, "M-102")
sig(ax, 66.5, 22, 26, "DO_P2_RunCmd", into=True)
sig(ax, 70, 22, 26, "DI_P2_RunFeedback")
sig(ax, 73.5, 22, 26, "DI_P2_Fault")
bubble(ax, 86, 19, "II-102")
thin(ax, (82, 19), (75, 19))
sig(ax, 86, 23, 28, "AI_P2_Current_A")

# Process instruments
bubble(ax, 11, 64, "LT-001")
thin(ax, (11, 60), (11, 55))
sig(ax, 11, 68, 74, "AI_Source_Level_pct")
bubble(ax, 24, 64, "LSL-001")
thin(ax, (24, 60), (24, 55))
sig(ax, 24, 68, 74, "DI_Source_Low")

bubble(ax, 116, 52, "FT-101")
thin(ax, (116, 48), (116, 40))
sig(ax, 116, 56, 62, "AI_Flow_m3h")
bubble(ax, 126, 52, "PT-101")
thin(ax, (126, 48), (126, 40))
sig(ax, 126, 56, 62, "AI_Pressure_bar")

bubble(ax, 146, 64, "LT-101")
thin(ax, (146, 60), (146, 55))
sig(ax, 146, 68, 74, "AI_Tank_Level_pct")

# Legend
ax.plot([100, 110], [-2, -2], color=WATER, lw=3)
ax.text(112, -2, "water", va="center", fontsize=8)
ax.plot([128, 138], [-2, -2], color=SIGNAL, lw=1.5, ls="--")
ax.text(140, -2, "signal to or from PLC S7-1200 (tag names as in io_list.csv)", va="center", fontsize=8)

title_block(fig, "pid_simplified")
save(fig, "pid_simplified")