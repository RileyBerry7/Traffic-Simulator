# chunk.py

import pygame
from collections import deque


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

    def draw(self, screen, offset_x, offset_y, camera_rect):
        """Only draw the chunk if it's visible to the display_window."""

        if self.bounding_box.colliderect(camera_rect):
            if self.needs_update:
                self.process_updates()     # Process the queued updates when the chunk is visible
                self.needs_update = False  # Mark chunk as clean after processing

            # Draw the chunk surface to the screen at the correct position
            screen.blit(self.surface, (self.bounding_box.x - offset_x, self.bounding_box.y - offset_y))

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

