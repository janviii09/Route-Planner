import heapq

def dijkstra(graph, start, end):
    # Min-Heap for priority queue
    pq = [(0, start)]
    distances = {node: float('inf') for node in graph.nodes}
    distances[start] = 0
    previous = {node: None for node in graph.nodes}
    
    while pq:
        current_distance, current_node = heapq.heappop(pq)
        
        # We found the shortest path to end
        if current_node == end:
            break
            
        # Optimization: if we find a longer path, ignore it
        if current_distance > distances[current_node]:
            continue
            
        for neighbor, weight in graph.adj[current_node]:
            distance = current_distance + weight
            
            # Only consider this new path if it's better
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(pq, (distance, neighbor))
                
    # Reconstruct path
    path = []
    curr = end
    if distances[end] != float('inf'):
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()
        
    return path, distances[end] if distances[end] != float('inf') else -1
