# Floyd - Warshall shortest route algorithm
import numpy as np

MAXIMAL = 10000
MINIMAL = -1


def create_adjacency_matrix(distance_data: "list") -> "np.ndarray":
    n = len(distance_data)
    m = len(distance_data[0])
    matrix_size = n * m
    adjacency_matrix = np.full((matrix_size, matrix_size), 0, int)

    for i in range(n):
        for j in range(m):
            central_node_number = i * m + j
            if j > 0:
                left_node_number = central_node_number - 1
                left_distance = distance_data[i][j - 1]
                adjacency_matrix[central_node_number, left_node_number] = left_distance

            if j < m - 1:
                right_node_number = central_node_number + 1
                right_distance = distance_data[i][j + 1]
                adjacency_matrix[central_node_number, right_node_number] = right_distance

            if i > 0:
                up_node_number = central_node_number - m
                up_distance = distance_data[i - 1][j]
                adjacency_matrix[central_node_number, up_node_number] = up_distance

            if i < n - 1:
                down_node_number = central_node_number + m
                down_distance = distance_data[i + 1][j]
                adjacency_matrix[central_node_number, down_node_number] = down_distance

    return adjacency_matrix


def create_path_matrix(adjacency_matrix: "np.ndarray") -> "np.ndarray":
    matrix_size = len(adjacency_matrix)
    path_matrix = np.zeros(adjacency_matrix.shape, int)

    # initialize
    for i in range(matrix_size):
        for j in range(matrix_size):
            path_matrix[i, j] = i
            if i != j and (adjacency_matrix[i, j] == 0):
                path_matrix[i, j] = MINIMAL
                adjacency_matrix[i, j] = MAXIMAL
    # build
    for k in range(matrix_size):
        for i in range(matrix_size):
            for j in range(matrix_size):
                if adjacency_matrix[i, j] > adjacency_matrix[i, k] + adjacency_matrix[k, j]:
                    adjacency_matrix[i, j] = adjacency_matrix[i, k] + adjacency_matrix[k, j]
                    path_matrix[i, j] = path_matrix[k, j]

    return path_matrix


def build_path(p, start_node, end_node):
    if start_node == end_node:
        print(start_node, )
    elif p[start_node, end_node] == MINIMAL:
        print(start_node, '-', end_node)  # node are not connected
    else:
        build_path(p, start_node, p[start_node, end_node])
        print(end_node, )


test_data_2 = [
    [3, 101, 1, 101, 101],
    [2, 101, 1, 1, 1],
    [2, 1, 4, 101, 3]
]

from_node = 0
to_node = 14


def main():
    a_matrix = create_adjacency_matrix(test_data_2)
    p_matrix = create_path_matrix(a_matrix)

    print(a_matrix)
    print(p_matrix)

    build_path(p_matrix, from_node, to_node)


if __name__ == "__main__":
    main()
