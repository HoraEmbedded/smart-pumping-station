"""Grafcet drawing helpers (IEC 60848 notation) built on matplotlib."""
from matplotlib.patches import Rectangle

SW = 12  # step square size


def step(ax, x, y, num, name="", initial=False, action=None):
    ax.add_patch(Rectangle((x - SW / 2, y - SW / 2), SW, SW, fc="white", ec="black", lw=1.5, zorder=3))
    if initial:
        ax.add_patch(Rectangle((x - SW / 2 + 1.5, y - SW / 2 + 1.5), SW - 3, SW - 3,
                               fc="white", ec="black", lw=1, zorder=4))
    ax.text(x, y, str(num), ha="center", va="center", fontsize=8, fontweight="bold", zorder=5)
    if name:
        ax.text(x - SW / 2 - 2, y, name, ha="right", va="center", fontsize=7.5)
    if action:
        ax.plot([x + SW / 2, x + SW / 2 + 4], [y, y], color="black", lw=1)
        ax.text(x + SW / 2 + 4, y, action, ha="left", va="center", fontsize=7,
                bbox=dict(boxstyle="square,pad=0.35", fc="white", ec="black", lw=1))


def link(ax, p0, p1):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="black", lw=1, zorder=1)


def trans(ax, x, y, text=""):
    ax.plot([x - 4, x + 4], [y, y], color="black", lw=2.5, zorder=4)
    if text:
        ax.text(x + 6, y, text, ha="left", va="center", fontsize=7)


def jump(ax, x, y, target):
    """Arrow leaving the diagram toward a step drawn elsewhere."""
    ax.annotate("", xy=(x, y - 10), xytext=(x, y),
                arrowprops=dict(arrowstyle="-|>", color="black", lw=1, shrinkA=0, shrinkB=0))
    ax.text(x + 2, y - 7.5, f"to {target}", ha="left", va="center", fontsize=7, style="italic")