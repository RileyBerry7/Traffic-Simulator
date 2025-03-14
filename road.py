import pygame
import math
from typing import List
import road_types


############################################################################################

class Node:
    """
    Represents a node in the road network, with connections to other nodes and rendering attributes.
    Each node may have connections to other nodes for traversal in the simulation.
    """
    def __init__(self, coordinates: tuple[float, float] = (0, 0)):
        # Graph relationships
        self.next_node: Node = None               # The next node connected to this one
        self.prev_node: Node = None               # The previous node connected to this one
        self.curr_lane: Node = None               # The lane associated with this node
        self.in_intersection = False              # Flag for intersection status
        self.intersection_connections = []        # List of connected nodes in an intersection

        # Rendering Attributes
        self.size = 30                            # Size of the node (used in drawing)
        self.color = 'Red'                        # Color of the node (used in drawing)
        self.coordinates = coordinates           # The (x, y) coordinates of the node
        self.geometry = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.geometry.fill((0, 0, 0, 0))         # Transparent rectangle for node rendering

    def set_next_node(self, next_node):
        """
        Set the next node in the graph and update intersection connections.
        Always changes index 0 of intersection_connections to the next node.
        """
        self.next_node = next_node
        self.intersection_connections[0] = next_node

    def draw(self, screen):
        """
        Draws the node on the given screen at the node's coordinates.
        A circle is drawn to represent the node.
        """
        pygame.draw.circle(screen, self.color, self.coordinates, self.size)


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
    def __init__(self, right_lanes: List[Lane], left_lanes: List[Lane], road_type: str):

        # Road Specific Type
        self.type_string = road_type

        # Lane Data
        self.right_lanes = right_lanes  # Right lanes of the road
        self.left_lanes = left_lanes    # Left lanes of the road

        # Locational Data (start and end coordinates of the road)
        self.start_coord = right_lanes[0].start_node.coordinates
        self.end_coord   = right_lanes[0].end_node.coordinates

        # Geometry Data (surface to render the road)
        self.geometry = pygame.Surface((1400, 1000), pygame.SRCALPHA)
        self.geometry.fill((0, 0, 0, 0))  # Transparent surface for road rendering
        self.build_geometry()



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
        import user_tools

        # Subject to Change based on road_type
        median_line_color = self.road_type("median_line_color")          # Color for the median (middle) line
        divider_line_color = 'White'          # Color for the lane divider lines
        lines_to_draw = []                     # List of lines to be drawn on the road
        lane_width = self.road_type("lane_width")                        # The width of each lane
        half_lane = lane_width / 2             # Half the lane width for positioning the lines
        line_width = 4                         # Width of the lines (for divider lines)

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
            lines_to_draw.append((median_line_color, buffer_point, buffer_slope))

            # Add Each Left White Lane Separator
            for lane in self.left_lanes:
                buffer_point = lane.start_node.coordinates
                buffer_slope = user_tools.perpendicularize_slope(lane.slope)
                buffer_translation = user_tools.calculate_slope_translation(buffer_slope, -half_lane)
                buffer_point = user_tools.add_translation(buffer_point, buffer_translation)
                buffer_slope = buffer_point
                buffer_point = lane.end_node.coordinates
                buffer_point = user_tools.add_translation(buffer_point, buffer_translation)
                lines_to_draw.append((divider_line_color, buffer_point, buffer_slope))

            # Add Both Left Perpendicular Edge Lines
            corner_buffer = lines_to_draw[-1][1]
            lines_to_draw.append(('Red', lines_to_draw[-1][2], lines_to_draw[0][2]))
            lines_to_draw.append(('Blue', corner_buffer, lines_to_draw[0][1]))

        else:  # If no left lanes, set median line color to white
            median_line_color = 'White'

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
        lines_to_draw.append((median_line_color, buffer_slope, buffer_point))

        # Add Each Right White Lane Separator
        for lane in self.right_lanes:
            buffer_point = lane.start_node.coordinates
            buffer_slope = user_tools.perpendicularize_slope(lane.slope)
            buffer_translation = user_tools.calculate_slope_translation(buffer_slope, half_lane)
            buffer_point = user_tools.add_translation(buffer_point, buffer_translation)
            buffer_slope = buffer_point
            buffer_point = lane.end_node.coordinates
            buffer_point = user_tools.add_translation(buffer_point, buffer_translation)
            lines_to_draw.append((divider_line_color, buffer_slope, buffer_point))

        # Add Both Right Perpendicular Edge Lines
        lines_to_draw.append(('Red', lines_to_draw[-1][1], lines_to_draw[0][1]))
        lines_to_draw.append(('Blue', lines_to_draw[-2][2], lines_to_draw[0][2]))

        ################################################################################################################
        # Draw All Lines onto Geometry Attribute
        for line in lines_to_draw:
            pygame.draw.line(self.geometry, line[0], line[1], line[2], line_width)

        # End of build_geometry()
