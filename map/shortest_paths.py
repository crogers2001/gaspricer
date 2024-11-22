import numpy as np

def build_adj_matrix(roadways, intersections):
    intersection_indices = intersections
    reverse_intersections = {v: k for k, v in intersections.items()}
    num_intersections = len(intersections)

    adj_matrix = np.empty((num_intersections, num_intersections), dtype=object)

    for i in range(num_intersections):
        for j in range(num_intersections):
            if i == j:
                adj_matrix[i][j] = (0, [reverse_intersections[i]])
            else:
                adj_matrix[i][j] = (np.inf, [])

    intersection_cost = 1

    for start, end in roadways:
        x0, y0 = start
        x1, y1 = end
        roadway_length = abs(x0 - x1) + abs(y0 - y1)
        i = intersection_indices[start]
        j = intersection_indices[end]
        distance = roadway_length + intersection_cost
        adj_matrix[i][j] = (distance, [reverse_intersections[i], reverse_intersections[j]])
        adj_matrix[j][i] = (distance, [reverse_intersections[j], reverse_intersections[i]])

    return adj_matrix

def floyd_warshall(matrix):
    num_vertices = len(matrix)

    for k in range(num_vertices):
        for i in range(num_vertices):
            for j in range(num_vertices):
                current_distance, current_path = matrix[i][j]
                new_distance = matrix[i][k][0] + matrix[k][j][0]
                if new_distance < current_distance:
                    new_path = matrix[i][k][1] + matrix[k][j][1][1:]
                    matrix[i][j] = (new_distance, new_path)
    return matrix

def get_shortest_paths(roadways, intersections):
    """
    Expects: list of roadway coordinates tuples and intersection coordinates dictionary, 
    Returns: 2D array of shortest path costs between each intersection as well as the path taken to get there.

    Example of using shortest_paths 2D Matrix: 
        print(shortest_paths[0][12])
        => (16, [(0, 6), (2, 6), (5, 6), (5, 3), (5, 1), (5, 0)])   # tuple of path cost, visited intersections
        print(shortest_paths[0][12][0])
        => 16                                                       # path cost
        print(shortest_paths[0][12][1])
        => [(0, 6), (2, 6), (5, 6), (5, 3), (5, 1), (5, 0)]         # visited intersections

    Important notes:
        -Moving from current coordinate to a roadway coordinate costs 1
        -Moving from current coordinate to an intersection coordinate costs 2
    """
    adj_matrix = build_adj_matrix(roadways, intersections)
    shortest_paths = floyd_warshall(adj_matrix)
    return shortest_paths



intersections = {(0, 6): 0, (2, 6): 1, (5, 6): 2, (0, 3): 3, (2, 3): 4, (5, 3): 5, (0, 2): 6, (0, 1): 7, (5, 1): 8, (0, 0): 9, (2, 0): 10, (3, 0): 11, (5, 0): 12}
roadways = [((0,6), (2,6)), ((2,6), (5,6)), ((0,6), (0,3)), ((2,6), (2,3)), ((5,6), (5,3)), ((0,3), (2,3)), ((2,3), (5,3)), ((0,3), (0,2)), ((0,2), (0,1)), ((0,1), (0,0)), ((5,3), (5,1)), ((5,1), (5,0)), ((0,0), (2,0)), ((2,0), (3,0)), ((3,0), (5,0))] 

shortest_paths = get_shortest_paths(roadways, intersections)

print(shortest_paths[0][12])
print(shortest_paths[0][12][0])
print(shortest_paths[0][12][1])
# Display results
# for i, row in enumerate(shortest_paths):
#     for j, (distance, path) in enumerate(row):
#         print(f"Shortest path from {list(intersections.keys())[i]} to {list(intersections.keys())[j]}: Distance = {distance}, Path = {path}")