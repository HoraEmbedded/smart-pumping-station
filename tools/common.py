"""Shared drawing helpers for project figures (matplotlib only)."""
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Polygon, Rectangle

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "02_design" / "diagrams"
WATER = "#1f6fb4"
SIGNAL = "#555555"
VERSION = "V0.1"
AUTHOR = "HoraEmbedded"


def new_canvas(width, height, xlim, ylim):
    fig, ax = plt.subplots(figsize=(width, height))
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax


def box(ax, x, y, w, h, label, fc="#f2f2f2", fs=10):
    ax.add_patch(Rectangle((x, y), w, h, fc=fc, ec="black", lw=1.5, zorder=2))
    ax.text(x + w / 2, y + h / 2, label, ha="center", va="center", fontsize=fs, zorder=3)


def arrow(ax, p0, p1, color=SIGNAL, ls="-", lw=1.5, both=False):
    style = "<|-|>" if both else "-|>"
    ax.annotate(
        "", xy=p1, xytext=p0,
        arrowprops=dict(arrowstyle=style, color=color, lw=lw, linestyle=ls, shrinkA=0, shrinkB=0),
    )


def pipe(ax, pts):
    xs, ys = zip(*pts)
    ax.plot(xs, ys, color=WATER, lw=3, solid_capstyle="butt", zorder=1)


def thin(ax, p0, p1):
    ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="black", lw=1, zorder=1)


def tank(ax, x, y, w, h, level, label):
    ax.add_patch(Rectangle((x, y), w, h * level, fc=WATER, ec="none", alpha=0.35))
    ax.add_patch(Rectangle((x, y), w, h, fc="none", ec="black", lw=1.8, zorder=2))
    ax.text(x + w / 2, y - 1.5, label, ha="center", va="top", fontsize=8)


def valve(ax, x, y, tag, s=2.8):
    pts = [(x - s, y + s), (x + s, y - s), (x + s, y + s), (x - s, y - s)]
    ax.add_patch(Polygon(pts, fc="white", ec="black", lw=1.2, zorder=3))
    ax.text(x, y + s + 1.2, tag, ha="center", va="bottom", fontsize=7)


def check(ax, x, y, tag, s=2.8):
    ax.add_patch(Polygon([(x - s, y + s), (x - s, y - s), (x + s, y)],
                         fc="white", ec="black", lw=1.2, zorder=3))
    ax.plot([x + s, x + s], [y - s, y + s], color="black", lw=1.5, zorder=3)
    ax.text(x, y + s + 1.2, tag, ha="center", va="bottom", fontsize=7)


def pump(ax, x, y, tag, r=6, up=True):
    ax.add_patch(Circle((x, y), r, fc="white", ec="black", lw=1.5, zorder=3))
    ax.add_patch(Polygon([(x - r * 0.45, y + r * 0.6), (x - r * 0.45, y - r * 0.6), (x + r * 0.7, y)],
                         fc="#cfe3f5", ec="black", lw=1, zorder=4))
    if up:
        ax.text(x, y + r + 2, tag, ha="center", va="bottom", fontsize=8)
    else:
        ax.text(x, y - r - 2, tag, ha="center", va="top", fontsize=8)


def motor(ax, x, y, w, h, tag):
    ax.add_patch(Rectangle((x, y), w, h, fc="#eeeeee", ec="black", lw=1.2, zorder=3))
    ax.text(x + w / 2, y + h / 2, tag, ha="center", va="center", fontsize=7, zorder=4)


def bubble(ax, x, y, tag, r=4):
    letters, number = tag.split("-")
    ax.add_patch(Circle((x, y), r, fc="white", ec="black", lw=1.2, zorder=3))
    ax.plot([x - r, x + r], [y, y], color="black", lw=0.8, zorder=4)
    ax.text(x, y + 1.6, letters, ha="center", va="center", fontsize=7, zorder=5)
    ax.text(x, y - 1.6, number, ha="center", va="center", fontsize=7, zorder=5)


def sig(ax, x, y_dev, y_far, text, into=False):
    """Dashed vertical signal with its PLC tag name written at the far end."""
    if into:
        arrow(ax, (x, y_far), (x, y_dev), SIGNAL, "--", 1.1)
    else:
        arrow(ax, (x, y_dev), (x, y_far), SIGNAL, "--", 1.1)
    if y_far > y_dev:
        ax.text(x, y_far + 0.8, text, rotation=90, ha="center", va="bottom", fontsize=6.5, color=SIGNAL)
    else:
        ax.text(x, y_far - 0.8, text, rotation=90, ha="center", va="top", fontsize=6.5, color=SIGNAL)


def title_block(fig, name):
    stamp = f"{name} | {VERSION} | {date.today().isoformat()} | {AUTHOR}"
    fig.text(0.99, 0.01, stamp, ha="right", va="bottom", fontsize=7, color="#333333")


def save(fig, name, formats=("png", "svg", "pdf")):
    OUT.mkdir(parents=True, exist_ok=True)
    for ext in formats:
        path = OUT / f"{name}.{ext}"
        fig.savefig(path, dpi=200, bbox_inches="tight")
        print(f"saved {path}")