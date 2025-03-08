# main.py
######################################################################
import sys

import pygame
from sys import exit
import roads

def hello_world():
    print(f'Hello World :3')

def main():
    hello_world()

    # Setup Pygame
    pygame.init()
    screen = pygame.display.set_mode((800, 400))
    pygame.display.set_caption('Traffic Simulator')
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        myNode = roads.Node()
        screen.blit(myNode.pygame_surface, (5,5))


        # draw all our elemetns
        # update everythin
        pygame.display.update()
        clock.tick(60)


if __name__ == '__main__':
    main()