import matplotlib.pyplot as plt

def draw_graph(graph, path=None, mst_edges=None):
    plt.figure(figsize=(10, 8))
    
    # Draw all edges
    for edge in graph.edges:
        u_node = graph.get_node(edge.u)
        v_node = graph.get_node(edge.v)
        
        # Color MST edges differently if provided
        color = 'gray'
        linewidth = 1
        
        if mst_edges:
            for mst_e in mst_edges:
                if (mst_e.u == edge.u and mst_e.v == edge.v) or (mst_e.u == edge.v and mst_e.v == edge.u):
                    color = 'green'
                    linewidth = 2
                    break
                    
        plt.plot([u_node.x, v_node.x], [u_node.y, v_node.y], color=color, linewidth=linewidth, zorder=1)
        
        # Add weight labels
        mid_x = (u_node.x + v_node.x) / 2
        mid_y = (u_node.y + v_node.y) / 2
        plt.text(mid_x, mid_y, str(edge.weight), color='blue', fontsize=10, zorder=3)
        
    # Draw path if provided
    if path:
        for i in range(len(path) - 1):
            u_node = graph.get_node(path[i])
            v_node = graph.get_node(path[i+1])
            plt.plot([u_node.x, v_node.x], [u_node.y, v_node.y], color='red', linewidth=3, zorder=2)
            
    # Draw nodes
    for node_id, node in graph.nodes.items():
        plt.scatter(node.x, node.y, s=300, color='lightblue', zorder=4)
        plt.text(node.x, node.y, node_id, fontsize=12, ha='center', va='center', zorder=5)
        
    plt.title("AI Route Planner")
    plt.axis('equal')
    plt.grid(True)
    plt.show()
