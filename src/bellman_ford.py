def bellman_ford(graph, start, end):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    previous = {node: None for node in graph.nodes}
    
    # Relax all edges V-1 times
    V = len(graph.nodes)
    for _ in range(V - 1):
        for edge in graph.edges:
            if distances[edge.u] != float('inf') and distances[edge.u] + edge.weight < distances[edge.v]:
                distances[edge.v] = distances[edge.u] + edge.weight
                previous[edge.v] = edge.u
                
    # Check for negative weight cycles
    for edge in graph.edges:
        if distances[edge.u] != float('inf') and distances[edge.u] + edge.weight < distances[edge.v]:
            print("Graph contains negative weight cycle")
            return [], -1
            
    # Reconstruct path
    path = []
    curr = end
    if distances[end] != float('inf'):
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()
        
    return path, distances[end] if distances[end] != float('inf') else -1
