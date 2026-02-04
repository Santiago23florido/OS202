import numpy as np
import graph
import warshall

g = graph.Graph(np.array(["a", "c", "d", "b", "e"]))

g.addArc("a", "c", 4)
g.addArc("a", "d", 8)
g.addArc("d", "c", 4)
g.addArc("c", "d", 6)
g.addArc("c", "b", 3)
g.addArc("d", "b", 2)
g.addArc("b", "e", 2)
g.addArc("d", "e", 1)

dist, pred = warshall.warshall(g)
warshall.print_dist_matrix("Distances", g, dist)
warshall.print_pred_matrix("Predecesseurs", g, pred)
