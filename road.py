# road.py

import pygame
import math
from typing import List
import road_types
from node import Node
import user_tools

############################################################################################

class Lane:
    """
    Represents a lane between two nodes (start_node and end_node).
    A lane is a line connecting two nodes with a defined slope and length.
    """
    def __init__(self, start_node: Node, end_node: Node):
        # Node Initialization
        self.start_node = start_node                # The starting node of the lane
        self.end_node = end_node                    # The ending node of the lane
        self.start_node.next_node = end_node        # Set next node of start node
        self.start_node.curr_lane = self            # Assign this lane to the start node

        # Lane properties
        self.length = math.sqrt((self.end_node.coordinates[0] - self.start_node.coordinates[0]) ** 2 +
                                (self.end_node.coordinates[1] - self.start_node.coordinates[1]) ** 2)
        self.slope = ((self.end_node.coordinates[1] - self.start_node.coordinates[1]) /
                      (self.end_node.coordinates[0] - self.start_node.coordinates[0]))  # Slope of the lane

        # Geometry for lane rendering (currently just a transparent surface)
        self.geometry = pygame.Surface((0, 0), pygame.SRCALPHA)
        self.geometry.fill((0, 0, 0, 0))  # Transparent surface for lane rendering

    def draw(self, screen):
        """
        Draws the lane on the screen as a line between the start and end nodes.
        """
        pygame.draw.line(screen, (250, 70, 90), self.start_node.coordinates, self.end_node.coordinates, 25)


############################################################################################


class Road:
    """
    Represents a road consisting of left and right lanes.
    This class calculates and displays the geometry of the road, including lane markings and borders.
    The road geometry includes lines for dividing lanes and separating the road edges.
    """
    def __init__(self, start_point: [float, float], end_point: [float, float], road_type: str):
        """Initializes the road by constructing lane geometry based on the given start and end points."""

        # Store road type
        self.type_string      = road_type

        # Create start and end nodes
        self.start_node       = Node(start_point)
        self.end_node         = Node(end_point)
        self.start_node.set_next(self.end_node)

        # Pre-calculated geometry values
        self.scale            = 10
        self.median_width     = road_types.ROAD_TYPES[road_type]["median_width"]   * self.scale
        self.lane_width       = road_types.ROAD_TYPES[road_type]["lane_width"]     * self.scale
        self.shoulder_width   = road_types.ROAD_TYPES[road_type]["shoulder_width"] * self.scale
        self.left_lane_count  = road_types.ROAD_TYPES[road_type]["left_lane_count"]
        self.right_lane_count = road_types.ROAD_TYPES[road_type]["right_lane_count"]

        # Construct lane geometry
        center_median         = Lane(self.start_node, self.end_node)
        perpendicular_slope   = user_tools.perpendicularize_slope(center_median.slope)
        lane_translation      = user_tools.calculate_slope_translation(perpendicular_slope, self.lane_width)
        median_translation    = user_tools.calculate_slope_translation(perpendicular_slope,
                                ((self.median_width / 2) + self.lane_width / 2))

        self.left_lanes  = []
        self.right_lanes = []

        ################################################################################################################
        # Left Lanes Construction
        if self.left_lane_count > 0:
            # Add Innermost Left Lane
            start_buffer = user_tools.add_translation(start_point, median_translation, True)
            end_buffer   = user_tools.add_translation(end_point, median_translation, True)
            self.left_lanes.append(Lane(Node(end_buffer), Node(start_buffer)))

            # Add Remaining Left Lanes
            for _ in range(1, self.left_lane_count):
                start_buffer = user_tools.add_translation(start_buffer, lane_translation, True)
                end_buffer   = user_tools.add_translation(end_buffer, lane_translation, True)
                self.left_lanes.append(Lane(Node(end_buffer), Node(start_buffer)))

        ################################################################################################################
        # Right Lanes Construction
        start_buffer = user_tools.add_translation(start_point, median_translation)
        end_buffer   = user_tools.add_translation(end_point, median_translation)
        self.right_lanes.append(Lane(Node(start_buffer), Node(end_buffer)))

        # Add Remaining Right Lanes
        for _ in range(1, self.right_lane_count):
            start_buffer = user_tools.add_translation(start_buffer, lane_translation)
            end_buffer   = user_tools.add_translation(end_buffer, lane_translation)
            self.right_lanes.append(Lane(Node(start_buffer), Node(end_buffer)))

        ################################################################################################################
        # Final Geometry Setup
        self.geometry = self.calculate_bounding_box()
        self.build_geometry()

    # END - Constructor - __init__(...)
    ####################################################################################################################

    def __hash__(self):
        """Create a hash based on start and end coordinates (or other unique attributes)"""
        return hash((self.start_node, self.end_node))

    def __eq__(self, other):
        """Compare start and end coordinates (or other attributes) """
        if isinstance(other, Road):
            return self.start_node == other.start_node and self.end_node == other.end_node
        return False

    def road_type(self, attribute: str):
        return road_types.ROAD_TYPES[self.type_string][attribute]

    def draw(self, canvas: pygame.Surface):
        """
        Draws the road geometry on the provided canvas (screen).
        """
        canvas.blit(self.geometry, (0, 0))


    def build_geometry(self):
        """
        Builds the geometry for the road, including lane markings and borders.
        It calculates the positions for the lane divider lines and road edges.
        """
        # Precompute commonly used values for better efficiency
        half_lane = self.lane_width / 2
        line_width = 4                         # Width of the lines (for divider lines)
        lines_to_draw = []                     # List of lines to be drawn on the road
        corners = []

        ################################################################################################################
        # Left Lanes
        if self.left_lanes:  # If there are left lanes, process them

            # Add Middle Yellow Line (median line)
            buffer_point = self.left_lanes[0].start_node.coordinates
            buffer_slope = user_tools.perpendicularize_slope(self.left_lanes[0].slope)
            buffer_translation = user_tools.calculate_slope_translation(buffer_slope, half_lane - 7)
            buffer_point = user_tools.add_translation(buffer_point, buffer_translation)
            buffer_slope = buffer_point
            buffer_point = self.left_lanes[0].end_node.coordinates
            buffer_point = user_tools.add_translation(buffer_point, buffer_translation)
            lines_to_draw.append(('Yellow', buffer_point, buffer_slope))

            # Add Each Left White Lane Separator
            for lane in self.left_lanes:
                buffer_point = lane.start_node.coordinates
                buffer_slope = user_tools.perpendicularize_slope(lane.slope)
                buffer_translation = user_tools.calculate_slope_translation(buffer_slope, -half_lane)
                buffer_point = user_tools.add_translation(buffer_point, buffer_translation)
                buffer_slope = buffer_point
                buffer_point = lane.end_node.coordinates
                buffer_point = user_tools.add_translation(buffer_point, buffer_translation)
                lines_to_draw.append(('White', buffer_point, buffer_slope))

        ################################################################################################################
        # Right Lanes

        # Add Middle Yellow Line (median line)
        buffer_point = self.right_lanes[0].start_node.coordinates
        buffer_slope = user_tools.perpendicularize_slope(self.right_lanes[0].slope)
        buffer_translation = user_tools.calculate_slope_translation(buffer_slope, -half_lane)
        buffer_point = user_tools.add_translation(buffer_point, buffer_translation)
        buffer_slope = buffer_point
        buffer_point = self.right_lanes[0].end_node.coordinates
        buffer_point = user_tools.add_translation(buffer_point, buffer_translation)
        lines_to_draw.append(('Yellow', buffer_slope, buffer_point))

        # Add Each Right White Lane Separator
        for lane in self.right_lanes:
            buffer_point = lane.start_node.coordinates
            buffer_slope = user_tools.perpendicularize_slope(lane.slope)
            buffer_translation = user_tools.calculate_slope_translation(buffer_slope, half_lane)
            buffer_point = user_tools.add_translation(buffer_point, buffer_translation)
            buffer_slope = buffer_point
            buffer_point = lane.end_node.coordinates
            buffer_point = user_tools.add_translation(buffer_point, buffer_translation)
            lines_to_draw.append(('White', buffer_point, buffer_slope))

        ################################################################################################################
        # Loop through lines_to_draw and draw each line on the road geometry surface
        for line_color, start, end in lines_to_draw:
            pygame.draw.line(self.geometry, line_color, start, end, line_width)

    # END of Build Geometry
    ####################################################################################################################

    def calculate_bounding_box(self, breathing_room:int=10) -> pygame.Surface:
        """Calculates the minimum size bounding box required to draw the entire road geometry in full."""


        # Grab outermost lanes
        last_right_lane = self.right_lanes[-1]
        last_left_lane = self.left_lanes[-1] if self.left_lane_count > 0 else last_right_lane

        perpendicular_slope = user_tools.perpendicularize_slope(last_left_lane.slope)
        length_to_edge      = (self.lane_width/2) + self.shoulder_width + breathing_room
        translation = user_tools.calculate_slope_translation(perpendicular_slope, length_to_edge)

        # Grab Right Lane Ends and Add translation
        right_start = last_right_lane.start_node.coordinates
        right_end   = last_right_lane.end_node.coordinates
        user_tools.add_translation(right_start, translation)
        user_tools.add_translation(right_end, translation)

        # Grab Left Lane Ends and Add translation
        left_start = last_right_lane.start_node.coordinates
        left_end = last_right_lane.end_node.coordinates
        user_tools.add_translation(left_start, translation, True)
        user_tools.add_translation(left_end, translation, True)

        # Find Min and Max of Bounding Rectangle
        x_coords = [right_start[0], right_end[0], left_start[0], left_end[0]]
        y_coords = [right_start[1], right_end[1], left_start[1], left_end[1]]

        min_x, max_x = min(x_coords), max(x_coords)
        min_y, max_y = min(y_coords), max(y_coords)

        # Calculate dimensions
        width = max_x - min_x
        height = max_y - min_y

        # Create a transparent Pygame surface
        surface = pygame.Surface((width, height), pygame.SRCALPHA)

        return surface

