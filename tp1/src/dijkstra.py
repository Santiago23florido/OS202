import graph
import sys

def main():
    cities = []
    cities.append("Paris")
    cities.append("Hambourg")
    cities.append("Londres")
    cities.append("Amsterdam")
    cities.append("Edimbourg")
    cities.append("Berlin")
    cities.append("Stockholm")
    cities.append("Rana")
    cities.append("Oslo")

    g = graph.Graph(cities)
    
    g.addArc("Paris", "Hambourg", 7)
    g.addArc("Paris",  "Londres", 4)
    g.addArc("Paris",  "Amsterdam", 3)
    g.addArc("Hambourg",  "Stockholm", 1)
    g.addArc("Hambourg",  "Berlin", 1)
    g.addArc("Londres",  "Edimbourg", 2)
    g.addArc("Amsterdam",  "Hambourg", 2)
    g.addArc("Amsterdam",  "Oslo", 8)
    g.addArc("Stockholm",  "Oslo", 2)
    g.addArc("Stockholm",  "Rana", 5)
    g.addArc("Berlin",  "Amsterdam", 2)
    g.addArc("Berlin",  "Stockholm", 1)
    g.addArc("Berlin",  "Oslo", 3)
    g.addArc("Edimbourg",  "Oslo", 7)
    g.addArc("Edimbourg",  "Amsterdam", 3)
    g.addArc("Edimbourg",  "Rana", 6)
    g.addArc("Oslo",  "Rana", 2)
    
    # Applique l'algorithme de Dijkstra pour obtenir une arborescence
    tree = dijkstra(g, "Paris")
    print(tree)

def dijkstra(g, origin):
        
    r = g.indexOf(origin)



    pred = [0] * g.n
    pi = [sys.float_info.max] * g.n
    pi[r] = 0
    source = r
    for i in range(g.n-1):
        for v, w in enumerate(g.adjacency[r]):
            if w != 0:  # hay arco r -> v
                if pi[r] + w < pi[v]:
                    pi[v] = pi[r] + w
                    pred[v] = r

        r = sorted(range(len(pi)), key=lambda k: pi[k])[i]

    tree = graph.Graph(g.nodes)
    for v in range(g.n):
        if v != source and pred[v] is not None:
            u = pred[v]
            tree.addArcByIndex(u, v, g.adjacency[u][v])

    return tree
   
if __name__ == '__main__':
    main()
