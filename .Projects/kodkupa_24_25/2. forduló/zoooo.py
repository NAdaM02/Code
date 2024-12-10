from collections import deque, defaultdict

def bfs_distances(start, graph, n):
    """Performs BFS to calculate shortest distances from the start node."""
    distances = [-1] * n
    queue = deque([start])
    distances[start] = 0
    while queue:
        node = queue.popleft()
        for neighbor in graph[node]:
            if distances[neighbor] == -1:  # Not visited
                distances[neighbor] = distances[node] + 1
                queue.append(neighbor)
    return distances

def count_stable_edges(N, edges):
    # Build the graph
    graph = defaultdict(set)
    for u, v in edges:
        graph[u].add(v)
        graph[v].add(u)

    # BFS from 0 and N-1 to get distances
    dist_from_start = bfs_distances(0, graph, N)
    dist_from_end = bfs_distances(N - 1, graph, N)

    # Shortest path length from 0 to N-1
    shortest_path_length = dist_from_start[N - 1]

    if shortest_path_length == -1:
        # If no path exists, no edges can keep shortest path length stable
        return 0

    # Count valid edge additions
    count = 0
    for u in range(N):
        for v in range(u + 1, N):
            # Skip if edge already exists
            if v in graph[u]:
                continue

            # Calculate new shortest path via the added edge
            new_path_via_u = dist_from_start[u] + 1 + dist_from_end[v]
            new_path_via_v = dist_from_start[v] + 1 + dist_from_end[u]

            # Check if the shortest path length remains unchanged
            if min(new_path_via_u, new_path_via_v) >= shortest_path_length:
                count += 1

    return count

# Input reading
N, num_edges = map(int, input().split())
edges = [tuple(map(int, input().split())) for _ in range(num_edges)]

# Compute and print the result
print(count_stable_edges(N, edges))