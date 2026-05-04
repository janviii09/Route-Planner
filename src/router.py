from .dsu import DSU
from .bfs import bfs
from .bellman_ford import bellman_ford
from .astar import astar
from .dijkstra import dijkstra

class Router:
    def __init__(self, graph):
        self.graph = graph
        self.dsu = DSU(graph.nodes.keys())
        
        # Precompute connected components
        for edge in graph.edges:
            self.dsu.union(edge.u, edge.v)

    def find_route(self, src, dest, emergency_mode=False, has_negative_weights=False, has_heuristic=False):
        """
        The core decision logic.
        """
        # Step 1: DSU check
        if not self.dsu.connected(src, dest):
            return {"algorithm": "None", "path": [], "cost": -1, "reason": "No path exists between source and destination."}
            
        # Step 2: Emergency mode check
        if emergency_mode:
            path, cost = bfs(self.graph, src, dest)
            return {"algorithm": "BFS", "path": path, "cost": cost}
            
        # Step 3: Negative weights check
        if has_negative_weights:
            path, cost = bellman_ford(self.graph, src, dest)
            return {"algorithm": "Bellman-Ford", "path": path, "cost": cost}
            
        # Step 4: Grid / Geo-coordinate (Heuristic) check
        if has_heuristic:
            path, cost = astar(self.graph, src, dest)
            return {"algorithm": "A*", "path": path, "cost": cost}
            
        # Step 5: Default to Dijkstra + Min-Heap
        path, cost = dijkstra(self.graph, src, dest)
        return {"algorithm": "Dijkstra", "path": path, "cost": cost}
