from .dsu import DSU

def kruskal(graph):
    mst_edges = []
    
    # Filter to unique undirected edges to avoid processing (u,v) and (v,u)
    unique_edges = []
    seen = set()
    # Sort all edges by weight
    sorted_edges = sorted(graph.edges, key=lambda e: e.weight)
    
    for e in sorted_edges:
        pair = tuple(sorted([e.u, e.v]))
        if pair not in seen:
            seen.add(pair)
            unique_edges.append(e)
            
    # Initialize DSU
    dsu = DSU(graph.nodes.keys())
    
    total_weight = 0
    full_cost = sum(e.weight for e in unique_edges)
    trace = []
    
    for edge in unique_edges:
        would_cycle = dsu.connected(edge.u, edge.v)
        
        if not would_cycle:
            dsu.union(edge.u, edge.v)
            mst_edges.append(edge)
            total_weight += edge.weight
            trace.append({
                "u": edge.u, "v": edge.v, "weight": edge.weight,
                "status": "accepted"
            })
        else:
            trace.append({
                "u": edge.u, "v": edge.v, "weight": edge.weight,
                "status": "rejected"
            })
            
    return mst_edges, total_weight, full_cost, trace
