# user_tools.py

from roads import Road
from roads import Lane
from roads import Node
import math

def perpendicularize_slope(given_slope: float) -> float:
    """Calculates the slope perpendicular to the given slope."""
    if given_slope == 0:
        return float('inf')  # Represents an undefined slope (vertical line)

    return -1 / given_slope

def calculate_slope_translation(given_slope: float, distance_from_origin: float) -> (float, float):
    """Calculates translation along a given line."""
    if given_slope == float('inf'):
       return (0, distance_from_origin)

    x_translation = distance_from_origin / math.sqrt(1 + given_slope ** 2)
    y_translation = given_slope * x_translation
    return (x_translation, y_translation)

def add_translation(origin_point: [float, float], translation_tuple: [float, float] = (0, 0)) -> (float, float):
    """Adds given translation to an existing point."""
    x_new = origin_point[0] + translation_tuple[0]
    y_new = origin_point[1] + translation_tuple[1]
    return (x_new, y_new)


class road_builder:
    def __init__(self):
        self.user_inputer = 0

    def build_road(self, start_point, end_point, road_type):
        """ The two point arguments represents a center median line
              that the lanes will be parallel to and be built off from. """

        center_median = Lane(start_point, end_point)

        # Initialize lane lists
        right_lanes  = []
        left_lanes   = []
        right_starts = []
        right_ends   = []
        left_starts  = []
        left_ends    = []

        # cur_lane = road_type.lane_deatils()
        # road type will be expaneded upon
        lane_width = 10
        # Calculate real lane coordinates
        # center_median.slope
        # for i in range of #lanes
        #   self.right_lane_starts.append(calculate_perpendicular_coordinate(slope, lane_width))
        # cur_lane = Lane()

        for i in range(1):
            right_lanes.append(Lane(start_point, end_point))

        for i in range(1):
            left_lanes.append(Lane(end_point, start_point))

        new_road = Road(right_lanes, left_lanes)

        return new_road