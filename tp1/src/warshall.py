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
    
    dist, pred = warshall(g)
    print_dist_matrix("Distances", g, dist)
    print_pred_matrix("Predecesseurs", g, pred)

def warshall(g, max=False, has_arc=None):
    n = g.n
    inf = sys.float_info.max
    neg_inf = -sys.float_info.max
    maximize = max
    fill = neg_inf if maximize else inf
    dist = [[fill] * n for _ in range(n)]
    pred = [[None] * n for _ in range(n)]

    for i in range(n):
        dist[i][i] = 0

    for i in range(n):
        for j in range(n):
            w = g.adjacency[i][j]
            if has_arc is not None:
                if has_arc[i][j]:
                    dist[i][j] = w
                    pred[i][j] = i
            else:
                if w != 0:
                    dist[i][j] = w
                    pred[i][j] = i

    for k in range(n):
        for i in range(n):
            if maximize:
                if dist[i][k] == neg_inf:
                    continue
            else:
                if dist[i][k] == inf:
                    continue
            for j in range(n):
                if maximize:
                    if dist[k][j] == neg_inf:
                        continue
                else:
                    if dist[k][j] == inf:
                        continue
                nd = dist[i][k] + dist[k][j]
                if maximize:
                    if nd > dist[i][j]:
                        dist[i][j] = nd
                        pred[i][j] = pred[k][j]
                else:
                    if nd < dist[i][j]:
                        dist[i][j] = nd
                        pred[i][j] = pred[k][j]

    return dist, pred

def print_dist_matrix(title, g, mat):
    print(title)
    header = " " * 12 + " ".join([f"{name:>10}" for name in g.nodes])
    print(header)
    for i, row in enumerate(mat):
        formatted = []
        for val in row:
            if val == sys.float_info.max:
                formatted.append(f"{'inf':>10}")
            elif val == -sys.float_info.max:
                formatted.append(f"{'-inf':>10}")
            else:
                formatted.append(f"{val:>10}")
        print(f"{g.nodes[i]:>10} " + " ".join(formatted))
    print()

def print_pred_matrix(title, g, mat):
    print(title)
    header = " " * 12 + " ".join([f"{name:>10}" for name in g.nodes])
    print(header)
    for i, row in enumerate(mat):
        formatted = []
        for val in row:
            if val is None:
                formatted.append(f"{'-':>10}")
            else:
                formatted.append(f"{g.nodes[val]:>10}")
        print(f"{g.nodes[i]:>10} " + " ".join(formatted))
    print()
   
if __name__ == '__main__':
    main()
