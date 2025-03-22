# camera.py
import pygame


class Camera:
    def __init__(self, viewport_width: int, viewport_height: int):

        # Locational Data - Center of Camera
        self.x_coord: int = 0
        self.y_coord: int = 0
        self.camera_scale: float = 1

        # Bounding Box
        self.bounding_box = pygame.Rect(0, 0, viewport_width, viewport_height)
        self.max_width    = viewport_width
        self.max_height   = viewport_height

        # Movement Attributes
        self.speed = 25
        self.max_scale = 80 # Percent Scale
        self.min_scale = 10 # Percent Scale

    def move(self, dx, dy):
        self.bounding_box.width  += dx
        self.bounding_box.height += dy
        center = self.bounding_box.center
        self.x_coord = center[0]
        self.y_coord = center[1]

    # def set_position(self, coordinate: [float, float]):
    #     self.x_coord = coordinate[0]
    #     self.y_coord = coordinate[1]

    def default_camera(self, map_width, map_height):
        """Centers the camera in the middle of the visible screen and sets a zoom of 50%."""
        # Set the camera to the center of the full map (half the width and height)
        self.move(map_width // 2, map_height // 2)

        # Set the camera zoom to 40%
        self.camera_scale = 40

    def move_camera(self, new_position: [float, float]):
        """ """
        self.set_position(new_position)

    def zoom_camera(self, user_scroll):
        """Adjusts "zoom" attribute, while it is called zoom it
           actually represents the scale of the bounding box relative
           to its max size. As the camera is scaled the bounding box
           should remain centered. """

        zoom_step = 1  # Adjust this for more/less sensitivity in zooming
        new_scale = self.camera_scale + user_scroll * zoom_step

        # Clamp zoom to reasonable values using min_scale and max_scale
        new_scale = max(self.min_scale, min(new_scale, self.max_scale))

        # If zoom level changes, adjust the bounding box size
        if new_scale != self.camera_scale:
            scale_factor = new_scale / self.camera_scale # Calculate how much the scale changes
            new_width = self.max_width   * scale_factor / 100 #
            new_height = self.max_height * scale_factor / 100 #

            # Update the bounding box dimensions
            self.bounding_box.width  = int(new_width)
            self.bounding_box.height = int(new_height)

            # Update the camera zoom level
            self.camera_scale = new_scale

            # Get the position before zooming
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Convert mouse position to world coordinates based on current zoom
            world_x = self.x_coord + (mouse_x - self.bounding_box.width  / 2) / self.camera_scale
            world_y = self.y_coord + (mouse_y - self.bounding_box.height / 2) / self.camera_scale

            # Apply the new zoom and adjust the camera position to maintain the same focal point
            # Recalculate world coordinates with the new zoom level
            self.x_coord = world_x - (mouse_x - self.bounding_box.width  / 2) / new_scale
            self.y_coord = world_y - (mouse_y - self.bounding_box.height / 2) / new_scale

            print('Zoom: ', str(self.camera_scale))