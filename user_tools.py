# user_tools.py
import road
from road import Road
from road import Lane
from road import Node
import road_types
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

def add_translation(origin_point: [float, float], translation_tuple: [float, float] = (0, 0), invert:bool=False) -> (float, float):
    """Adds given translation to an existing point."""
    if invert:
        x_new = origin_point[0] - translation_tuple[0]
        y_new = origin_point[1] - translation_tuple[1]
        return (x_new, y_new)

    x_new = origin_point[0] + translation_tuple[0]
    y_new = origin_point[1] + translation_tuple[1]
    return (x_new, y_new)


class road_builder:
    def __init__(self):
        self.user_inputer = 0

    def build_road(start_point: [float, float], end_point: [float, float], road_type: str):
        """ The two point arguments represents a center median line
              that the lanes will be parallel to and be built off from. """


        center_median       = Lane(Node(start_point), Node(end_point))
        perpendicular_slope = perpendicularize_slope(center_median.slope)
        lane_translation    = calculate_slope_translation(perpendicularize_slope(center_median.slope), road_types.ROAD_TYPES[road_type]["lane_width"])
        median_translation  = calculate_slope_translation(perpendicular_slope, (((road_types.ROAD_TYPES[road_type]["median_width"]) / 2) +
                                                                                  road_types.ROAD_TYPES[road_type]["lane_width"] / 2))

        left_lanes  = []
        right_lanes = []

        ################################################################################################################
        # Left Lanes

        if road_types.ROAD_TYPES[road_type]["left_lane_count"] > 0: # If there are left lanes, process them

            # Add Innermost Left Index 0 Lane
            start_buffer = add_translation(start_point, median_translation, True)
            end_buffer   = add_translation(end_point,   median_translation, True)
            left_lanes.append(Lane(Node(end_buffer), Node(start_buffer)))

            # Add 1 to k Remaining Left Lanes
            for index in range(1 ,road_types.ROAD_TYPES[road_type]["left_lane_count"]):

                start_buffer = add_translation(start_buffer, lane_translation, True)
                end_buffer = add_translation(end_buffer, lane_translation, True)
                left_lanes.append(Lane(Node(end_buffer), Node(start_buffer)))


        else:  # If no left lanes, set median line color to white
            median_line_color = 'White'

        ################################################################################################################
        # Right Lanes

        # Add Innermost Right Index 0 Lane
        start_buffer = add_translation(start_point, median_translation)
        end_buffer = add_translation(end_point, median_translation)
        right_lanes.append(Lane(Node(start_buffer), Node(end_buffer)))

        # Add 1 to k Remaining Right Lanes
        for index in range(1, road_types.ROAD_TYPES[road_type]["right_lane_count"]):
            start_buffer = add_translation(start_buffer, lane_translation)
            end_buffer = add_translation(end_buffer, lane_translation)
            right_lanes.append(Lane(Node(start_buffer), Node(end_buffer)))

        ################################################################################################################
        # Build Road
        return road.Road(right_lanes, left_lanes, road_type)

        # End of build_geometry()


