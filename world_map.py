# world_map
import pygame
import road_network
import camera
import user_tools


# Plan to eventually make this class into an abstract
# map of rendering surface taht uses chunks or tiles
# to render more efficiently.

class World_Map:
    def __init__(self, display_width: int, display_height: int):
        # temporary single massive canvas
        self.map_height = 10300
        self.map_width  = 17200
        self.full_map  = pygame.Surface((self.map_width, self.map_height))
        self.measurement_scale = 10
        self.camera = camera.Camera()

        self.visible_height   = display_height
        self.visible_width    = display_width
        self.background_color = 'White'
        self.full_map.fill(self.background_color)

        self.road_network = road_network.Road_Network()

        # Testing
        border = pygame.Surface((self.map_width, self.map_height))
        border.fill('cornflowerblue')
        background = pygame.Surface((self.map_width-400, self.map_height-400))
        background.fill('chartreuse4')
        center = pygame.Surface((200, 200))
        center.fill('Red2')

        self.full_map.blit(border, (0,0))
        self.full_map.blit(background,(200, 200))
        self.full_map.blit(center, (self.map_width//2-50,self.map_height//2-50))

        new_road = user_tools.build_road((self.map_width//2-550,self.map_height//2-200),
                                         (self.map_width//2+5000,self.map_height//2-200), "Two-Lane Road")
        new_road.build_geometry()
        new_road.draw(self.full_map)

    def default_camera(self):
        """Centers the camera in the middle of the visible screen and sets a zoom of 50%."""
        # Set the camera to the center of the full map (half the width and height)
        self.camera.x_coord = self.map_width // 2
        self.camera.y_coord = self.map_height // 2

        # Set the camera zoom to 50%
        self.camera.zoom = 50  # Zoom is now set to 50%

        # Update the visible window based on the zoom level
        # self.visible_width = int(self.full_map.get_width() * self.camera.zoom)
        # self.visible_height = int(self.full_map.get_height() * self.camera.zoom)

        # Optionally, call render_visible after zooming to update the view
        self.render_visible()
    def move_camera(self, new_position: [float, float]):
        self.camera.set_position(new_position)
        self.render_visible()

    def zoom_camera(self, user_scroll):
        """ Adjusts the zoom level while keeping the camera centered at the same world position. """
        zoom_step = 10  # Adjust this if zooming feels too fast or slow
        new_zoom = self.camera.zoom + user_scroll * zoom_step

        # Clamp zoom to reasonable values
        new_zoom = max(1, min(new_zoom, 100))

        # Get the position before zooming
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Convert mouse position to world coordinates
        world_x = self.camera.x_coord + (mouse_x - self.visible_width / 2) / self.camera.zoom
        world_y = self.camera.y_coord + (mouse_y - self.visible_height / 2) / self.camera.zoom

        # Apply the new zoom
        self.camera.zoom = new_zoom

        # Adjust camera position to maintain the same focal point
        self.camera.x_coord = world_x - (mouse_x - self.visible_width / 2) / self.camera.zoom
        self.camera.y_coord = world_y - (mouse_y - self.visible_height / 2) / self.camera.zoom

        # self.render_visible()

    def render_visible(self) -> pygame.Surface:
        """Returns rendered surface within the bounds of the camera.
           This surface should be drawn over the game window."""

        # Convert zoom percentage to a scale factor
        zoom_factor = self.camera.zoom / 100

        # Calculate the visible area's width and height based on the zoom factor
        zoomed_width = int(self.visible_width / zoom_factor)
        zoomed_height = int(self.visible_height / zoom_factor)

        # Calculate the top-left corner of the visible window
        top_left_x = int(self.camera.x_coord - zoomed_width / 2)
        top_left_y = int(self.camera.y_coord - zoomed_height / 2)

        # Clamp values to ensure they stay within the map boundaries
        top_left_x = max(0, min(top_left_x, self.map_width - zoomed_width))
        top_left_y = max(0, min(top_left_y, self.map_height - zoomed_height))

        # Ensure we don't sample outside the valid range
        zoomed_width = min(zoomed_width, self.map_width - top_left_x)
        zoomed_height = min(zoomed_height, self.map_height - top_left_y)

        # Create the sub-surface representing the visible portion of the map
        visible_window = self.full_map.subsurface(
            pygame.Rect(top_left_x, top_left_y, zoomed_width, zoomed_height)
        )

        return pygame.transform.scale(visible_window, (self.visible_width, self.visible_height))

    def get_world_coordinates(self, visible_coords: tuple) -> tuple:
        """
        Converts coordinates in the visible window (screen space) to world map coordinates.

        :param visible_coords: A tuple (x, y) representing the position in the visible window.
        :return: A tuple (world_x, world_y) representing the world map coordinates.
        """
        # Convert the visible window coordinates to the relative position within the visible window
        visible_x, visible_y = visible_coords

        # Convert the screen (visible) coordinates to the zoomed-in world coordinates
        zoom_factor = self.camera.zoom / 100  # Get the zoom scale factor

        # Calculate the offset in world space for the camera
        world_x = self.camera.x_coord - (self.visible_width / 2 - visible_x) / zoom_factor
        world_y = self.camera.y_coord - (self.visible_height / 2 - visible_y) / zoom_factor

        return (world_x, world_y)