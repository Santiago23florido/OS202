import numpy as np
import graph
from kruskal import kruskalCC


def build_graph_image_1():
    # Nodos: a, b, c, d, e, f, g, h
    g = graph.Graph(np.array(["a", "b", "c", "d", "e", "f", "g", "h"]))

    g.addEdge("a", "b", 9)
    g.addEdge("a", "f", 6)
    g.addEdge("a", "h", 9)

    g.addEdge("b", "c", 5)
    g.addEdge("b", "d", 8)
    g.addEdge("b", "e", 5)

    g.addEdge("c", "d", 2)
    g.addEdge("c", "g", 5)

    g.addEdge("d", "g", 8)
    g.addEdge("d", "h", 7)

    g.addEdge("e", "f", 1)
    g.addEdge("e", "g", 3)

    g.addEdge("g", "h", 5)

    return g


def build_graph_image_2():
    # Nodos: A, B, C, D, E, F
    g = graph.Graph(np.array(["A", "B", "C", "D", "E", "F"]))

    g.addEdge("A", "B", 4)
    g.addEdge("A", "C", 3)

    g.addEdge("B", "C", 5)
    g.addEdge("B", "F", 2)

    g.addEdge("C", "F", 5)
    g.addEdge("C", "D", 2)

    g.addEdge("D", "F", 3)
    g.addEdge("D", "E", 4)

    g.addEdge("F", "E", 3)

    return g


def main():
    graphs = [
        ("Imagen 1", build_graph_image_1()),
        ("Imagen 2", build_graph_image_2()),
    ]

    for name, g in graphs:
        tree = kruskalCC(g)
        tree2 = kruskalCC(g,max=True)
        if tree is None:
            print(f"{name}: no es conexo, no hay arbol cubriente")
            print()
            continue
        if tree2 is None:
            print(f"{name}: no es conexo, no hay arbol cubriente")
            print()
            continue
        print(f"{name}: MST con KruskalCC")
        print(tree)
        print(f"{name}: MAXT con KruskalCC")
        print(tree2)


if __name__ == "__main__":
    main()
