"""OT / IT data architecture."""
from matplotlib.patches import Rectangle

from common import arrow, box, new_canvas, save, title_block

fig, ax = new_canvas(18, 7, xlim=(0, 190), ylim=(0, 70))
ax.set_title("OT / IT data architecture", fontsize=12)


def zone(x, y, w, h, label):
    ax.add_patch(Rectangle((x, y), w, h, fc="none", ec="#777777", lw=1.2, ls="--", zorder=0))
    ax.text(x + 2, y + h - 2, label, ha="left", va="top", fontsize=9, color="#555555")


zone(2, 6, 64, 58, "OT zone")
zone(84, 6, 104, 58, "IT zone (local)")

box(ax, 6, 36, 24, 16, "PLC S7-1200\nDB_IIoTExport", fc="#fdf2d9")
box(ax, 38, 36, 24, 16, "WinCC Runtime\nOPC UA server", fc="#e6f4e6")
box(ax, 38, 12, 24, 14, "HMI screens", fc="#e6f4e6")
box(ax, 88, 32, 26, 16, "Collector\nPython, read only", fc="#e8f1fa")
box(ax, 122, 32, 22, 16, "CSV datasets", fc="#f2f2f2")
box(ax, 154, 42, 32, 14, "Dashboard and KPI", fc="#f2f2f2")
box(ax, 154, 16, 32, 14, "Anomaly rules\n(Python)", fc="#f2f2f2")

arrow(ax, (30, 44), (38, 44), both=True)
ax.text(34, 47, "HMI link", ha="center", va="bottom", fontsize=8)
arrow(ax, (50, 36), (50, 26), both=True)
arrow(ax, (62, 44), (88, 44))
ax.text(75, 47, "OPC UA, read only", ha="center", va="bottom", fontsize=8)
arrow(ax, (114, 40), (122, 40))
arrow(ax, (144, 42), (154, 49))
arrow(ax, (144, 38), (154, 23))

ax.text(4, 2, "Local lab PC only, no Internet exposure. The collector only reads.", fontsize=8)

title_block(fig, "architecture_ot_it")
save(fig, "architecture_ot_it")