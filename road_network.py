# road_network.py
import roads


class road_network:
    def __init__(self):
        # Adjacency List
        self.node_adjacency_list: roads.List[roads.Node] = []2
        self.road_list: roads.List[roads.Node] = []