# dislplay_window

import pygame

import road
import world_map
import math

# Setup Pygame
pygame.init()

# Screen Setup
screen_info   = pygame.display.Info()
SCREEN_WIDTH  = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
SCREEN_COLOR  = (255, 0, 0)  # Red color in RGB format - Should not be visible

# Reduce height slightly to fit within the visible screen area
WINDOW_HEIGHT = SCREEN_HEIGHT - 50  # Adjust this value if needed
WINDOW_WIDTH  = SCREEN_WIDTH
WINDOW_AREA   = WINDOW_WIDTH * WINDOW_HEIGHT
#
PARTITION_AMOUNT = 1000         # for 1080p, 10,000 partitions = 14.06 pixels of width
PARTITION_SIZE   = math.sqrt(WINDOW_AREA/PARTITION_AMOUNT)

# Calculate number of partitions in x and y
num_partitions_x = int(WINDOW_WIDTH // PARTITION_SIZE)
num_partitions_y = int(WINDOW_HEIGHT // PARTITION_SIZE)

# Used as a unique partition that is used to represent road boundaries
class Road_Partition:
    def __init__(self, road: road.Road, distance_along:float):
        self.road = road
        self.distance_along = distance_along

class Display_Window:
    def __init__(self):
        # Create a resizable window that fits within the screen
        self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        self.canvas.fill(SCREEN_COLOR)  # White background
        pygame.display.set_caption('Traffic Simulator')

        # World Map
        self.world = world_map.World_Map(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.world.default_camera()

        # Spatial Partitioning - Display Level
        self.partition_matrix = [[0 for _ in range(num_partitions_x)] for _ in range(num_partitions_y)]

    def insert_partition(self, coordinates: [float, float], road_partition: Road_Partition=None):

        row_column = self.calculate_partition_position(coordinates)

        # If road exists add its partition
        if road_partition:
            self.partition_matrix [row_column[0]][row_column[1]] = road_partition # This my throw an Error

    def reset_partitions(self):
        """"""
        # Fill with zeroes
        self.partition_matrix = [[0 for _ in range(num_partitions_x)] for _ in range(num_partitions_y)]


    def calculate_partition_position(self, coordinates: [float, float]) -> [float, float]:
        """
           Calculate the partition position (row, column) in the partition matrix
           based on the given (x, y) coordinates.

           Returns: tuple: A tuple containing (row, column) of the partition in the partition matrix. """

        x, y = coordinates

        # Calculate the partition row (y-axis) and column (x-axis) based on the coordinates
        partition_x = int(x // PARTITION_SIZE)  # Integer division to get the column
        partition_y = int(y // PARTITION_SIZE)  # Integer division to get the row

        # Ensure the partition indices stay within the valid range of the matrix
        partition_x = min(partition_x, num_partitions_x - 1)  # Make sure we don't go out of bounds
        partition_y = min(partition_y, num_partitions_y - 1)  # Make sure we don't go out of bounds

        return partition_y, partition_x


