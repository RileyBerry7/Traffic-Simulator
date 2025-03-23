# chunk.py

import pygame
from collections import deque

import camera
import world_map


def calculate_initial_chunks(map_width, map_height, chunk_size):
    num_chunks_x = map_width // chunk_size
    num_chunks_y = map_height // chunk_size

    initial_chunks = []

    for row in range(num_chunks_y):
        for col in range(num_chunks_x):
            top_left_x = chunk_size * col
            top_left_y = chunk_size * row
            buffer_chunk = Chunk((top_left_x, top_left_y), chunk_size, chunk_size)
            initial_chunks.append(((row, col), buffer_chunk))

    return initial_chunks


class Chunk:
    def __init__(self, x_y:[float, float], width:int, height:int):
        self.spatial_data = x_y
        self.width        = width
        self.height       = height
        self.bounding_box = pygame.Rect(x_y[0], x_y[1], width, height)
        self.surface      = pygame.Surface((width, height))
        self.needs_update = False
        self.update_queue: deque[pygame.Surface] = deque()

        # Local cache per chunk
        # self.scaled_surfaces = OrderedDict()
        # self.max_cache_size = 5  # Adjust for memory needs

    def add_update(self, update_draw: pygame.Surface):
        """Adds update of most recent changes to the update queue. """

        if not self.needs_update:
            self.needs_update = True # Mark Update Queue as Non-Empty
            self.update_queue.append(update_draw) # Enqueue Latests Update

    def process_updates(self):
        """Apply all updates in queue to the chunk, empties the update queue. """

        while self.update_queue:
            update = self.update_queue.popleft()  # Grab Update
            update.blit(self.surface,(0, 0)) # Apply Update

        self.needs_update = False # Mark Update Queue as Empty

    def default_red(self):
        """Debugging method """
        # test_update = self.surface
        # test_update.fill('Red')
        # self.add_update(test_update)

        test_update = self.surface
        # Fill the surface with red color
        test_update.fill('Red')

        # Get the size of the surface
        width, height = test_update.get_size()

        # Draw a smaller rectangle in the middle (a hole in the middle to keep it unaltered)
        margin = 10  # The thickness of the border
        inner_rect = (margin, margin, width - 2 * margin, height - 2 * margin)
        pygame.draw.rect(test_update, 'White', inner_rect)  # Draw white inner rectangle to keep middle unaltered

        # Update the surface with the border and unaltered middle
        self.add_update(test_update)

    # def draw(self, screen, cam):
    #     """ If the calling chunk is within the bounding box of the camera, it will be drawn to passed in surface
    #         at a scale and position relative to how it lies within the camera's bounding box."""
    #
    #     scale_factor = cam.camera_scale / 100.0
    #     scaled_size = (int(self.width * scale_factor), int(self.height * scale_factor))
    #     cache_key = (cam.camera_scale, scaled_size)
    #
    #     # Check local cache first
    #     if cache_key in self.scaled_surfaces:
    #         scaled_surface = self.scaled_surfaces.pop(cache_key)
    #         self.scaled_surfaces[cache_key] = scaled_surface
    #     elif cache_key in self.world.global_cache:
    #         # Load from global cache if not in local
    #         scaled_surface = self.world.global_cache.pop(cache_key)
    #         self.scaled_surfaces[cache_key] = scaled_surface
    #     else:
    #         # Scale the chunk and store in the local cache
    #         scaled_surface = pygame.transform.scale(self.surface, scaled_size)
    #         self.scaled_surfaces[cache_key] = scaled_surface
    #
    #     # Manage chunk cache size
    #     if len(self.scaled_surfaces) > self.max_cache_size:
    #         old_key, old_surface = self.scaled_surfaces.popitem(last=False)
    #         self.world.global_cache[old_key] = old_surface
    #
    #     # Draw
    #     chunk_x = (self.spatial_data[0] - cam.bounding_box.x) * scale_factor + (cam.max_width / 2) - (
    #                 cam.bounding_box.width / 2)
    #     chunk_y = (self.spatial_data[1] - cam.bounding_box.y) * scale_factor + (cam.max_height / 2) - (
    #                 cam.bounding_box.height / 2)
    #     screen.blit(scaled_surface, (chunk_x, chunk_y))

    # def invalidate_cache(self):
    #     self.scaled_surfaces.clear()