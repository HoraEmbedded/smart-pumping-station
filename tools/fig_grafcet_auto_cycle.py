"""Grafcet G3: automatic pumping cycle, enclosed in step 30 of G1."""
from common import new_canvas, save, title_block
from grafcet_lib import SW, jump, link, step, trans

fig, ax = new_canvas(11, 14, xlim=(-20, 150), ylim=(-34, 222))
ax.set_title("Grafcet G3: automatic pumping cycle (enclosed in step 30 of G1)", fontsize=12)
h = SW / 2
CX, JX = 40, 80
rows = [200, 168, 136, 104, 72, 40, 8]

steps = [
    (0, "IDLE", True, "No pump command"),
    (1, "SELECT_PUMP", False, "Pick priority pump if available, else the other"),
    (2, "WAIT_RESTART", False, "Wait Restart_Delay_s (P07) for the selected pump"),
    (3, "START", False, "Run command on selected pump"),
    (4, "RUNNING", False, "Run command held, flow check after P06"),
    (5, "STOP_PUMP", False, "Run command off"),
    (6, "SWAP_PRIORITY", False, "Toggle priority pump"),
]
recept = [
    "Level <= P01 and no inhibit",
    "Selected pump available",
    "Restart delay done",
    "Run feedback confirmed",
    "Level >= P02",
    "Run feedback off",
]

ax.text(-18, 214, "Enclosed Grafcet: activated by step 30 of G1, reset when step 30 is left",
        fontsize=8, style="italic")

for i, (num, name, init, action) in enumerate(steps):
    y = rows[i]
    step(ax, CX, y, num, name, initial=init, action=action)
    if i < len(steps) - 1:
        link(ax, (CX, y - h), (CX, y - 16))
        trans(ax, CX, y - 16, recept[i])
        link(ax, (CX, y - 16), (CX, rows[i + 1] + h))

# Last step: return to step 0
link(ax, (CX, rows[-1] - h), (CX, rows[-1] - 16))
trans(ax, CX, rows[-1] - 16, "1")
jump(ax, CX, rows[-1] - 16, "step 0")

# Alternative exits back to step 1 (pump lost during start or run)
for i, text in ((3, "Run feedback timeout (P23)"), (4, "Flow low after P06 or pump fault")):
    y = rows[i]
    link(ax, (CX, y - 9), (JX, y - 9))
    link(ax, (JX, y - 9), (JX, y - 16))
    trans(ax, JX, y - 16, text)
    jump(ax, JX, y - 16, "step 1")

ax.text(-18, -31, "At step 1, if no pump is available: ALM_009 is raised and G0 forces G1 to step 90.",
        fontsize=8)

title_block(fig, "grafcet_auto_cycle")
save(fig, "grafcet_auto_cycle")