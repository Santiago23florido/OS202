import graph
import warshall

nodes = ["D", "a1", "a2", "c1", "c2", "d1", "d2", "b1", "b2", "g1", "g2", "e1", "e2", "f1", "f2", "h1", "h2", "i1", "i2", "F"]

g = graph.Graph(nodes)
has_arc = [[False] * g.n for _ in range(g.n)]

arcs = [
    ("a1", "a2", 4),
    ("b1", "b2", 6),
    ("c1", "c2", 4),
    ("d1", "d2", 12),
    ("e1", "e2", 24),
    ("f1", "f2", 10),
    ("g1", "g2", 7),
    ("h1", "h2", 10),
    ("i1", "i2", 3),
    ("D", "a1", 0),
    ("D", "c1", 0),
    ("D", "d1", 0),
    ("c2", "b1", 0),
    ("c2", "g1", 0),
    ("a2", "e1", 0),
    ("b2", "e1", 0),
    ("b2", "f1", 0),
    ("d2", "h1", 0),
    ("f2", "h1", 0),
    ("g2", "h1", 0),
    ("e2", "i1", 0),
    ("h2", "i1", 0),
    ("i2", "F", 0),
]

for u, v, w in arcs:
    g.addArc(u, v, w)
    has_arc[g.indexOf(u)][g.indexOf(v)] = True

dist, pred = warshall.warshall(g, has_arc=has_arc,max=True)
warshall.print_dist_matrix("Distances", g, dist)
warshall.print_pred_matrix("Predecesseurs", g, pred)
