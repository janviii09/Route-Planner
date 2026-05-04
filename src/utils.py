import json
from src.graph import Graph

def load_graph(graph_file, weights_file=None):
    graph = Graph()
    
    with open(graph_file, 'r') as f:
        data = json.load(f)
        
    for node_id, coords in data.get('nodes', {}).items():
        graph.add_node(node_id, coords['x'], coords['y'])
        
    for edge in data.get('edges', []):
        graph.add_edge(edge['u'], edge['v'], edge.get('weight', 1))
        
    if weights_file:
        try:
            with open(weights_file, 'r') as f:
                weights = json.load(f)
            for k, w in weights.items():
                u, v = k.split('-')
                graph.update_weight(u, v, w)
        except Exception as e:
            print(f"Could not load traffic weights: {e}")
            
    return graph
