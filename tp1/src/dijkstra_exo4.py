import numpy as np
import graph
from dijkstra import dijkstra


def build_graph_left():
    # Nodes: r, a, b, c, d, e, f, g
    g = graph.Graph(np.array(["r", "a", "b", "c", "d", "e", "f", "g"]))

    g.addArc("r", "a", 5)
    g.addArc("r", "b", 4)

    g.addArc("b", "a", 5)
    g.addArc("a", "c", 3)
    g.addArc("b", "c", 3)
    g.addArc("b", "g", 9)

    g.addArc("c", "d", 2)
    g.addArc("d", "a", 8)
    g.addArc("d", "e", 2)
    g.addArc("e", "c", 4)

    g.addArc("c", "f", 6)
    g.addArc("c", "g", 8)
    g.addArc("g", "f", 5)

    return g


def build_graph_right():
    # Nodes: r, A, B, C, D, E, F, G
    g = graph.Graph(np.array(["r", "A", "B", "C", "D", "E", "F", "G"]))

    g.addArc("r", "A", 2)
    g.addArc("r", "G", 3)

    g.addArc("A", "B", 3)
    g.addArc("A", "F", 1)

    g.addArc("B", "C", 2)
    g.addArc("D", "C", 2)

    g.addArc("F", "D", 4)
    g.addArc("F", "G", 3)

    g.addArc("G", "E", 2)
    g.addArc("E", "F", 2)
    g.addArc("E", "D", 3)

    return g


def main():
    graphs = [
        ("Left graph", build_graph_left(), "r"),
        ("Right graph", build_graph_right(), "r"),
    ]

    for name, g, origin in graphs:
        tree = dijkstra(g, origin)
        print(f"{name} - shortest path tree from {origin}:")
        print(tree)


if __name__ == "__main__":
    main()
