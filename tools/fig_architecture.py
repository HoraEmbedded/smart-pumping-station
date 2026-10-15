"""OT / IT data architecture."""
from matplotlib.patches import Rectangle

from common import arrow, box, new_canvas, save, title_block

fig, ax = new_canvas(16, 7, xlim=(0, 170), ylim=(0, 70))
ax.set_title("OT / IT data architecture", fontsize=12)


def zone(x, y, w, h, label):
    ax.add_patch(Rectangle((x, y), w, h, fc="none", ec="#777777", lw=1.2, ls="--", zorder=0))
    ax.text(x + 2, y + h - 2, label, ha="left", va="top", fontsize=9, color="#555555")


zone(2, 6, 38, 58, "OT zone")
zone(88, 6, 80, 58, "IT zone (local)")

box(ax, 6, 36, 30, 16, "PLC S7-1200\nDB_IIoTExport", fc="#fdf2d9")
box(ax, 6, 12, 30, 14, "HMI\nWinCC Runtime", fc="#e6f4e6")
box(ax, 54, 30, 30, 16, "Collector\nPython, read only", fc="#e8f1fa")
box(ax, 94, 30, 24, 16, "CSV datasets", fc="#f2f2f2")
box(ax, 128, 40, 36, 14, "Dashboard and KPI", fc="#f2f2f2")
box(ax, 128, 14, 36, 14, "Anomaly rules\n(Python)", fc="#f2f2f2")

arrow(ax, (21, 26), (21, 36), both=True)
ax.text(23, 31, "tags", ha="left", va="center", fontsize=8)
arrow(ax, (36, 44), (54, 44))
ax.text(45, 47, "S7 read, 1 s", ha="center", va="bottom", fontsize=8)
arrow(ax, (84, 38), (94, 38))
arrow(ax, (118, 42), (128, 46))
arrow(ax, (118, 34), (128, 21))

ax.text(4, 2, "Local lab network only, no Internet exposure. The collector only reads.", fontsize=8)

title_block(fig, "architecture_ot_it")
save(fig, "architecture_ot_it")