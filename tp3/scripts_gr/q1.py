import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

x_min, x_max = -10, 8
y_min, y_max = -10, 12

nx, ny = 700, 700
x = np.linspace(x_min, x_max, nx)
y = np.linspace(y_min, y_max, ny)
X, Y = np.meshgrid(x, y)

A = (Y >= X - 4)
B = (Y <= 8)
C = (8*X + 5*Y <= 56)
ALL = A & B & C

xx = np.linspace(x_min, x_max, 1000)
y1 = xx - 4
y2 = np.full_like(xx, 8.0)
y3 = (56 - 8*xx) / 5

plt.figure(figsize=(9, 7))

plt.contourf(X, Y, A.astype(int), levels=[0.5, 1.5], alpha=0.12)
plt.contourf(X, Y, B.astype(int), levels=[0.5, 1.5], alpha=0.12)
plt.contourf(X, Y, C.astype(int), levels=[0.5, 1.5], alpha=0.12)
plt.contourf(X, Y, ALL.astype(int), levels=[0.5, 1.5], alpha=0.45)

plt.plot(xx, y1, linewidth=2, label=r"$y = x - 4$")
plt.plot(xx, y2, linewidth=2, label=r"$y = 8$")
plt.plot(xx, y3, linewidth=2, label=r"$8x + 5y = 56$")

x_int = 15.2 / 2.6
y_int = x_int - 4

plt.scatter([2, x_int], [8, y_int], s=45)
plt.annotate("(2, 8)", (2, 8), textcoords="offset points", xytext=(8, 8))
plt.annotate(f"({x_int:.3f}, {y_int:.3f})", (x_int, y_int), textcoords="offset points", xytext=(8, -12))

plt.xlim(x_min, x_max)
plt.ylim(y_min, y_max)
plt.axhline(0, linewidth=1)
plt.axvline(0, linewidth=1)
plt.grid(True, alpha=0.3)
plt.xlabel("x")
plt.ylabel("y")
plt.title("Inequality regions and their common feasible area")
plt.legend(loc="upper right")
plt.tight_layout()

output_dir = Path(__file__).resolve().parents[1] / "docs" / "images"
output_dir.mkdir(parents=True, exist_ok=True)
output_path = output_dir / "q1_feasible_region.png"

plt.savefig(output_path, dpi=300)
print(f"Image saved to: {output_path}")
