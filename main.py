# main.py
######################################################################
import sys

import pygame
from sys import exit
from roads import Node
from roads import Lane
from roads import Road
from vehicles import Car
from intersections import four_way_stop



def hello_world():
    print(f'Hello World :3')

# Screen Setup
SCREEN_WIDTH  = 1400
SCREEN_HEIGHT = 1000
SCREEN_COLOR  = (10, 10, 10)

# Setup Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill(SCREEN_COLOR)  # White background
pygame.display.set_caption('Traffic Simulator')
clock = pygame.time.Clock()

# Overlay Setup
vehicle_overlay = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
vehicle_overlay.fill((0, 0, 0, 0))

# Load button images
build_img = pygame.image.load('GUI/build_img.png').convert_alpha()

class Button():
    def __init__(self, x, y, image, scale):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))

    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

create_button = Button(50, 50, build_img, 0.2)

########################################################################################################################
# Main Loop
def main():

    # hello world test lol
    hello_world()



    # # Left lanes

    left_lane2 = Lane(Node((1000, 400)), Node((100, 400)))  # Flipped start and end nodes for Lane 2
    left_lane1 = Lane(Node((1000, 450)), Node((100, 450)))  # Flipped start and end nodes for Lane 1
    left_lane0 = Lane(Node((1000, 500)), Node((100, 500)))

    # Right lanes
    right_lane0 = Lane(Node((100, 550)), Node((1000, 550)))  # Flipped start and end nodes for Lane 0
    right_lane1 = Lane(Node((100, 600)), Node((1000, 600)))  # Flipped start and end nodes for Lane 1
    # right_lane2 = Lane(Node((150, 600)), Node((1050, 350)))  # Flipped start and end nodes for Lane 2

    # Create the road with both right and left lanes (populate left lanes with the new parallel lanes)

    background = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((10, 10, 10))

    road = Road([right_lane0, right_lane1], [left_lane0, left_lane1])
    road.build_geometry()
    road.draw(background)

    # Car Testing
    car = Car(road, 'Right', 0)
    car.coordinates = right_lane0.start_node.coordinates
    counter = 0

    # Intersection Testing
    intersections = four_way_stop()

    intersections.left_input  = road.right_lanes[0].end_node
    intersections.right_output = Node((1020, 550))
    intersections.left_output  = road.left_lanes[0].start_node
    intersections.right_input  = Node((1020, 500))
    # lane7 = Lane(intersections.left_input, intersections.right_output)

    # intersections.calculate_lanes("right", "right")

########################################################################################################################
    # Game Loop
    while True:

        # Event_Checker Loop
        for event in pygame.event.get():

            # Event Quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Alter Display


        # Clear vehicles every frame
        vehicle_overlay = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        vehicle_overlay.fill((0, 0, 0, 0))

        counter +=  1
        car.acceleration = 0.025
        if counter > 200:
            car.acceleration = -0.05

        car.move()
        car.draw(vehicle_overlay)

        if car.acceleration == 0:
            car.color = 'Red'

        print(str(car.length_along_lane))
        # print(str(car.lane_ptr.length))  934

        # input("Press Enter to make the car move: ")
        screen.blit(background, (0,0))
        screen.blit(vehicle_overlay, (0, 0))


        intersections.draw(screen)
        create_button.draw()


        # Update Display
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()