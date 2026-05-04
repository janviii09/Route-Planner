import sys
from src.utils import load_graph
from src.router import Router
from src.kruskal import kruskal

try:
    from ui.canvas import draw_graph
    CANVAS_AVAILABLE = True
except ImportError:
    CANVAS_AVAILABLE = False
    print("Matplotlib not found. Visualization disabled.")

def run_cli():
    print("AI Route Planner CLI")
    graph = load_graph('data/city_graph.json', 'data/traffic_weights.json')
    router = Router(graph)
    
    while True:
        print("\nOptions:")
        print("1. Find Route")
        print("2. Find Minimum Spanning Tree (Kruskal)")
        print("3. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            src = input("Enter source node: ")
            dest = input("Enter destination node: ")
            
            if src not in graph.nodes or dest not in graph.nodes:
                print("Invalid nodes.")
                continue
                
            emergency = input("Emergency mode? (y/N): ").lower() == 'y'
            negative = input("Negative weights? (y/N): ").lower() == 'y'
            heuristic = input("Use spatial heuristic? (y/N): ").lower() == 'y'
            
            result = router.find_route(src, dest, emergency, negative, heuristic)
            print("\n--- Result ---")
            print(f"Algorithm used: {result['algorithm']}")
            print(f"Path: {' -> '.join(result['path']) if result['path'] else 'No Path'}")
            print(f"Total Cost: {result['cost']}")
            
            if CANVAS_AVAILABLE and result['path']:
                draw_graph(graph, path=result['path'])
            
        elif choice == '2':
            mst_edges, total_weight = kruskal(graph)
            print("\n--- Minimum Spanning Tree ---")
            print(f"Total Weight: {total_weight}")
            print("Edges:")
            for e in mst_edges:
                print(f"  {e.u} - {e.v} : {e.weight}")
                
            if CANVAS_AVAILABLE:
                draw_graph(graph, mst_edges=mst_edges)
                
        elif choice == '3':
            sys.exit(0)
            
if __name__ == "__main__":
    run_cli()
