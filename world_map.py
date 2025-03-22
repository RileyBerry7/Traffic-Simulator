# world_map
import pygame
import math
import camera
import road_network
import user_tools
import chunk
from camera import Camera

# Plan to eventually make this class into an abstract
# map of rendering surface taht uses chunks or tiles
# to render more efficiently.
"""Currently this class is HYPER UNOPTIMIZED
   REWORK IN PROGRESS - IMPLEMENTING CHUNKS   """

class WorldMap:
    def __init__(self, cam: Camera, world_width: int, world_height: int):
        # temporary single massive canvas
        self.map_height = world_height
        self.map_width  = world_width
        self.full_map  = pygame.Surface((self.map_width, self.map_height))

        self.chunk_dict: dict[[int, int], chunk.Chunk] = {}
        self.chunk_size  = 200

        self.measurement_scale = 10
        self.cam = cam

        # self.visible_height   = display_height
        # self.visible_width    = display_width
        self.background_color = 'White'
        self.full_map.fill(self.background_color)

        # Road Network Object - contains Road and Lane Graphs
        self.road_network = road_network.Road_Network()

        # Testing
        # border = pygame.Surface((self.map_width, self.map_height))
        # border.fill('cornflowerblue')
        # background = pygame.Surface((self.map_width-400, self.map_height-400))
        # background.fill('chartreuse4')
        # center = pygame.Surface((200, 200))
        # center.fill('Red2')
        #
        # self.full_map.blit(border, (0,0))
        # self.full_map.blit(background,(200, 200))
        # self.full_map.blit(center, (self.map_width//2-50,self.map_height//2-50))

        # new_road = user_tools.build_road((self.map_width//2-550,self.map_height//2-200),
        #                                  (self.map_width//2+5000,self.map_height//2-200), "Two-Lane Road")
        # new_road.build_geometry()
        # new_road.draw(self.full_map)

    def init_chunk_map(self):
        """Initializes and populates the chunk dictionary with chunk objects."""

        inital_chunks = chunk.calculate_initial_chunks(self.map_width, self.map_height, self.chunk_size)
        for data in inital_chunks:
            fresh_chunk = data[1]
            fresh_chunk.default_red()
            self.chunk_dict[data[0]] = fresh_chunk

    def find_visible_chunks(self):
        """Find all visible chunks within the camera's bounding box."""

        # Calculate the bounds of the camera's visible area in world coordinates
        camera_left = self.cam.x_coord - self.cam.bounding_box.width / 2
        camera_top = self.cam.y_coord - self.cam.bounding_box.height / 2
        camera_right = camera_left + self.cam.bounding_box.width
        camera_bottom = camera_top + self.cam.bounding_box.height

        # Calculate the chunk row and column indices using floor division
        start_row = max(0, math.floor(camera_top / self.chunk_size))
        end_row = min(math.ceil(camera_bottom / self.chunk_size), self.map_height // self.chunk_size)

        start_col = max(0, math.floor(camera_left / self.chunk_size))
        end_col = min(math.ceil(camera_right / self.chunk_size), self.map_width // self.chunk_size)

        # Generate all visible chunk coordinates
        visible_chunks = [(row, col) for row in range(start_row, end_row) for col in range(start_col, end_col)]

        return visible_chunks

    def draw_build_points(self):
        """This Method visualizes the build points onto the world map,
             it is mainly for debugging purposes. """

        self.road_network.generate_build_points()
        # build_points = List( Tuple( Tuple(x,y), Road, Node) )
        build_points = self.road_network.build_points

        for point in build_points:
            coordinates = point[0]

            # Draw a circle onto world map
            pygame.draw.circle(self.full_map, (255, 0, 0), coordinates, 15)  # Red circle with radius 5

    def draw_road_graph(self):
        """ WARNING - WARNING - WARNING -
                HYPER INEFFICIENT
        Currently this draws Every Road when called. Needs Abstractions/Rework. """

        # for elem in self.road_network.road_dict:
        #     elem.draw(self.full_map)


    # def render_visible(self) -> pygame.Surface:
    #     """Returns rendered surface within the bounds of the camera.
    #        This surface should be drawn over the game window."""
    #
    #     # Convert zoom percentage to a scale factor
    #     zoom_factor = self.camera.zoom / 100
    #
    #     # Calculate the visible area's width and height based on the zoom factor
    #     zoomed_width = int(self.visible_width / zoom_factor)
    #     zoomed_height = int(self.visible_height / zoom_factor)
    #
    #     # Calculate the top-left corner of the visible window
    #     top_left_x = int(self.camera.x_coord - zoomed_width / 2)
    #     top_left_y = int(self.camera.y_coord - zoomed_height / 2)
    #
    #     # Clamp values to ensure they stay within the map boundaries
    #     top_left_x = max(0, min(top_left_x, self.map_width - zoomed_width))
    #     top_left_y = max(0, min(top_left_y, self.map_height - zoomed_height))
    #
    #     # Ensure we don't sample outside the valid range
    #     zoomed_width = min(zoomed_width, self.map_width - top_left_x)
    #     zoomed_height = min(zoomed_height, self.map_height - top_left_y)
    #
    #     # Create the sub-surface representing the visible portion of the map
    #     visible_window = self.full_map.subsurface(
    #         pygame.Rect(top_left_x, top_left_y, zoomed_width, zoomed_height)
    #     )
    #
    #     return pygame.transform.scale(visible_window, (self.visible_width, self.visible_height))
    #
    # def get_world_coordinates(self, visible_coords: tuple) -> tuple:
    #     """
    #     Converts coordinates in the visible window (screen space) to world map coordinates.
    #
    #     :param visible_coords: A tuple (x, y) representing the position in the visible window.
    #     :return: A tuple (world_x, world_y) representing the world map coordinates.
    #     """
    #     # Convert the visible window coordinates to the relative position within the visible window
    #     visible_x, visible_y = visible_coords
    #
    #     # Convert the screen (visible) coordinates to the zoomed-in world coordinates
    #     zoom_factor = self.camera.zoom / 100  # Get the zoom scale factor
    #
    #     # Calculate the offset in world space for the camera
    #     world_x = self.camera.x_coord - (self.visible_width / 2 - visible_x) / zoom_factor
    #     world_y = self.camera.y_coord - (self.visible_height / 2 - visible_y) / zoom_factor
    #
    #     return (world_x, world_y)

    def get_world_coordinates(self, visible_coords: tuple) -> tuple:
        """
        Converts coordinates in the visible window (screen space) to world map coordinates.

        :param visible_coords: A tuple (x, y) representing the position in the visible window.
        :return: A tuple (world_x, world_y) representing the world map coordinates.
        """
        # Convert the visible window coordinates to the relative position within the visible window
        visible_x, visible_y = visible_coords

        # Convert the screen (visible) coordinates to the zoomed-in world coordinates
        zoom_factor = self.cam.camera_scale / 100  # Get the zoom scale factor

        # Calculate the offset in world space for the camera
        world_x = self.cam.x_coord - (self.cam.bounding_box.width / 2 - visible_x) / zoom_factor
        world_y = self.cam.y_coord - (self.cam.bounding_box.height / 2 - visible_y) / zoom_factor

        return world_x, world_y