# roads.py
############################################################################################
import pygame

class Node:
    def __init__(self):
        self.pygame_surface = pygame.Surface((100,100))
        self.pygame_surface.fill('Red')
