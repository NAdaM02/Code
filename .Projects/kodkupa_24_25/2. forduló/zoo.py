import sys

def bfs(start, end, graph):
    queue = [(start, 0)]
    visited = {start}
    while queue:
        node, dist = queue.pop(0)
        if node == end:
            return dist
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return float('inf')

links_table = {}

N, num_edges = map(int, input().split())

for _ in range(num_edges):
    u, v = map(int, input().split())
    links_table.setdefault(u, []).append(v)
    links_table.setdefault(v, []).append(u)

shortest_path_length = bfs(0, N-1, links_table)
count = 0

for u in range(N):
    for v in range(u + 1, N):
        if v in links_table.get(u, []) or u in links_table.get(v, []):
            continue

        temp_graph = {node: neighbors[:] for node, neighbors in links_table.items()}
        temp_graph.setdefault(u, []).append(v)
        temp_graph.setdefault(v, []).append(u)

        new_shortest_path_length = bfs(0, N - 1, temp_graph)

        if new_shortest_path_length == shortest_path_length:
            count += 1

print(count)

sys.stdout.close()
