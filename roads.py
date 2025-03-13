# roads.py


import pygame
import math
from typing import List

from PIL.ImageChops import offset
from scipy.linalg import sqrtm


############################################################################################

class Node:
    def __init__(self, coordinates: tuple[float, float]=(0,0)):

        # Graph relationships
        self.next_node: Node = None
        self.prev_node: Node = None
        self.curr_lane: Node = None
        self.in_intersection = False
        self.intersection_connections = []

        # Rendering Attributes
        self.size = 30
        self.color = 'Red'
        self.coordinates = coordinates
        self.geometry =  pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.geometry.fill((0, 0, 0, 0)) # transparent rectangle


    def set_next_node(self, next_node):
        """Always changes index 0 of intersection_connections"""
        self.next_node = next_node
        self.intersection_connections[0] = next_node

    def draw(self, screen):
        # Draw the circle centered in the node surface
        pygame.draw.circle(screen, self.color,self.coordinates, self.size)


############################################################################################

class Lane:
    def __init__(self, start_node: Node, end_node: Node):

        # Node Initialization
        self.start_node = start_node
        self.end_node   = end_node
        self.start_node.next_node = end_node
        self.start_node.curr_lane = self

        self.length     = math.sqrt((self.end_node.coordinates[0] - self.start_node.coordinates[0]) ** 2 +
                                   (self.end_node.coordinates[1] - self.start_node.coordinates[1]) ** 2)

        self.slope      = ((self.end_node.coordinates[1] - self.start_node.coordinates[1]) /
                           (self.end_node.coordinates[0] - self.start_node.coordinates[0]))

        # print(self.slope)

        self.geometry =  pygame.Surface((0,0), pygame.SRCALPHA)
        self.geometry.fill((0, 0, 0, 0)) # transparent rectangle

    def draw(self, screen):
        pygame.draw.line(screen, (250,70,90), self.start_node.coordinates, self.end_node.coordinates, 25)


############################################################################################


###### DRAW needs major reworking, lanes should start from the middle
#      to allow for better compatibility with smaller roads
#                     ex. road        |    |     |     ^    |
#                                     |    v     |     |    |
#                                     | L2,L1,L0 | R0,R1,R2 |
#                                     |          |          |

class Road:

    ################
    # Constructor  #
    ################
    def __init__(self, right_lanes: List[Lane], left_lanes: List[Lane]=[]):

        # Lane Data
        self.right_lanes = right_lanes
        self.left_lanes  = left_lanes

        # Locational Data
        self.start_coord = right_lanes[0].start_node.coordinates
        self.end_coord   = right_lanes[0].end_node.coordinates

        # Geometry Data
        self.geometry    = pygame.surface.Surface((1400, 1000), pygame.SRCALPHA)
        self.geometry.fill((0, 0, 0, 0))
        self.build_geometry()



    ###########################
    # Displays Road Geometry  #
    ###########################
    def draw(self, canvas: pygame.Surface):
        canvas.blit(self.geometry, (0,0))



    ################################
    # Calculates All Road Geometry #
    ################################
    def build_geometry(self):

        import user_tools

        # Subject to Change based on road_type
        median_line_color  = 'Yellow'
        divider_line_color = 'White'
        lines_to_draw      = []
        lane_width         = 50             # grab this from road_type when implemented
        half_lane          = lane_width/2
        line_width         = 4

        ############################################################################
        # Left Lanes

        if self.left_lanes: # There are left lane(s)

            # Add Middle Yellow Line - calculate proper location -> then save it
            buffer_point = self.left_lanes[0].start_node.coordinates  # grab line start
            buffer_slope = user_tools.perpendicularize_slope(self.left_lanes[0].slope)  # calc perpendicular slope
            buffer_translation = user_tools.calculate_slope_translation(buffer_slope, half_lane-7)  # calc translation
            buffer_point = user_tools.add_translation(buffer_point, buffer_translation)  # add  translation
            buffer_slope = buffer_point  # save point in buffer
            buffer_point = self.left_lanes[0].end_node.coordinates  # grab line end
            buffer_point = user_tools.add_translation(buffer_point, buffer_translation)  # add  translation
            lines_to_draw.append((median_line_color, buffer_point, buffer_slope))  # Add  points to line list

            # Add Every Left White Lane Seperator
            for lane in self.left_lanes:
                # Add Outer White Line - calculate proper location -> then save it
                buffer_point = lane.start_node.coordinates                                          # grab line start
                buffer_slope = user_tools.perpendicularize_slope(lane.slope)                        # calc perp slope
                buffer_translation = user_tools.calculate_slope_translation(buffer_slope,-half_lane)# calc translation
                buffer_point = user_tools.add_translation(buffer_point, buffer_translation)         # add  translation
                buffer_slope = buffer_point                                                         # save point in buffer
                buffer_point = lane.end_node.coordinates                                            # grab line end
                buffer_point = user_tools.add_translation(buffer_point, buffer_translation)         # add  translation
                lines_to_draw.append((divider_line_color, buffer_point, buffer_slope))              # save both points

            # Add Both Left Perpendicular Edge Lines
            corner_buffer = lines_to_draw[-1][1]
            lines_to_draw.append(('Red', lines_to_draw[-1][2], lines_to_draw[0][2]))
            lines_to_draw.append(('Blue', corner_buffer, lines_to_draw[0][1]))

        else: # No left lanes
            median_line_color = 'White'

        ############################################################################
        # Right Lanes

        # Add Middle Yellow Line - calculate proper location -> then save it
        buffer_point       = self.right_lanes[0].start_node.coordinates                       # grab line start
        buffer_slope       = user_tools.perpendicularize_slope(self.right_lanes[0].slope)     # calc perpendicular slope
        buffer_translation = user_tools.calculate_slope_translation(buffer_slope, -half_lane) # calc translation
        buffer_point       = user_tools.add_translation(buffer_point, buffer_translation)     # add  translation
        buffer_slope       = buffer_point                                                     # save point in buffer
        buffer_point       = self.right_lanes[0].end_node.coordinates                         # grab line end
        buffer_point       = user_tools.add_translation(buffer_point, buffer_translation)     # add  translation
        lines_to_draw.append((median_line_color, buffer_slope, buffer_point))                 # Add  points to line list


        # Add Every Right White Lane Seperator
        for lane in self.right_lanes:

            # Add Outer White Line - calculate proper location -> then save it
            buffer_point       = lane.start_node.coordinates                                     # grab line start
            buffer_slope       = user_tools.perpendicularize_slope(lane.slope)                   # calc perp slope
            buffer_translation = user_tools.calculate_slope_translation(buffer_slope, half_lane) # calc translation
            buffer_point       = user_tools.add_translation(buffer_point, buffer_translation)    # add  translation
            buffer_slope       = buffer_point                                                    # save point in buffer
            buffer_point       = lane.end_node.coordinates                                       # grab line end
            buffer_point       = user_tools.add_translation(buffer_point, buffer_translation)    # add  translation
            lines_to_draw.append((divider_line_color, buffer_slope, buffer_point))               # Add  points to list

        # Add Both Right Perpendicular Edge Lines
        lines_to_draw.append(('Red', lines_to_draw[-1][1], lines_to_draw[0][1]))
        lines_to_draw.append(('Blue', lines_to_draw[-2][2], lines_to_draw[0][2]))

        ############################################################################
        # Draw All Lines onto Geometry Attribute

        for line in lines_to_draw:
            pygame.draw.line(self.geometry, line[0], line[1], line[2], line_width)

        # End of build_geometry()


    # # LEFT LANES:
    #     if self.left_lanes:
    #         # Iterate and draw all right lanes
    #         for lane in self.left_lanes:
    #
    #             # Grab lane width based on road type
    #             lane_width = -25
    #
    #         # Calculate Perpendicular slope
    #         perpendicular_slope =-1/ lane.slope if lane.slope != 0 else 1 # NEEDS FIX
    #
    #         # Use a small delta to compute the perpendicular offset
    #         offset_x = offset / math.sqrt(1 + perpendicular_slope ** 2)
    #         offset_y = perpendicular_slope * offset_x
    #
    #         # Calculate new coordinates for the offset lines
    #         lane_line_start = (lane.start_node.coordinates[0] + offset_x,
    #                            lane.start_node.coordinates[1] + offset_y)
    #         lane_line_end   = (lane.end_node.coordinates[0]   + offset_x,
    #                            lane.end_node.coordinates[1]   + offset_y)
    #
    #         # lane.draw(screen)
    #         pygame.draw.line(screen, 'White', lane_line_start, lane_line_end, 5)
    #         # pygame.draw.line(screen, 'Red',lane.start_node.coordinates, lane.end_node.coordinates, 5)
    #
    #         # Grab first corner in first loop
    #         if not corner_buffer_full:
    #             first_corner  = lane_line_start
    #             second_corner = lane_line_end
    #             corner_buffer_full = True
    #
    #     ##### Left Loop - END #########
    #
    #     # Calculate reverse offset for final line
    #     offset_x = -offset / math.sqrt(1 + perpendicular_slope ** 2)
    #     offset_y = perpendicular_slope * offset_x
    #
    #     # Calculate new coordinates for final the offset line
    #     lane_line_start = (lane.start_node.coordinates[0] + offset_x,
    #                         lane.start_node.coordinates[1] + offset_y)
    #     lane_line_end = (lane.end_node.coordinates[0] + offset_x,
    #                         lane.end_node.coordinates[1] + offset_y)
    #
    #     # Draw perpendicular Start for Left Lanes
    #     pygame.draw.line(screen,
    #                'Red',
    #                      first_corner,
    #                      lane_line_start,
    #                      5)
    #
    #     # Draw perpendicular End for Left Lanes
    #     pygame.draw.line(screen,
    #                      'Blue',
    #                      second_corner,
    #                      lane_line_end,
    #                      5)
    #
    #     # Prep corners for left
    #     first_corner  = lane_line_start
    #     second_corner = lane_line_end
    #
    # ############################################################################
    # # RIGHT LANES:
    #     # Iterate and draw all left lanes
    #     if self.right_lanes:
    #         for lane in self.right_lanes:
    #             # Calculate individual lane offset based on distance between lanes
    #             offset = -25
    #
    #             # Calculate Perpendicular slope
    #             perpendicular_slope = -1 / lane.slope if lane.slope != 0 else 1  # NEEDS FIX
    #
    #             # Use a small delta to compute the perpendicular offset
    #             offset_x = offset / math.sqrt(1 + perpendicular_slope ** 2)
    #             offset_y = perpendicular_slope * offset_x
    #
    #             # Calculate new coordinates for the offset lines
    #             lane_line_start = (lane.start_node.coordinates[0] + offset_x,
    #                                lane.start_node.coordinates[1] + offset_y)
    #             lane_line_end = (lane.end_node.coordinates[0] + offset_x,
    #                              lane.end_node.coordinates[1] + offset_y)
    #
    #             # lane.draw(screen)
    #             pygame.draw.line(screen, 'White', lane_line_start, lane_line_end, 5)
    #             # pygame.draw.line(screen, 'Red',lane.start_node.coordinates, lane.end_node.coordinates, 5)
    #
    #         ##### Right Loop - END #########
    #
    #         # Calculate reverse offset for final line
    #         offset_x = -offset / math.sqrt(1 + perpendicular_slope ** 2)
    #         offset_y = perpendicular_slope * offset_x
    #
    #         # Calculate new coordinates for final the offset line
    #         lane_line_start = (lane.start_node.coordinates[0] + offset_x,
    #                            lane.start_node.coordinates[1] + offset_y)
    #         lane_line_end = (lane.end_node.coordinates[0] + offset_x,
    #                          lane.end_node.coordinates[1] + offset_y)
    #
    #         # Draw perpendicular End for Right lanes
    #         pygame.draw.line(screen,
    #                          'Blue',
    #                          first_corner,
    #                          lane_line_end,
    #                          5)
    #
    #         # Draw perpendicular Start for Right lanes
    #         pygame.draw.line(screen,
    #                          'Red',
    #                          second_corner,
    #                          lane_line_start,
    #                          5)
    #
    # ##################
    #     # Draw final lane to close the road
    #     pygame.draw.line(screen, 'White', lane_line_start, lane_line_end, 5)

