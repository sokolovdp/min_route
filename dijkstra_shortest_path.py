# github.com/zaz/dijkstra
from collections import defaultdict

INFINIT = 1e309


class Digraph(object):
    def __init__(self):
        self.nodes = set()
        self.neighbours = defaultdict(set)
        self.dist = {}

    def add_node(self, *nodes):
        [self.nodes.add(n) for n in nodes]

    def add_edge(self, frm, to, d=INFINIT):
        self.add_node(frm, to)
        self.neighbours[frm].add(to)
        self.dist[frm, to] = d

    def dijkstra(self, start, max_d=INFINIT):
        """Returns a map of nodes to distance from start and a map of nodes to
        the neighbouring node that is closest to start."""
        # total distance from origin
        tdist = defaultdict(lambda: INFINIT)
        tdist[start] = 0
        # neighbour that is nearest to the origin
        preceding_node = {}
        unvisited = self.nodes.copy()  # unvisited = self.nodes

        while unvisited:
            current = unvisited.intersection(tdist.keys())
            if not current:
                break
            min_node = min(current, key=tdist.get)
            unvisited.remove(min_node)

            for neighbour in self.neighbours[min_node]:
                d = tdist[min_node] + self.dist[min_node, neighbour]
                if tdist[neighbour] > d and max_d >= d:
                    tdist[neighbour] = d
                    preceding_node[neighbour] = min_node

        return tdist, preceding_node

    def min_path(self, start, end, max_d=INFINIT):
        """Returns the minimum distance and path from start to end."""
        tdist, preceding_node = self.dijkstra(start, max_d)
        dist = tdist[end]
        backpath = [end]
        try:
            while end != start:
                end = preceding_node[end]
                backpath.append(end)
            path = list(reversed(backpath))
        except KeyError:
            path = None

        return dist, path

    def dist_to(self, *args):
        return self.min_path(*args)[0]

    def path_to(self, *args):
        return self.min_path(*args)[1]


# Мой код

def create_graph_with_distances(_graph: "Digraph", distance_data: "list") -> "Digraph":
    n = len(distance_data)
    m = len(distance_data[0])

    for i in range(n):
        for j in range(m):
            center_node = (i, j)
            if j > 0:
                left_node = (i, j - 1)
                left_distance = distance_data[i][j - 1]
                _graph.add_edge(center_node, left_node, left_distance)
            if j < m - 1:
                right_node = (i, j + 1)
                right_distance = distance_data[i][j + 1]
                _graph.add_edge(center_node, right_node, right_distance)
            if i > 0:
                up_node = (i - 1, j)
                up_distance = distance_data[i - 1][j]
                _graph.add_edge(center_node, up_node, up_distance)
            if i < n - 1:
                down_node = (i + 1, j)
                down_distance = distance_data[i + 1][j]
                _graph.add_edge(center_node, down_node, down_distance)
    return _graph


test_data = [
    [2, 100, 0, 100, 100],
    [1, 100, 0, 0, 0],
    [1, 0, 3, 100, 2]
]
start_node = (0, 0)
end_node = (2, 4)


def main():
    graph = create_graph_with_distances(Digraph(), test_data)
    print(graph.min_path(start_node, end_node))


if __name__ == "__main__":
    main()
