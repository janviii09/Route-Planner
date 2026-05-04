from collections import deque

def bfs(graph, start, end):
    # Unweighted emergency routing
    queue = deque([start])
    visited = {start}
    previous = {node: None for node in graph.nodes}
    
    while queue:
        current_node = queue.popleft()
        
        if current_node == end:
            break
            
        for neighbor, _ in graph.adj[current_node]:
            if neighbor not in visited:
                visited.add(neighbor)
                previous[neighbor] = current_node
                queue.append(neighbor)
                
    # Reconstruct path
    path = []
    curr = end
    if curr in visited:
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()
        
    # In BFS weight is just step count, so length of path - 1
    return path, len(path) - 1 if path else -1
