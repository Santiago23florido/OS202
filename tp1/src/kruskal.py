import numpy as np
import graph
import sys

def main():
    
    # Créer un graphe contenant les sommets a, b, c, d, e, f, g 
    g = graph.Graph(np.array(["a", "b", "c", "d", "e", "f", "g"]))

    # Ajouter les arêtes
    g.addEdge("a", "b",  1.0)
    g.addEdge("a", "c",  3.0)
    g.addEdge("b", "c",  2.0)
    g.addEdge("b", "d",  5.0)
    g.addEdge("b", "e",  7.0)
    g.addEdge("b", "f",  9.0)
    g.addEdge("c", "d",  4.0)
    g.addEdge("d", "e",  6.0)
    g.addEdge("d", "g", 12.0)
    g.addEdge("e", "f",  8.0)
    g.addEdge("e", "g", 11.0)
    g.addEdge("f", "g", 10.0)
    
    # Obtenir un arbre couvrant de poids minimal du graphe
    tree = kruskal(g)
    tree2 = kruskalCC(g)
    # S'il existe un tel arbre (i.e., si le graphe est connexe)
    if tree != None:
        
        # L'afficher
        print(tree)
        print(tree2)
    
    else:
        print("Pas d'arbre couvrant")

# Applique l'algorithme de Kruskal pour trouver un arbre couvrant de poids minimal d'un graphe
# Retourne: Un arbre couvrant de poids minimal du graphe ou None s'il n'en existe pas
def kruskal(g,max=False):
    # Nuevo grafo con los mismos nodos
    tree = graph.Graph(g.nodes)

    addedEdges = 0

    edges = g.getEdges()
    edges.sort(reverse=max)  # usa Edge.__lt__

    for e in edges:
        if not tree.createACycle(e):
            tree.addCopyOfEdge(e)
            addedEdges += 1

            # si ya tenemos n-1 aristas, terminamos
            if addedEdges == tree.n - 1:
                break

    # si no llegamos a n-1 aristas, el grafo no era conexo
    if addedEdges != tree.n - 1:
        return None

    return tree

def kruskalCC(g,max=False):
    tree = graph.Graph(g.nodes)

    edges = g.getEdges()
    edges.sort(reverse=max)

    n = tree.n
    addedEdges = 0

    comp = list(range(n))  

    for e in edges:
        u, v = e.id1, e.id2

        if comp[u] == comp[v]:
            continue  

        tree.addCopyOfEdge(e)
        addedEdges += 1

        old = comp[v]
        new = comp[u]
        for i in range(n):
            if comp[i] == old:
                comp[i] = new  

        if addedEdges == n - 1:
            break

    if addedEdges != n - 1:
        return None

    return tree

if __name__ == "__main__":
    main()
