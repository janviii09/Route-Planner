class Node:
    def __init__(self, id, x=0, y=0):
        self.id = id
        self.x = x
        self.y = y

class Edge:
    def __init__(self, u, v, weight=1):
        self.u = u
        self.v = v
        self.weight = weight
        self.base_weight = weight

class Graph:
    def __init__(self):
        self.nodes = {}  # id -> Node
        self.adj = {}    # id -> list of (neighbor_id, weight)
        self.edges = []  # list of Edge

    def add_node(self, id, x=0, y=0):
        if id not in self.nodes:
            self.nodes[id] = Node(id, x, y)
            self.adj[id] = []

    def add_edge(self, u, v, weight=1, bidirectional=True):
        if u not in self.nodes:
            self.add_node(u)
        if v not in self.nodes:
            self.add_node(v)
            
        self.adj[u].append((v, weight))
        self.edges.append(Edge(u, v, weight))
        if bidirectional:
            self.adj[v].append((u, weight))
            self.edges.append(Edge(v, u, weight))

    def update_weight(self, u, v, new_weight, bidirectional=True):
        # Update adjacency list
        for i, (neighbor, w) in enumerate(self.adj[u]):
            if neighbor == v:
                self.adj[u][i] = (v, new_weight)
        if bidirectional:
            for i, (neighbor, w) in enumerate(self.adj[v]):
                if neighbor == u:
                    self.adj[v][i] = (u, new_weight)
                    
        # Update edge list
        for edge in self.edges:
            if (edge.u == u and edge.v == v) or (bidirectional and edge.u == v and edge.v == u):
                edge.weight = new_weight

    def get_node(self, id):
        return self.nodes.get(id)
