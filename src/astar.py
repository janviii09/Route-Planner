import heapq
import math

def heuristic(node1, node2):
    # Euclidean distance heuristic
    return math.sqrt((node1.x - node2.x)**2 + (node1.y - node2.y)**2)

def astar(graph, start, end):
    end_node = graph.get_node(end)
    
    # Priority queue stores (f_score, g_score, node_id)
    pq = [(0, 0, start)]
    
    # g_score: distance from start
    g_scores = {node: float('inf') for node in graph.nodes}
    g_scores[start] = 0
    
    # f_score: g_score + heuristic
    f_scores = {node: float('inf') for node in graph.nodes}
    start_node = graph.get_node(start)
    f_scores[start] = heuristic(start_node, end_node)
    
    previous = {node: None for node in graph.nodes}
    
    while pq:
        _, current_g, current_node_id = heapq.heappop(pq)
        
        if current_node_id == end:
            break
            
        if current_g > g_scores[current_node_id]:
            continue
            
        for neighbor_id, weight in graph.adj[current_node_id]:
            tentative_g = current_g + weight
            
            if tentative_g < g_scores[neighbor_id]:
                previous[neighbor_id] = current_node_id
                g_scores[neighbor_id] = tentative_g
                neighbor_node = graph.get_node(neighbor_id)
                f_scores[neighbor_id] = tentative_g + heuristic(neighbor_node, end_node)
                
                heapq.heappush(pq, (f_scores[neighbor_id], tentative_g, neighbor_id))
                
    # Reconstruct path
    path = []
    curr = end
    if g_scores[end] != float('inf'):
        while curr is not None:
            path.append(curr)
            curr = previous[curr]
        path.reverse()
        
    return path, g_scores[end] if g_scores[end] != float('inf') else -1
