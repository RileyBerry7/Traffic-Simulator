# main.py
######################################################################
import sys

import pygame
from sys import exit
from roads import Node
from roads import Lane
from roads import Road
from vehicles import Car

def hello_world():
    print(f'Hello World :3')

SCREEN_WIDTH  = 1400
SCREEN_HEIGHT = 1000
SCREEN_COLOR  = (10, 10, 10)


# Main Loop
def main():

    # hello world test lol
    hello_world()

    # Setup Pygame
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.fill(SCREEN_COLOR)  # White background
    pygame.display.set_caption('Traffic Simulator')
    clock = pygame.time.Clock()

    vehicle_overlay = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    vehicle_overlay.fill((0, 0, 0, 0))



    # Road Testing
    lane4 = Lane((100, 350), (1000, 100))  # Original lane
    lane5 = Lane((110, 400), (1010, 150))  # Second parallel lane
    lane6 = Lane((120, 450), (1020, 200))  # Third parallel lane

    # Additional parallel lanes (with slight vertical offset)
    lane1 = Lane((1030, 250), (130, 500))  # Fourth parallel lane
    lane2 = Lane((1040, 300), (140, 550))  # Fifth parallel lane
    lane3 = Lane((1050, 350), (150, 600))  # Sixth parallel lane

    # Create the road with both right and left lanes (populate left lanes with the new parallel lanes)

    background = pygame.surface.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    background.fill((10, 10, 10))

    road = Road([lane1, lane2, lane3], [lane4, lane5, lane6])
    road.draw(background)

    # Car Testing
    car = Car(road, 'Right', 1)
    car.coordinates = lane2.end_node.coordinates
    counter = 0

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



        # Update Display
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()