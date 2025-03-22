# road_network.py
from enum import unique

import node
import road
from typing import Dict, Tuple, List

############################################################################################

class Road_Network:
    def __init__(self):

        # Road - Edge Dictionary
        self.road_dict: Dict[road.Road, List[node.Node, node.Node]] = {} # Higher Level

        # Lane - Adjacency List
        self.lane_list: List[road.Node] = [] # Lower  Level

        # Build Points
        self.build_points: List[Tuple[Tuple[float, float], road.Road, node.Node]] = []
        self.generate_build_points()

    def add_road(self,
                 start_point: [float, float],
                 end_point:   [float, float],
                 road_type:   str,
                 root_road  =None,
                 branch_road=None) -> bool:
        """"""

        # Create road and add to adjacency list
        new_road = road.Road(start_point, end_point, road_type)

        # Check if road already exists in list
        if new_road and not self.road_dict.get(new_road, None):
            # If no road exists, Add to list
            self.road_dict[new_road] = [new_road.start_node, new_road.end_node]
            # print('Road Added to Road Graph.')
            return True
        else:
            return False

        # Below is WIP - Connection to other roads:

        # # Connect Root road to new road with intersection
        # if root_road:
        # # First check if intersection exists
        #     # If Yes connect to existing intersection
        #
        #     # If No break root road into 2 halves
        #
        #
        #         # then create and insert new intersection
        #
        # # Connect Branch road to new road
        # if branch_road:

        # Successful Add
        return True

    def generate_build_points(self, point_step: float=100):
        """ Given the adjacency list of roads, this function will traverse the road network
              and return a list of tuples (coordinates, road, node), node may be empty. """

        node_dict  = {}
        point_list = []

        # loop through dict of roads
        for key_road in self.road_dict.keys():

            # Check if start node already saved
            if not node_dict.get(key_road.start_node.coordinates, None):
                node_dict[key_road.start_node.coordinates] = (key_road, key_road.start_node)

            # Check if end node already been saved
            if not node_dict.get(key_road.end_node.coordinates, None):
                node_dict[key_road.end_node.coordinates]   = (key_road, key_road.end_node)

            # Calculate the difference in x and y
            delta_x = key_road.end_node.coordinates[0] - key_road.start_node.coordinates[0]
            delta_y = key_road.end_node.coordinates[1] - key_road.start_node.coordinates[1]

            # Calculate the distance between the two points
            distance = key_road.right_lanes[0].length

            # Calculate the number of steps required to generate points at the point_step distance
            num_steps = int(distance // point_step)

            # Calculate the normalized direction vector (unit vector)
            direction_x = delta_x / distance
            direction_y = delta_y / distance

            # Generate the points
            for i in range(1, num_steps):  # Start from 1 to exclude the start point
                x = key_road.start_node.coordinates[0] + i * point_step * direction_x
                y = key_road.start_node.coordinates[1] + i * point_step * direction_y
                point_list.append(((x, y), key_road, None))

        # Add all dictionary Key-Values to the point_list
        for coordinate in node_dict.keys():
            point_list.append((coordinate, node_dict[coordinate][0], node_dict[coordinate][1]))

        self.build_points = point_list

############################################################################################
