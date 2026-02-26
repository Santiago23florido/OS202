import itertools
from fractions import Fraction

import numpy as np

from tableau import Tableau


EPS = 1e-6


def _clean(v):
    if abs(v) < EPS:
        return 0.0
    return float(v)


def solve_ex4():
    problems = [
        {
            "name": "Exercise 4 - Problem 1",
            "A": np.array([[5, 3], [2, 3], [1, 3]], dtype=float),
            "b": np.array([30, 24, 18], dtype=float),
            "c": np.array([8, 6], dtype=float),
        },
        {
            "name": "Exercise 4 - Problem 2",
            "A": np.array([[-3, 2], [-1, 2], [1, 1]], dtype=float),
            "b": np.array([2, 4, 5], dtype=float),
            "c": np.array([1, 2], dtype=float),
        },
    ]

    print("=== Exercise 4 ===")
    for p in problems:
        t = Tableau(p["A"], p["b"], p["c"], False)
        t.DISPLAY_SIMPLEX_LOGS = False
        t.addSlackAndSolve()
        x1 = _clean(t.bestSolution[0])
        x2 = _clean(t.bestSolution[1])
        z = _clean(t.bestObjective)
        print(p["name"])
        print(f"Optimal solution: x1 = {x1:.6f}, x2 = {x2:.6f}")
        print(f"Optimal value: z = {z:.6f}")
        print()


def ex5_dual_and_cs_text():
    print("=== Exercise 5 ===")
    print("Dual problem:")
    print("max w = 3y1 + 5y2 + 6y3")
    print("s.t.")
    print("2y1 + 2y2 + y3 <= 2")
    print("y1 - y2 + 4y3 <= 3")
    print("y1, y2, y3 >= 0")
    print()
    print("Complementary slackness constraints:")
    print("x1 * (2 - (2y1 + 2y2 + y3)) = 0")
    print("x2 * (3 - (y1 - y2 + 4y3)) = 0")
    print("y1 * (2x1 + x2 - 3) = 0")
    print("y2 * (2x1 - x2 - 5) = 0")
    print("y3 * (x1 + 4x2 - 6) = 0")
    print()


def _feasible_ex5(x):
    x1, x2 = x
    return (
        x1 >= -EPS
        and x2 >= -EPS
        and 2 * x1 + x2 >= 3 - EPS
        and 2 * x1 - x2 >= 5 - EPS
        and x1 + 4 * x2 >= 6 - EPS
    )


def _active_constraints_ex5(x):
    x1, x2 = x
    values = {
        "C1": 2 * x1 + x2 - 3,
        "C2": 2 * x1 - x2 - 5,
        "C3": x1 + 4 * x2 - 6,
        "x1=0": x1,
        "x2=0": x2,
    }
    return [k for k, v in values.items() if abs(v) <= EPS]


def _is_basic_ex5(x):
    if not _feasible_ex5(x):
        return False
    normals = {
        "C1": np.array([2.0, 1.0]),
        "C2": np.array([2.0, -1.0]),
        "C3": np.array([1.0, 4.0]),
        "x1=0": np.array([1.0, 0.0]),
        "x2=0": np.array([0.0, 1.0]),
    }
    active = _active_constraints_ex5(x)
    if len(active) < 2:
        return False
    for a, b in itertools.combinations(active, 2):
        M = np.vstack([normals[a], normals[b]])
        if abs(np.linalg.det(M)) > EPS:
            return True
    return False


def _objective_ex5(x):
    x1, x2 = x
    return 2 * x1 + 3 * x2


def _intersect(line1, line2):
    A = np.array([[line1[0], line1[1]], [line2[0], line2[1]]], dtype=float)
    b = np.array([line1[2], line2[2]], dtype=float)
    det = np.linalg.det(A)
    if abs(det) <= EPS:
        return None
    return np.linalg.solve(A, b)


def _optimal_ex5():
    lines = [
        (2.0, 1.0, 3.0, "C1"),
        (2.0, -1.0, 5.0, "C2"),
        (1.0, 4.0, 6.0, "C3"),
        (1.0, 0.0, 0.0, "x1=0"),
        (0.0, 1.0, 0.0, "x2=0"),
    ]
    candidates = []
    for i in range(len(lines)):
        for j in range(i + 1, len(lines)):
            p = _intersect(lines[i], lines[j])
            if p is None:
                continue
            if _feasible_ex5(p):
                candidates.append((p, (lines[i][3], lines[j][3])))
    if not candidates:
        raise RuntimeError("No feasible vertex found for Exercise 5.")
    best = min(candidates, key=lambda item: _objective_ex5(item[0]))
    return best[0], best[1], _objective_ex5(best[0])


def _fmt_fraction(v):
    return str(Fraction(v).limit_denominator())


def evaluate_ex5_points():
    opt_x, opt_active, opt_z = _optimal_ex5()

    print("Reference optimum for Exercise 5:")
    print(
        "x* = ("
        + _fmt_fraction(opt_x[0])
        + ", "
        + _fmt_fraction(opt_x[1])
        + f"), z* = {_fmt_fraction(opt_z)} ({opt_z:.6f})"
    )
    print(f"Active constraints at optimum: {opt_active[0]}, {opt_active[1]}")
    print()

    points = [
        ("Point A", np.array([3.0, 1.0])),
        ("Point B", np.array([26.0 / 9.0, 7.0 / 9.0])),
    ]

    for name, x in points:
        feasible = _feasible_ex5(x)
        basic = _is_basic_ex5(x)
        z = _objective_ex5(x)
        optimal = feasible and abs(z - opt_z) <= 1e-5
        print(f"{name}: x1 = {x[0]:.6f}, x2 = {x[1]:.6f}")
        print(f"Feasible: {feasible}")
        print(f"Basic: {basic}")
        print(f"Objective value: z = {z:.6f}")
        print(f"Optimal: {optimal}")
        print()


def main():
    solve_ex4()
    ex5_dual_and_cs_text()
    evaluate_ex5_points()


if __name__ == "__main__":
    main()
