import networkx as nx
import matplotlib.pyplot as plt
from collections import namedtuple

Coordinates = namedtuple('Coordinates', ['y', 'x'])


def create_node_name(x, y):
    return "{}-{}".format(x, y)


def create_node(graph: "nx.Graph", position: "Coordinates", w_table: "list"):
    node_name = create_node_name(*position)
    graph.add_node(node_name, {'alarm': w_table[position.y][position.x], 'pos': (position.x, position.y)})
    return node_name


def build_graph(regions_data: "list") -> "nx.Graph":
    graph = nx.Graph()
    n = len(regions_data)
    m = len(regions_data[0])

    for i in range(n):
        for j in range(m):
            center_node = create_node(graph, Coordinates(i, j), regions_data)
            if j > 0:
                left_position = Coordinates(i, j - 1)
                left_node = create_node(graph, left_position, regions_data)
                graph.add_edge(center_node, left_node, weight=regions_data[left_position.y][left_position.x])
            if j < m - 1:
                right_position = Coordinates(i, j + 1)
                right_node = create_node(graph, right_position, regions_data)
                graph.add_edge(center_node, right_node, weight=regions_data[right_position.y][right_position.x])
            if i > 0:
                up_position = Coordinates(i - 1, j)
                up_node = create_node(graph, up_position, regions_data)
                graph.add_edge(center_node, up_node, weight=regions_data[up_position.y][up_position.x])
            if i < n - 1:
                down_position = Coordinates(i + 1, j)
                down_node = create_node(graph, down_position, regions_data)
                graph.add_edge(center_node, down_node, weight=regions_data[down_position.y][down_position.x])
    return nx.freeze(graph)


test_data = [
    [2, 100, 0, 100, 100],
    [1, 100, 0, 0, 0],
    [1, 0, 3, 100, 2]
]
start_node = create_node_name(0, 0)
end_node = create_node_name(2, 4)


def main():
    graph = build_graph(test_data)

    large_nodes = [node for node, attrb in graph.nodes(data=True) if attrb['alarm'] > 10]
    small_nodes = [node for node, attrb in graph.nodes(data=True) if attrb['alarm'] <= 10]
    nodes_in_shortest_path = nx.shortest_path(graph, source=start_node, target=end_node, weight='weight')

    thick_edges = [(u, v) for (u, v, attrb) in graph.edges(data=True) if attrb['weight'] > 10]
    thin_edges = [(u, v) for (u, v, attrb) in graph.edges(data=True) if attrb['weight'] <= 10]
    edges_in_shortest_path = list(zip(nodes_in_shortest_path[1:], nodes_in_shortest_path[:-1]))

    pos = nx.get_node_attributes(graph, 'pos')

    print(pos)

    nx.draw(graph, pos=pos)

    # pos = nx.circular_layout(graph)  # positions for all nodes
    # print(pos)

    # nodes
    nx.draw_networkx_nodes(graph, pos, nodelist=large_nodes, node_size=2000, node_color='r')
    nx.draw_networkx_nodes(graph, pos, nodelist=small_nodes, node_size=1000, node_color='y')
    nx.draw_networkx_nodes(graph, pos, nodelist=nodes_in_shortest_path, node_size=600, node_color='b')

    # edges
    nx.draw_networkx_edges(graph, pos, edgelist=thick_edges, width=10, edge_color='r')
    nx.draw_networkx_edges(graph, pos, edgelist=thin_edges, width=5, edge_color='y')
    nx.draw_networkx_edges(graph, pos, edgelist=edges_in_shortest_path, width=2, edge_color='b')

    # labels
    nx.draw_networkx_labels(graph, pos, font_size=10, font_family='sans-serif')

    plt.axis('off')
    plt.savefig("weighted_graph.png")  # save as png
    plt.show()  # display


if __name__ == "__main__":
    main()
