# camera.py
import pygame

import pygame

class Camera:
    def __init__(self, viewport_width: int, viewport_height: int):
        # Bounding Box
        self.bounding_box = pygame.Rect(0, 0, viewport_width, viewport_height)
        self.min_width = viewport_width
        self.min_height = viewport_height

        # Locational Data - Center of Camera
        self.x_coord = self.bounding_box.centerx
        self.y_coord = self.bounding_box.centery

        self.camera_scale = 100 # Default is 100 %

        # Movement Attributes
        self.speed = 25
        self.max_scale = 1100
        self.min_scale = 100

    def move(self, dx, dy):
        """Translate the bounding box by dx, dy."""
        self.bounding_box.move_ip(dx, dy)
        self.x_coord = self.bounding_box.centerx
        self.y_coord = self.bounding_box.centery

    def default_camera(self, map_width, map_height):
        """Centers the camera in the middle of the visible screen and sets a zoom of 50%."""
        # Set camera to map center
        self.bounding_box.center = (map_width // 2, map_height // 2)
        self.x_coord, self.y_coord = self.bounding_box.center
        # Set camera zoom to 40%
        for _ in range(10):
            self.scale_camera(-1)

    def scale_camera(self, user_scroll):
        """Adjusts the camera zoom level and keeps it centered on the mouse position."""

        # Step size for zoom changes
        zoom_step = 10

        # Calculate new scale
        new_scale = self.camera_scale - (user_scroll * zoom_step) # Scroll down grows bounding box
        new_scale = min(self.max_scale, max(new_scale, self.min_scale)) # 100 <= new_scale <= 900

        # If Scale is new and valid within bounds
        if new_scale != self.camera_scale:

            # Calculate new scale
            scale_factor = new_scale / 100.0 # Always is >= 1

            # Calculate new dimensions
            new_width = int(self.min_width * scale_factor)
            new_height = int(self.min_height * scale_factor)

            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Convert mouse position to world coordinates before updating the scale
            world_x = self.x_coord + (mouse_x - self.bounding_box.width / 2) / (self.camera_scale / 100.0)
            world_y = self.y_coord + (mouse_y - self.bounding_box.height / 2) / (self.camera_scale / 100.0)

            # Update camera scale
            self.camera_scale = new_scale

            # Update bounding box dimensions
            self.bounding_box.width = new_width
            self.bounding_box.height = new_height

            # After the scale has been updated, adjust the camera to maintain the focal point under the mouse
            new_world_x = world_x - (mouse_x - self.bounding_box.width / 2) / (new_scale / 100.0)
            new_world_y = world_y - (mouse_y - self.bounding_box.height / 2) / (new_scale / 100.0)

            # Update the camera position
            self.x_coord = new_world_x
            self.y_coord = new_world_y
            self.bounding_box.center = (int(self.x_coord), int(self.y_coord))

            # print(f'Zoom: {self.camera_scale}, Bounding Box: {self.bounding_box}')

    def print_camera_bounding_box(self, screen: pygame.Surface):
        """Draws the camera's bounding box as a yellow rectangle on the screen."""
        # Draw the bounding box directly without scaling
        pygame.draw.rect(screen, 'Yellow', self.bounding_box, 2000)
        print(
            # f"Camera Bounding Box: Position=({self.bounding_box.x}, {self.bounding_box.y}), "
            # f"Width={self.bounding_box.width}, Height={self.bounding_box.height}, "
            # f"Scale={self.camera_scale}"
        )
