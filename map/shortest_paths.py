import numpy as np

def build_adj_matrix(roadways, intersections):

    intersection_indices = {coord: index for index, coord in enumerate(intersections)}

    num_intersections = len(intersections)
    adj_matrix = np.full((num_intersections, num_intersections), np.inf)

    for i in range(len(intersections)):
        adj_matrix[i][i] = 0

    intersection_cost = 1

    for start, end in roadways:
        x0, y0 = start
        x1, y1 = end 
        roadway_length = abs(x0 - x1) + abs(y0 - y1)
        i = intersection_indices[start]
        j = intersection_indices[end]
        adj_matrix[i][j] = roadway_length + intersection_cost
        adj_matrix[j][i] = roadway_length + intersection_cost

    return adj_matrix

def floyd_warshall(matrix):
    num_vertices = len(matrix)
    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                matrix[i][j] = min(matrix[i][j], matrix[i][k] + matrix[k][j])
    return matrix

def get_adjacency_matrix(roadways, intersections):
    """
    Expects: list of roadway coordinates tuples and intersection coordinates, 
    Returns: 2D array of shortest path costs between each intersection
    """
    adj_matrix = build_adj_matrix(roadways, intersections)
    shortest_paths = floyd_warshall(adj_matrix)
    return shortest_paths