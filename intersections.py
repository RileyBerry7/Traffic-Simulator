# intersections.py

from road import Road
from road import Lane
from road import Node

# Intersection between two 2-way roads, with each incoming lane has 3 possible paths
class four_way_stop:
    def __init__(self, coordinates:[float,float]=(0,0),
                       left_road: Road=None,
                       right_road: Road=None,
                       top_road: Road=None,
                       bottom_road: Road=None):

        # Intersection Nodes
        self.left_input   = None
        self.left_output  = None
        self.right_input  = None
        self.right_output = None
        self.top_input    = None
        self.top_output   = None
        self.bot_input    = None
        self.bot_output   = None

        # Intersection State
        self.locked = False
        self.clear  = True
        self.right_of_way_holder = None
        self.center_coordinate = coordinates

    def attach_road(self, input_node: Node, output_node: Node, incoming_direction: str):
        """Note: This method moves roads to the intersection. So pre-existing road location
                  data wil be overwritten to fit within the bounds of the intersection.

           TLDR:   The intersection must exist prior to this being called.

                    If you dont want your roads getting moved, attach the intersection to the road,
                    then call this to setup the intersection."""

        input_node.in_intersection = True
        output_node.in_intersection = True

        if incoming_direction == 'left':
            input_node  = self.left_input
            output_node = self.left_output

        if incoming_direction == 'right':
            input_node  = self.right_input
            output_node = self.right_output

        if incoming_direction == 'top':
            input_node  = self.top_input
            output_node = self.top_output

        if incoming_direction == 'bot':
            input_node  = self.bot_input
            output_node = self.bot_output




    def calculate_lanes(self) -> [Lane]:
        """Reccomend using this method as little as possible"""
        # This method will will first fill all empty intersection nodes, based on given
        # node.coordinates data.
        #
        # This method assumes all pre-existing coordinate data is valid within the shape of the intersection

        calculated_lanes = []

        left_to_right_lane = Lane(self.left_input, self.right_output)
        right_to_left_lane = Lane(self.right_input, self.left_output)
        calculated_lanes.append(left_to_right_lane)
        calculated_lanes.append(right_to_left_lane)

        return calculated_lanes

    def draw(self, surface):
        """call draw after calculate lanes"""
        lane_surfaces = self.calculate_lanes()

        for lane in lane_surfaces:
            lane.draw(surface)




    # def grab_nodes(self, road, side:str='End') -> (Node, Node):

    #     if self.left_road is not None:
    #         # Grab Left Nodes
    #         if self.get_lane_direction(left_road) == 'left':
    #             left_in_node  = left_road.left_lanes[0]
    #             left_out_node = left_road.right_lanes[0]
    #         else:
    #             left_in_node  = left_road.right_lanes[0]
    #             left_out_node = left_road.left_lanes[0]
    #
    #     # Grab Right nodes
    #     if self.get_lane_direction(right_road) == 'left':
    #         right_in_node  = right_road.left_lanes[0]
    #         right_out_node = right_road.right_lanes[0]
    #     else:
    #         right_in_node  = right_road.right_lanes[0]
    #         right_out_node = right_road.left_lanes[0]
    #
    #     # Grap Top Nodes
    #     if self.get_lane_direction(top_road) == 'left':
    #         top_in_node = top_road.left_lanes[0]
    #         top_out_node = top_road.right_lanes[0]
    #     else:
    #         top_in_node = top_road.right_lanes[0]
    #         top_out_node = top_road.left_lanes[0]
    #
    #     # Grab bottom Nodes
    #     if self.get_lane_direction(bottom_road) == 'left':
    #         bottom_in_node = bottom_road.left_lanes[0]
    #         bottom_out_node = bottom_road.right_lanes[0]
    #     else:
    #         bottom_in_node = bottom_road.right_lanes[0]
    #         bottom_out_node = bottom_road.left_lanes[0]
    #
    #     # Create Intersection Paths
    #     self.left_to_right = Lane(left_in_node, right_out_node)
    #     self.right_to_left = Lane(right_in_node, left_out_node)
    #     self.top_to_bottom = Lane(top_in_node, bottom_out_node)
    #     self.bottom_to_top = Lane(bottom_in_node, top_out_node)
    #
    #     # Let Nodes be able to reference the lane they are a part of
    #     # and then assign next lane based on out road and out node found
    #     # self.left_to_right.next_lane =
    #     self.right_to_left.next_lane = left_road
    #     self.top_to_bottom.next_lane = bottom_road
    #     # self.bottom_to_top.end_node  = top_
    #
    #
    # def get_lane_direction(self, road: Road):
    #     """ Determine whether the road feeds into the intersection from the left or right. """
    #     start_dist = self.distance_to_intersection(road.start_coord)
    #     end_dist = self.distance_to_intersection(road.end_coord)
    #
    #     # If the end is closer, it's coming from the right; otherwise, it's coming from the left
    #     return 'right' if end_dist < start_dist else 'left'
    #
    # def distance_to_intersection(self, point):
    #     """ Calculate Euclidean distance from a point to the intersection center. """
    #     return math.sqrt((point[0] - self.center_coordinate[0]) ** 2 +
    #                      (point[1] - self.center_coordinate[1]) ** 2)
