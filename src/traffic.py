from src.segment_tree import SegmentTree

class TrafficManager:
    def __init__(self, graph):
        self.graph = graph
        # Hours: 6 to 24 (19 slots)
        # index 0 -> 6am, ..., index 18 -> 24 (midnight)
        self.hours = list(range(6, 25))
        
        # High multipliers for rush hour (8-10am and 5-7pm)
        self.arterial_mult = [
            1.0, 1.2, # 6, 7
            3.0, 3.5, 2.5, # 8, 9, 10
            1.5, 1.2, 1.2, 1.2, 1.2, 1.5, # 11..16
            2.5, 3.0, 2.0, # 17, 18, 19
            1.2, 1.0, 1.0, 1.0, 1.0 # 20..24
        ]
        
        self.local_mult = [
            1.0, 1.0, 
            1.2, 1.2, 1.1,
            1.0, 1.0, 1.0, 1.0, 1.0, 1.0,
            1.2, 1.2, 1.1,
            1.0, 1.0, 1.0, 1.0, 1.0
        ]
        
        # We need a segment tree for each edge to query peak weight
        self.edge_trees = {}
        for edge in graph.edges:
            # Heuristic: weight >= 6 is considered an arterial road
            is_arterial = edge.base_weight >= 6
            mult_array = self.arterial_mult if is_arterial else self.local_mult
            
            # Precompute weights for all hours for this edge
            weight_history = [round(edge.base_weight * m, 1) for m in mult_array]
            self.edge_trees[(edge.u, edge.v)] = SegmentTree(weight_history)
            
    def apply_traffic(self, hour):
        """Dynamic Edge Reweighting based on time"""
        idx = hour - 6
        if idx < 0 or idx >= len(self.hours):
            idx = 0
            
        for edge in self.graph.edges:
            is_arterial = edge.base_weight >= 6
            mult = self.arterial_mult[idx] if is_arterial else self.local_mult[idx]
            new_weight = round(edge.base_weight * mult, 1)
            
            # Update graph
            edge.weight = new_weight
            
        # also update adjacency list
        for edge in self.graph.edges:
            self.graph.update_weight(edge.u, edge.v, edge.weight, bidirectional=True)
            
    def get_peak_congestion(self, u, v, start_hour, end_hour):
        """Segment tree range-max query"""
        start_idx = start_hour - 6
        end_idx = end_hour - 6 + 1 # +1 for exclusive bound in query
        start_idx = max(0, start_idx)
        end_idx = min(len(self.hours), end_idx)
        
        tree = self.edge_trees.get((u, v)) or self.edge_trees.get((v, u))
        if not tree:
            return -1
            
        return tree.query(start_idx, end_idx)
