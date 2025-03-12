# roads.py


import pygame
import math
from collections import namedtuple

from PIL.ImageChops import offset
from scipy.linalg import sqrtm


############################################################################################

class Node:
    def __init__(self, coordinates: tuple[float, float]=(0,0)):
        self.size = 30
        self.color = 'Red'
        self.coordinates = coordinates
        self.geometry =  pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.geometry.fill((0, 0, 0, 0)) # transparent rectangle

    def draw(self, screen):
        # Draw the circle centered in the node surface
        pygame.draw.circle(screen, self.color,self.coordinates, self.size)

############################################################################################

class Lane:
    def __init__(self, start: tuple[float, float]=(0,0), end: tuple[float, float]=(0,0)):
        self.next_lane  = None
        self.start_node = Node(start)
        self.end_node   = Node(end)
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

class Road:
    def __init__(self, right_lanes: [Lane], left_lanes: [Lane]):
        self.right_lanes = right_lanes
        self.left_lanes  = left_lanes
        self.start_coord = right_lanes[0].start_node.coordinates
        self.end_coord   = right_lanes[0].end_node.coordinates

    def draw(self, screen):

        # Initialize loop variables
        offset = 0
        perpendicular_slope = 0
        corner_buffer_full  = False
        first_corner  = (0, 0)
        second_corner = (0, 0)

    ############################################################################
    # LEFT LANES:
        # Iterate and draw all right lanes
        for lane in self.left_lanes:

            # Calculate individual lane offset based on distance between lanes
            offset = -25

            # Calculate Perpendicular slope
            perpendicular_slope =-1/ lane.slope if lane.slope != 0 else 1 # NEEDS FIX

            # Use a small delta to compute the perpendicular offset
            offset_x = offset / math.sqrt(1 + perpendicular_slope ** 2)
            offset_y = perpendicular_slope * offset_x

            # Calculate new coordinates for the offset lines
            lane_line_start = (lane.start_node.coordinates[0] + offset_x,
                               lane.start_node.coordinates[1] + offset_y)
            lane_line_end   = (lane.end_node.coordinates[0]   + offset_x,
                               lane.end_node.coordinates[1]   + offset_y)

            # lane.draw(screen)
            pygame.draw.line(screen, 'White', lane_line_start, lane_line_end, 5)
            # pygame.draw.line(screen, 'Red',lane.start_node.coordinates, lane.end_node.coordinates, 5)

            # Grab first corner in first loop
            if not corner_buffer_full:
                first_corner  = lane_line_start
                second_corner = lane_line_end
                corner_buffer_full = True

        ##### Right Loop - END #########

        # Calculate reverse offset for final line
        offset_x = -offset / math.sqrt(1 + perpendicular_slope ** 2)
        offset_y = perpendicular_slope * offset_x

        # Calculate new coordinates for final the offset line
        lane_line_start = (lane.start_node.coordinates[0] + offset_x,
                            lane.start_node.coordinates[1] + offset_y)
        lane_line_end = (lane.end_node.coordinates[0] + offset_x,
                            lane.end_node.coordinates[1] + offset_y)

        # Draw perpendicular start
        pygame.draw.line(screen,
                   'Blue',
                         first_corner,
                         lane_line_start,
                         5)

        # Draw perpendicular end
        pygame.draw.line(screen,
                         'Red',
                         second_corner,
                         lane_line_end,
                         5)

        # Prep corners for left
        first_corner  = lane_line_start
        second_corner = lane_line_end

    ############################################################################
    # RIGHT LANES:
        # Iterate and draw all left lanes
        if self.right_lanes:
            for lane in self.right_lanes:
                # Calculate individual lane offset based on distance between lanes
                offset = -25

                # Calculate Perpendicular slope
                perpendicular_slope = -1 / lane.slope if lane.slope != 0 else 1  # NEEDS FIX

                # Use a small delta to compute the perpendicular offset
                offset_x = offset / math.sqrt(1 + perpendicular_slope ** 2)
                offset_y = perpendicular_slope * offset_x

                # Calculate new coordinates for the offset lines
                lane_line_start = (lane.start_node.coordinates[0] + offset_x,
                                   lane.start_node.coordinates[1] + offset_y)
                lane_line_end = (lane.end_node.coordinates[0] + offset_x,
                                 lane.end_node.coordinates[1] + offset_y)

                # lane.draw(screen)
                pygame.draw.line(screen, 'White', lane_line_start, lane_line_end, 5)
                # pygame.draw.line(screen, 'Red',lane.start_node.coordinates, lane.end_node.coordinates, 5)

            ##### Left Loop - END #########

            # Calculate reverse offset for final line
            offset_x = -offset / math.sqrt(1 + perpendicular_slope ** 2)
            offset_y = perpendicular_slope * offset_x

            # Calculate new coordinates for final the offset line
            lane_line_start = (lane.start_node.coordinates[0] + offset_x,
                               lane.start_node.coordinates[1] + offset_y)
            lane_line_end = (lane.end_node.coordinates[0] + offset_x,
                             lane.end_node.coordinates[1] + offset_y)

            # Draw perpendicular start
            pygame.draw.line(screen,
                             'Red',
                             first_corner,
                             lane_line_end,
                             5)

            # Draw perpendicular end
            pygame.draw.line(screen,
                             'Blue',
                             second_corner,
                             lane_line_start,
                             5)

    ##################
        # Draw final lane to close the road
        pygame.draw.line(screen, 'White', lane_line_start, lane_line_end, 5)

