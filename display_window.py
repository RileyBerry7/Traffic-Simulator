# dislplay_window

import pygame

import camera
import node
import road
import world_map
import math

# Setup Pygame
pygame.init()

# Screen Setup
screen_info   = pygame.display.Info()
SCREEN_WIDTH  = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
SCREEN_COLOR  = 'White'  # Red color in RGB format - Should not be visible

# Reduce height slightly to fit within the visible screen area
WINDOW_HEIGHT = SCREEN_HEIGHT - 50  # Adjust this value if needed
WINDOW_WIDTH  = SCREEN_WIDTH
WINDOW_AREA   = WINDOW_WIDTH * WINDOW_HEIGHT
#
PARTITION_AMOUNT = 1000         # for 1080p, 10,000 partitions = 14.06 pixels of width
PARTITION_SIZE   = math.sqrt(WINDOW_AREA/PARTITION_AMOUNT)

# Calculate number of partitions in x and y
num_partitions_x = int(WINDOW_WIDTH  // PARTITION_SIZE)
num_partitions_y = int(WINDOW_HEIGHT // PARTITION_SIZE)

# Used as a unique partition that is used to represent road boundaries
class Road_Partition:
    def __init__(self, world_coordinates:[float, float], road_data:road.Road, node_data: node.Node):
        """ Represents a marked partition within the matrix, holds data releveant to the road whose, build point
             orbit the matricie is within.  """

        self.real_coordinates = world_coordinates
        self.road             = road_data
        self.node             = node_data

class Display_Window:

    def __init__(self):
        """ """
        # Create a resizable window that fits within the screen
        self.canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.RESIZABLE)
        self.canvas.fill(SCREEN_COLOR)  # White background
        pygame.display.set_caption('Traffic Simulator')

        # Camera
        self.camera = camera.Camera(WINDOW_WIDTH, WINDOW_HEIGHT)

        # World Map
        self.world = world_map.WorldMap(self.camera, 17200, 10300)
        self.world.init_chunk_map()

        # Default Camera Pos
        self.camera.default_camera(self.world.map_width, self.world.map_height)

        # Spatial Partitioning - Display Level
        # self.partition_matrix = [[0 for _ in range(num_partitions_x)] for _ in range(num_partitions_y)]

    def render_visible_chunks(self):
        """ """
        # Temporary Loops through entire dict of chunks
        visible_chunks = self.world.find_visible_chunks()
        for row_col in visible_chunks:
            self.world.draw_with_cache(self.canvas, row_col)
        print(str(len(visible_chunks)), ' Chunks Visible')

    def draw_camera_bounding_box(self):
        """Wrapper Method """
        self.camera.print_camera_bounding_box(self.canvas)

    def populate_road_partitions(self, orbit_radius=1000):
        """Using the road network's calculated partition points, this method given an orbit range will calculate and
            populate all of the partitions within range of any points orbit, passing in its relevant point data. """

        points = self.world.road_network.build_points # List of Tuples: ((x,y), Road, Node)

        for point in points:
            buffer_data    = self.calculate_partition_position(point[0])
            core_partition = Road_Partition(point[0], point[1], point[2])
            self.insert_partition(buffer_data, core_partition)
            self.fill_orbit(core_partition, orbit_radius)

    def insert_partition(self, coordinates: [float, float], road_partition: Road_Partition):

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

           Takes ????? Coordinates

           Returns: tuple: A tuple containing (row, column) of the partition in the partition matrix. """

        x, y = coordinates

        # Calculate the partition row (y-axis) and column (x-axis) based on the coordinates
        partition_x = int(x // PARTITION_SIZE)  # Integer division to get the column
        partition_y = int(y // PARTITION_SIZE)  # Integer division to get the row

        # Ensure the partition indices stay within the valid range of the matrix
        partition_x = min(partition_x, num_partitions_x - 1)  # Make sure we don't go out of bounds
        partition_y = min(partition_y, num_partitions_y - 1)  # Make sure we don't go out of bounds

        return partition_y, partition_x

    def fill_orbit(self, core_partition: Road_Partition, orbit_radius):
        """Populate all partitions within the orbit radius of the given core partition."""

        # Extract x and y
        coords  = core_partition.real_coordinates
        core_x = coords[0]
        core_y = coords[1]

        # Loop over the range of orbit_radius around the core partition
        for dx in range(-orbit_radius, orbit_radius + 1):

            for dy in range(-orbit_radius, orbit_radius + 1):

                # Calculate the distance from the core partition
                distance = math.sqrt(dx ** 2 + dy ** 2)

                # Only consider points within the radius, forming a rounded shape
                if distance <= orbit_radius:
                    # Calculate the matrix position (core_x + dx, core_y + dy)
                    x, y = core_x + dx, core_y + dy

                    # Check if the position is within valid bounds (optional, depending on your matrix size)
                    if self.is_valid_position(x, y):  # Assuming this function checks bounds
                        # Insert the core partition at the calculated position
                        self.insert_partition((x, y), core_partition)

    def is_valid_position(self, x, y):
        """Check if the given (x, y) position is within the valid partition bounds."""

        # Calculate the partition indices based on the partition size
        partition_x = x // PARTITION_SIZE
        partition_y = y // PARTITION_SIZE

        # Check if the partition indices are within the valid bounds of the partition grid
        if 0 <= partition_x < num_partitions_x and 0 <= partition_y < num_partitions_y:
            return True
        else:
            return False

