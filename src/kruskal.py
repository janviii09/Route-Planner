from .dsu import DSU

def kruskal(graph):
    mst_edges = []
    # Sort all edges by weight
    # Because we made bidirectional edges, we might have duplicates like (u,v) and (v,u).
    # We can handle this by only considering unique edges or just letting DSU handle it.
    sorted_edges = sorted(graph.edges, key=lambda e: e.weight)
    
    # Initialize DSU
    dsu = DSU(graph.nodes.keys())
    
    total_weight = 0
    
    for edge in sorted_edges:
        # If adding this edge doesn't cause a cycle
        if dsu.union(edge.u, edge.v):
            mst_edges.append(edge)
            total_weight += edge.weight
            
    return mst_edges, total_weight
