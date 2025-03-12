# intersections.py

from roads import Road
from roads import Lane

# Intersection between two 2-way roads, with each incoming lane has 3 possible paths
class four_way_stop:
    def __init__(self, left_road: Road, right_road: Road, top_road: Road, bottom_road: Road):
        self.left_road   = left_road
        self.right_road  = right_road
        self.top_road    = top_road
        self.bottom_road = bottom_road

        self.locked = False
        self.clear  = True

        self.right_away_holder = None

        self.center_coordinate = (0,0)

        # Lane Connectors

        # Grab Left Nodes
        if self.get_lane_direction(left_road) == 'left':
            left_in_node  = left_road.left_lanes[0]
            left_out_node = left_road.right_lanes[0]
        else:
            left_in_node  = left_road.right_lanes[0]
            left_out_node = left_road.left_lanes[0]

        # Grab Right nodes
        if self.get_lane_direction(right_road) == 'left':
            right_in_node  = right_road.left_lanes[0]
            right_out_node = right_road.right_lanes[0]
        else:
            right_in_node  = right_road.right_lanes[0]
            right_out_node = right_road.left_lanes[0]

        # Grap Top Nodes
        if self.get_lane_direction(top_road) == 'left':
            top_in_node = top_road.left_lanes[0]
            top_out_node = top_road.right_lanes[0]
        else:
            top_in_node = top_road.right_lanes[0]
            top_out_node = top_road.left_lanes[0]

        # Grab bottom Nodes
        if self.get_lane_direction(bottom_road) == 'left':
            bottom_in_node = bottom_road.left_lanes[0]
            bottom_out_node = bottom_road.right_lanes[0]
        else:
            bottom_in_node = bottom_road.right_lanes[0]
            bottom_out_node = bottom_road.left_lanes[0]

        # Create Intersection Paths
        self.left_to_right = Lane(left_in_node, right_out_node)
        self.right_to_left = Lane(right_in_node, left_out_node)
        self.top_to_bottom = Lane(top_in_node, bottom_out_node)
        self.bottom_to_top = Lane(bottom_in_node, top_out_node)

        # Let Nodes be able to reference the lane they are a part of
        # and then assign next lane based on out road and out node found
        # self.left_to_right.next_lane =
        self.right_to_left.next_lane = left_road
        self.top_to_bottom.next_lane = bottom_road
        # self.bottom_to_top.end_node  = top_


    def get_lane_direction(self, road: Road):
        """ Determine whether the road feeds into the intersection from the left or right. """
        start_dist = self.distance_to_intersection(road.start_coord)
        end_dist = self.distance_to_intersection(road.end_coord)

        # If the end is closer, it's coming from the right; otherwise, it's coming from the left
        return 'right' if end_dist < start_dist else 'left'

    def distance_to_intersection(self, point):
        """ Calculate Euclidean distance from a point to the intersection center. """
        return math.sqrt((point[0] - self.center_coordinate[0]) ** 2 +
                         (point[1] - self.center_coordinate[1]) ** 2)
