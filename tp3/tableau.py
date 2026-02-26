import numpy as np


class Tableau:
    EPS = 1e-6

    def __init__(self, A, b, c, isMinimization):
        self.n = len(c)
        self.m = len(A)
        self.A = np.array(A, dtype=np.float64)
        self.b = np.array(b, dtype=np.float64)
        self.c = np.array(c, dtype=np.float64)
        self.isMinimization = bool(isMinimization)
        self.basis = np.array([], dtype=int)
        self.bestSolution = None
        self.bestObjective = 0.0
        self.DISPLAY_SIMPLEX_LOGS = True

    @staticmethod
    def ex1():
        A = np.array([[1, -1], [0, 1], [8, 5]], dtype=float)
        c = np.array([2, 1], dtype=float)
        b = np.array([4, 8, 56], dtype=float)
        return Tableau(A, b, c, False)

    @staticmethod
    def ex2():
        A = np.array(
            [[1, -2, 1, -1, 0, 0], [0, 1, 3, 0, 1, 0], [2, 0, 1, 2, 0, 1]],
            dtype=float,
        )
        c = np.array([2, -3, 5, 0, 0, 0], dtype=float)
        b = np.array([4, 6, 7], dtype=float)
        return Tableau(A, b, c, True)

    def addSlackAndSolve(self):
        tSlack = self.tableauWithSlack()
        tSlack.DISPLAY_SIMPLEX_LOGS = self.DISPLAY_SIMPLEX_LOGS
        tSlack.applySimplex()
        self.setSolution(tSlack)

    def applySimplex(self):
        if self.DISPLAY_SIMPLEX_LOGS:
            print("Initial tableau")
            self.display()

        eps = 1e-7
        for i in range(self.m):
            self.b[i] += eps
            eps *= 0.1

        while self.pivot():
            if self.DISPLAY_SIMPLEX_LOGS:
                self.display()

        if self.DISPLAY_SIMPLEX_LOGS:
            print("Final tableau")
            self.display()

    def pivot(self):
        if len(self.basis) != self.m:
            raise ValueError("Basis must be defined before calling pivot().")

        eps = self.EPS

        for i in range(self.m):
            basic_var = int(self.basis[i])
            pivot_coef = self.A[i][basic_var]

            if abs(pivot_coef) <= eps:
                raise ValueError(
                    f"Invalid basis: A[{i}][{basic_var}] is near zero ({pivot_coef})."
                )

            if abs(pivot_coef - 1.0) > eps:
                self.A[i] /= pivot_coef
                self.b[i] /= pivot_coef

            for r in range(self.m):
                if r == i:
                    continue
                factor = self.A[r][basic_var]
                if abs(factor) > eps:
                    self.A[r] -= factor * self.A[i]
                    self.b[r] -= factor * self.b[i]

            cost_factor = self.c[basic_var]
            if abs(cost_factor) > eps:
                self.c -= cost_factor * self.A[i]
                self.bestObjective += cost_factor * self.b[i]

        self.A[np.abs(self.A) < eps] = 0.0
        self.b[np.abs(self.b) < eps] = 0.0
        self.c[np.abs(self.c) < eps] = 0.0
        if abs(self.bestObjective) < eps:
            self.bestObjective = 0.0

        if self.DISPLAY_SIMPLEX_LOGS:
            print("Tableau in canonical form")
            self.display()

        entering = -1
        if self.isMinimization:
            best_value = -eps
            for j in range(self.n):
                if self.c[j] < best_value:
                    best_value = self.c[j]
                    entering = j
        else:
            best_value = eps
            for j in range(self.n):
                if self.c[j] > best_value:
                    best_value = self.c[j]
                    entering = j

        if entering == -1:
            return False

        if self.DISPLAY_SIMPLEX_LOGS:
            print(f"Entering variable: x{entering + 1}")

        leaving_row = -1
        best_ratio = np.inf

        for i in range(self.m):
            a_ie = self.A[i][entering]
            if a_ie > eps:
                ratio = self.b[i] / a_ie
                if ratio < best_ratio - eps:
                    best_ratio = ratio
                    leaving_row = i
                elif abs(ratio - best_ratio) <= eps and leaving_row != -1:
                    if int(self.basis[i]) < int(self.basis[leaving_row]):
                        leaving_row = i

        if leaving_row == -1:
            if self.DISPLAY_SIMPLEX_LOGS:
                print("No leaving variable found.")
            return False

        leaving_var = int(self.basis[leaving_row])
        if self.DISPLAY_SIMPLEX_LOGS:
            print(f"Leaving variable: x{leaving_var + 1}")

        self.basis[leaving_row] = entering
        return True

    def getSolution(self):
        self.bestSolution = np.array([0.0] * self.n)
        for row in range(self.m):
            var_id = int(self.basis[row])
            self.bestSolution[var_id] = self.b[row]

    def setSolution(self, tSlack):
        tSlack.getSolution()
        self.bestSolution = np.array([0.0] * self.n)
        for var_id in range(self.n):
            self.bestSolution[var_id] = tSlack.bestSolution[var_id]
        self.bestObjective = tSlack.bestObjective

    def displaySolution(self):
        if self.bestSolution is None:
            self.getSolution()
        print(f"z = {self.bestObjective:.6f}")
        parts = []
        for i, value in enumerate(self.bestSolution):
            if abs(value) > self.EPS:
                parts.append(f"x{i + 1}={value:.6f}")
        print(", ".join(parts) if parts else "All variables are 0")

    def tableauWithSlack(self):
        ASlack = np.zeros((self.m, self.n + self.m))
        for r in range(self.m):
            ASlack[r, : self.n] = self.A[r]
            ASlack[r, self.n + r] = 1.0

        cSlack = np.zeros(self.n + self.m)
        cSlack[: self.n] = self.c

        slackTableau = Tableau(ASlack, self.b.copy(), cSlack, self.isMinimization)
        slackTableau.basis = np.array([self.n + i for i in range(self.m)], dtype=int)
        return slackTableau

    def display(self):
        header = ["Var"] + [f"x{i + 1}" for i in range(self.n)] + ["RHS"]
        print("\t".join(header))
        for i in range(self.m):
            row = [f"C{i + 1}"] + [f"{self.A[i][j]:.6f}" for j in range(self.n)] + [f"{self.b[i]:.6f}"]
            print("\t".join(row))
        obj = ["Obj"] + [f"{self.c[j]:.6f}" for j in range(self.n)] + [f"{self.bestObjective:.6f}"]
        print("\t".join(obj))
        if len(self.basis) == self.m:
            self.getSolution()
            self.displaySolution()
        print()


def run_exercises(show_logs=True):
    print("Exercise 1")
    t1 = Tableau.ex1()
    t1.DISPLAY_SIMPLEX_LOGS = show_logs
    t1.addSlackAndSolve()
    t1.displaySolution()
    print()

    print("Exercise 2")
    t2 = Tableau.ex2()
    t2.basis = np.array([0, 2, 5], dtype=int)
    t2.DISPLAY_SIMPLEX_LOGS = show_logs
    t2.applySimplex()
    t2.getSolution()
    t2.displaySolution()


if __name__ == "__main__":
    run_exercises(show_logs=True)
