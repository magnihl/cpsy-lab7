# /// script
# dependencies = ["matplotlib"]
# ///
"""Figures for the Lab 7 notebook.

Reads plant.csv and the pid_*.csv files, writes fig7-1.png and
fig7-2.png at A5 notebook size.

Run on the laptop:  uv run plot7.py
"""

import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

BLUE, ORANGE, AQUA = "#2a78d6", "#eb6834", "#1baf7a"
INK, MUTED = "#0b0b0b", "#52514e"
TARGET = 150.0
SIZE = (4.7, 3.3)


def read(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def tidy(ax):
    """Recessive axes and grid, so the data carries the figure."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color(MUTED)
        ax.spines[side].set_linewidth(0.6)
    ax.tick_params(colors=MUTED, labelsize=7, width=0.6)
    ax.grid(True, color="#d8d7d2", linewidth=0.5, alpha=0.8)
    ax.set_axisbelow(True)
    ax.xaxis.label.set_color(INK)
    ax.yaxis.label.set_color(INK)
    ax.xaxis.label.set_size(8)
    ax.yaxis.label.set_size(8)


# --- figure 1, the plant ------------------------------------------
rows = read("plant.csv")
duty = [float(r["duty"]) for r in rows]
left = [float(r["left_rpm"]) for r in rows]
right = [float(r["right_rpm"]) for r in rows]

fig, ax = plt.subplots(figsize=SIZE, dpi=300)
ax.plot(duty, left, color=BLUE, linewidth=1.6, marker="o", markersize=4,
        label="left wheel")
ax.plot(duty, right, color=ORANGE, linewidth=1.6, marker="s", markersize=4,
        linestyle="--", label="right wheel")
ax.annotate("left", (duty[-1], left[-1]), textcoords="offset points",
            xytext=(-4, 7), color=BLUE, fontsize=7.5, ha="right")
ax.annotate("right", (duty[-1], right[-1]), textcoords="offset points",
            xytext=(-4, -12), color=ORANGE, fontsize=7.5, ha="right")
ax.set_xlabel("PWM duty")
ax.set_ylabel("wheel speed (rpm)")
ax.set_xlim(0, 1.05)
ax.set_ylim(0, 250)
tidy(ax)
fig.tight_layout()
fig.savefig("fig7-1.png")
plt.close(fig)
print("wrote fig7-1.png")

# --- figure 2, the step response ----------------------------------
runs = [
    ("Kp 0.001, Ki 0.002", "pid_150_0.001_0.002_0.0.csv", BLUE, "-", "o"),
    ("Kp 0.002, Ki 0.004", "pid_150_0.002_0.004_0.0.csv", ORANGE, "--", "s"),
    ("Kp 0.004, Ki 0.008", "pid_150_0.004_0.008_0.0.csv", AQUA, ":", "^"),
]

fig, ax = plt.subplots(figsize=SIZE, dpi=300)
ax.axhline(TARGET, color=MUTED, linewidth=0.8, linestyle="-", alpha=0.7)
ax.annotate("target 150", (1.7, TARGET), textcoords="offset points",
            xytext=(0, 20), color=MUTED, fontsize=7, ha="center")

for label, path, colour, style, marker in runs:
    rows = [r for r in read(path) if float(r["t"]) <= 6.0]
    t = [float(r["t"]) for r in rows]
    rpm = [float(r["left_rpm"]) for r in rows]
    ax.plot(t, rpm, color=colour, linewidth=1.4, linestyle=style,
            label=label, marker=marker, markersize=2.5, markevery=6)

ax.set_xlabel("time (s)")
ax.set_ylabel("left wheel speed (rpm)")
ax.set_xlim(0, 6)
ax.set_ylim(0, 190)
tidy(ax)
leg = ax.legend(frameon=False, fontsize=7, loc="lower right")
for text in leg.get_texts():
    text.set_color(INK)
fig.tight_layout()
fig.savefig("fig7-2.png")
plt.close(fig)
print("wrote fig7-2.png")
