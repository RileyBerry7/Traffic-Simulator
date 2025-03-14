# vehicles.py

import ctypes
import math

import pygame.draw

from road import Road
from road import Lane


class Vehicle:
    def __init__(self, current_road: Road, direction: str='Right', lane_index: int=0, length_along_lane:float=0):
        # Physical attributes
        self.length       = 10
        self.top_speed    = 6
        self.acceleration = 0
        self.velocity     = 0
        self.is_hov = True
        self.color  = 'Green'

        # Relative Road Data
        self.road_ptr       = current_road
        if direction == 'Right':
            self.lane_ptr       = current_road.right_lanes[lane_index]
            self.slope          = current_road.right_lanes[lane_index].slope
        elif direction == 'Left':
            self.lane_ptr       = current_road.left_lanes[lane_index]
            self.slope          = current_road.left_lanes[lane_index].slope

        self.lane_index     = lane_index
        self.lane_direction = direction

        self.length_along_lane = length_along_lane

        # Real Location Data
        self.coordinates = (0, 0)


    # def set_position_in_lane(self, length_traveled):
    #     self.length_along_lane = length_traveled
    #
    #     # Compute movement in x and y direction
    #     dx = length_to_add / math.sqrt(1 + self.slope ** 2)
    #     dy = self.slope * dx  # Maintain the same direction
    #
    #     # Update position
    #     self.coordinates = (self.coordinates[0] + dx, self.coordinates[1] + dy)
    #     self.length_along_lane += length_traveled


    def set_slope(self, slope):
        self.slope = slope

    def move(self):
        # Update velocity based on acceleration

        self.velocity += self.acceleration

        if self.velocity > self.top_speed:
            self.velocity = self.top_speed
        if self.velocity < 0:
            self.velocity = 0
            self.acceleration = 0

        # Compute movement in x and y direction
        dx = self.velocity / math.sqrt(1 + self.slope ** 2)
        dy = self.slope * dx  # Maintain the same direction

        # Update position
        self.length_along_lane += math.sqrt(dx**2 + dy**2) # Total distance traveled
        self.coordinates = (self.coordinates[0] + dx, self.coordinates[1] + dy)


    def draw(self, screen):
        pygame.draw.circle(screen, self.color,self.coordinates, 15)


class Car(Vehicle):
    def __init__(self, current_road: Road, direction: str='Right', lane_index: int=0):
        super().__init__(current_road, direction, lane_index)


    # def draw(self, screen):
    #     super().draw(screen)
