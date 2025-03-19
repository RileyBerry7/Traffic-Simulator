# dislplay_window

import pygame
import world_map

# Setup Pygame
pygame.init()

# Screen Setup
screen_info   = pygame.display.Info()
SCREEN_WIDTH  = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
SCREEN_COLOR  = ('Red')

# Reduce height slightly to fit within the visible screen area
window_height = SCREEN_HEIGHT - 50  # Adjust this value if needed
window_width  = SCREEN_WIDTH

class Display_Window:
    def __init__(self):
        # Create a resizable window that fits within the screen
        self.canvas = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
        self.canvas.fill(SCREEN_COLOR)  # White background
        pygame.display.set_caption('Traffic Simulator')

        # World Map
        self.world = world_map.World_Map(window_width, window_height)
        self.world.default_camera()

    # def setup_world_map(self):
    #     # World Map Setup
    #     world = world_map.World_Map(window_width, window_height)
    #     world.default_camera()