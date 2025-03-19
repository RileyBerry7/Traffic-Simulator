# road_network.py

import road
import user_tools

############################################################################################

class road_network:
    def __init__(self):
        # Adjacency Lists
        self.road_list: road.List[road.Node] = [] # Higher Level - Every Adjacency node represents an intersection connection
        self.lane_list: road.List[road.Node] = [] # Lower  Level -


    def add_road(self, start_point: [float, float], end_point: [float, float],
                 road_type: str, root_road=None, branch_road=None) -> bool:
        """"""

        # Create road and add to adjacency list
        new_road = user_tools.build_road(start_point, end_point, road_type)
        if new_road:
            self.road_list.append(new_road)
        else:
            return False

        # Connect Root road to new road with intersection
        if root_road:
        # First check if intersection exists
            # If Yes connect to existing intersection

        else:
            # If No break root road into 2 halves


                # then create and insert new intersection

        # Connect Branch road to new road
        if branch_road:

        # Successful Add
        return True


############################################################################################
