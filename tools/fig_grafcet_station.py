"""Grafcet G1 (station modes) and supervisor G0 (stop and fault forcing)."""
from common import new_canvas, save, title_block
from grafcet_lib import SW, jump, link, step, trans

fig, ax = new_canvas(16, 14, xlim=(-25, 250), ylim=(-34, 218))
ax.set_title("Grafcet of the station: modes (G1) and supervisor (G0)", fontsize=12)
h = SW / 2
CX, LEFT, RIGHT, FAULT_X = 95, 20, 170, 205

# G1 main chain
ax.text(-24, 212, "G1  Station operating modes", fontsize=10, fontweight="bold")
step(ax, CX, 200, 0, "STOPPED", initial=True, action="Pumps off")
link(ax, (CX, 200 - h), (CX, 184))
trans(ax, CX, 184, "Start request (rising) and E-stop healthy")
link(ax, (CX, 184), (CX, 168 + h))
step(ax, CX, 168, 10, "INITIALIZING", action="Read inputs, check coherence")
link(ax, (CX, 168 - h), (CX, 152))
trans(ax, CX, 152, "Init_Delay_s (P24) elapsed and no critical alarm")
link(ax, (CX, 152), (CX, 136 + h))
step(ax, CX, 136, 20, "READY", action="Pumps off, mode selection")

# OR divergence into the three modes
link(ax, (CX, 136 - h), (CX, 124))
link(ax, (LEFT, 124), (RIGHT, 124))
branches = [
    (LEFT, 30, "AUTO_RUNNING", "Auto cycle enabled (G3)", "Mode_Auto selected", "Selector left Auto"),
    (CX, 40, "MANUAL_RUNNING", "Manual commands enabled", "Mode_Manual selected", "Selector left Manual"),
    (RIGHT, 50, "MAINTENANCE", "Pump tests enabled", "Mode_Maintenance selected", "Selector left Maintenance"),
]
for x, num, name, action, enter, leave in branches:
    link(ax, (x, 124), (x, 116))
    trans(ax, x, 116, enter)
    link(ax, (x, 116), (x, 104 + h))
    step(ax, x, 104, num, name, action=action)
    link(ax, (x, 104 - h), (x, 90))
    trans(ax, x, 90, leave)
    jump(ax, x, 90, "step 20")

# FAULT step, entered only by forcing from G0
step(ax, FAULT_X, 136, 90, "FAULT", action="Pumps off, red lamp, siren")
link(ax, (FAULT_X, 136 - h), (FAULT_X, 120))
trans(ax, FAULT_X, 120, "S0 active (fault released)")
jump(ax, FAULT_X, 120, "step 0")

# G0 supervisor
ax.text(-24, 58, "G0  Supervisor (forces G1)", fontsize=10, fontweight="bold")
step(ax, CX, 40, "S0", "MONITORING", initial=True, action="No forcing order")
link(ax, (CX, 40 - h), (CX, 28))
link(ax, (LEFT, 28), (RIGHT, 28))
g0 = [
    (LEFT, "S2", "STOP_REQUEST", "F/G1:{0}", "Stop request and no fault", "Step 0 of G1 active"),
    (RIGHT, "S1", "FAULT_LATCH", "F/G1:{90}",
     "ALM_001 or ALM_003 or ALM_009 or tank sensor ALM_008", "Reset and causes cleared"),
]
for x, num, name, action, enter, leave in g0:
    link(ax, (x, 28), (x, 20))
    trans(ax, x, 20, enter)
    link(ax, (x, 20), (x, 8 + h))
    step(ax, x, 8, num, name, action=action)
    link(ax, (x, 8 - h), (x, -8))
    trans(ax, x, -8, leave)
    jump(ax, x, -8, "S0")

ax.text(-24, -31, "F/G1:{n} = forcing order: while this step is active, G1 is held with only step n active.",
        fontsize=8)

title_block(fig, "grafcet_station")
save(fig, "grafcet_station")
