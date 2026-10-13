# /// script
# dependencies = ["matplotlib"]
# ///
"""Put both Lab 7 figures on one A4 sheet at their true size.

Captions are printed underneath, so they do not have to be copied by
hand. Print at 100 percent, not "fit to page", then cut and paste into
the notebook.

Run on the laptop:  uv run printsheet.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

A4 = (8.27, 11.69)
FIG_W, FIG_H = 4.7, 3.3
INK, MUTED = "#0b0b0b", "#52514e"

CAPTIONS = [
    ("Figure 7-1. Wheel speed against PWM duty, both wheels, rover on\n"
     "blocks. Measured 13 Oct 2026, fullspeedtest.py rev 2a841e1, data in\n"
     "plant.csv. Steep below duty 0.2, nearly flat above 0.3: going from\n"
     "0.3 to 1.0 adds only 25 percent more speed. The right wheel does not\n"
     "turn at duty 0.05, placing the deadband there."),
    ("Figure 7-2. Step response of the left wheel to a 150 rpm target at\n"
     "three gain settings, rover on blocks. Measured 13 Oct 2026,\n"
     "pidtest.py rev 2a841e1, data in pid_150_*.csv. Kp 0.001 reaches 90\n"
     "percent in 1.71 s with no overshoot, Kp 0.002 in 0.82 s, Kp 0.004\n"
     "overshoots to 170 rpm at t 0.30 s then rings. Chosen gains are half\n"
     "the oscillation point."),
]

fig = plt.figure(figsize=A4, dpi=300)
left = (A4[0] - FIG_W) / 2 / A4[0]
width = FIG_W / A4[0]
height = FIG_H / A4[1]

for i, (png, caption) in enumerate(zip(("fig7-1.png", "fig7-2.png"), CAPTIONS)):
    bottom = 1 - (0.06 + (i + 1) * height + i * 0.16)
    ax = fig.add_axes([left, bottom, width, height])
    ax.imshow(mpimg.imread(png))
    ax.axis("off")
    fig.text(left, bottom - 0.015, caption, fontsize=7.5, color=INK,
             va="top", ha="left", linespacing=1.5)

fig.text(left, 0.975, "CPSY Lab 7 figures, cut along the edges",
         fontsize=7, color=MUTED, va="top")
fig.savefig("lab7-print-sheet.pdf")
print("wrote lab7-print-sheet.pdf")
