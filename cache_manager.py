# cache_manager.py

from collections import OrderedDict
import pygame

class CacheManager:
    def __init__(self, max_cache_size=200):
        self.global_cache = OrderedDict()
        self.max_cache_size = max_cache_size

    def get_scaled_surface(self, chunk, scale, scale_factor):
        """Retrieve or create a scaled surface for a given chunk."""
        scaled_size = (int(chunk.width * scale_factor), int(chunk.height * scale_factor))
        cache_key = (id(chunk), scale, scaled_size)

        # Check if the scaled version exists
        if cache_key in self.global_cache:
            # Move the accessed item to the end to mark it as recently used
            scaled_surface = self.global_cache.pop(cache_key)
            self.global_cache[cache_key] = scaled_surface
        else:
            # Scale the chunk surface and cache it
            scaled_surface = pygame.transform.scale(chunk.surface, scaled_size)
            self.global_cache[cache_key] = scaled_surface

        # Perform cache cleanup if necessary
        self.cleanup_cache()

        return scaled_surface

    def cleanup_cache(self):
        """Remove the least recently used items if the cache exceeds the limit."""
        while len(self.global_cache) > self.max_cache_size:
            self.global_cache.popitem(last=False)  # Pop the oldest item (FIFO)
            print("Cache cleanup: Removed oldest entry to free memory.")
