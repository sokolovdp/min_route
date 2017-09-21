import networkx as nx
import matplotlib.pyplot as plt


def node_name(x, y):
    return "{}-{}".format(x, y)


def build_graph(regions_data: "list") -> "nx.Graph":
    graph = nx.Graph()
    n = len(regions_data)
    m = len(regions_data[0])

    for i in range(n):
        for j in range(m):
            center_node = node_name(i, j)
            graph.add_node(center_node, alarm=regions_data[i][j])
            if j > 0:
                left_node = node_name(i, j - 1)
                weight = regions_data[i][j - 1]
                graph.add_node(left_node, alarm=weight)
                graph.add_edge(center_node, left_node, weight=weight)
            if j < m - 1:
                right_node = node_name(i, j + 1)
                weight = regions_data[i][j + 1]
                graph.add_node(right_node, alarm=weight)
                graph.add_edge(center_node, right_node, weight=weight)
            if i > 0:
                up_node = node_name(i - 1, j)
                weight = regions_data[i - 1][j]
                graph.add_node(up_node, alarm=weight)
                graph.add_edge(center_node, up_node, weight=weight)
            if i < n - 1:
                down_node = node_name(i + 1, j)
                weight = regions_data[i + 1][j]
                graph.add_node(down_node, alarm=weight)
                graph.add_edge(center_node, down_node, weight=weight)

    return nx.freeze(graph)


test_data = [
    [2, 100, 0, 100, 100],
    [1, 100, 0, 0, 0],
    [1, 0, 3, 100, 2]
]
start_node = (0, 0)
end_node = (2, 4)


def main():
    graph = build_graph(test_data)

    thick_edges = [(u, v) for (u, v, attrb) in graph.edges(data=True) if attrb['weight'] > 10]
    thin_edges = [(u, v) for (u, v, attrb) in graph.edges(data=True) if attrb['weight'] <= 10]

    large_nodes = [node for node, attrb in graph.nodes(data=True) if attrb['alarm'] > 10]
    small_nodes = [node for node, attrb in graph.nodes(data=True) if attrb['alarm'] <= 10]

    pos = nx.spring_layout(graph)  # positions for all nodes

    # nodes
    nx.draw_networkx_nodes(graph, pos, nodelist=large_nodes, node_size=1600, node_color='r')
    nx.draw_networkx_nodes(graph, pos, nodelist=small_nodes, node_size=800, node_color='b')

    # edges
    nx.draw_networkx_edges(graph, pos, edgelist=thick_edges, width=6, edge_color='r')
    nx.draw_networkx_edges(graph, pos, edgelist=thin_edges, width=3, edge_color='b')

    # labels
    nx.draw_networkx_labels(graph, pos, font_size=10, font_family='sans-serif')

    print("shortest path:", nx.shortest_path(graph, source=node_name(0, 0), target=node_name(2, 4), weight='weight'))

    plt.axis('off')
    plt.savefig("weighted_graph.png")  # save as png
    plt.show()  # display


if __name__ == "__main__":
    main()
