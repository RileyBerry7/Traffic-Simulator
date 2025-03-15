# main.py
######################################################################
import sys

import pygame
from sys import exit
from road import Node
from road import Lane
from road import Road
from vehicles import Car
from intersections import four_way_stop
import user_tools
import world_map




def hello_world():
    print(f'Hello World :3')





# Setup Pygame
pygame.init()



# Screen Setup
# screen = pygame.display.set_mode((100, 100))

screen_info   = pygame.display.Info()
SCREEN_WIDTH  = screen_info.current_w
SCREEN_HEIGHT = screen_info.current_h
SCREEN_COLOR  = (10, 10, 10)

# Reduce height slightly to fit within the visible screen area
window_height = SCREEN_HEIGHT - 50  # Adjust this value if needed
window_width  = SCREEN_WIDTH

# Create a resizable window that fits within the screen
display_window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
display_window.fill(SCREEN_COLOR)  # White background
pygame.display.set_caption('Traffic Simulator')
clock = pygame.time.Clock()

# Overlay Setup
vehicle_overlay = pygame.surface.Surface((window_width, window_height), pygame.SRCALPHA)
vehicle_overlay.fill((0, 0, 0, 0))

# World Map Setup
world = world_map.World_Map(window_width, window_height)
world.default_camera()

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
        display_window.blit(self.image, (self.rect.x, self.rect.y))

create_button = Button(50, 50, build_img, 0.2)

########################################################################################################################
# Main Loop
def main():

    # hello world test lol
    hello_world()

    new_road = user_tools.build_road((3000,900),(12000,9000), "Six-Lane Road")

    # # Left lanes

    left_lane2 = Lane(Node((1000, 400)), Node((100, 400)))  # Flipped start and end nodes for Lane 2
    left_lane1 = Lane(Node((1000, 450)), Node((100, 450)))  # Flipped start and end nodes for Lane 1
    left_lane0 = Lane(Node((1000, 500)), Node((100, 500)))

    # Right lanes
    right_lane0 = Lane(Node((100, 550)), Node((1000, 550)))  # Flipped start and end nodes for Lane 0
    right_lane1 = Lane(Node((100, 600)), Node((1000, 600)))  # Flipped start and end nodes for Lane 1
    # right_lane2 = Lane(Node((150, 600)), Node((1050, 350)))  # Flipped start and end nodes for Lane 2

    # Create the road with both right and left lanes (populate left lanes with the new parallel lanes)

    background = pygame.surface.Surface((window_width, window_height))
    background.fill((10, 10, 10))

    road = Road([right_lane0, right_lane1], [left_lane0, left_lane1], "Two-Lane Road" )
    road.build_geometry()
    road.draw(world.full_map)

    new_road.build_geometry()
    new_road.draw(world.full_map)

    # Car Testing
    car = Car(new_road, 'Right', 0)
    car.coordinates = new_road.right_lanes[0].start_node.coordinates
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

            # Event Scroll
            if event.type == pygame.MOUSEWHEEL:
                wheel_scroll = event.y
                world.zoom_camera(wheel_scroll)
                # display_window.blit(world_map.render_visible(), (0, 0))

        # Alter Display


        # Clear vehicles every frame
        vehicle_overlay = pygame.surface.Surface((10500, 17200), pygame.SRCALPHA)
        vehicle_overlay.fill((0, 0, 0, 0))

        # counter +=  1
        car.acceleration = 25
        # if counter > 2000:
        #     car.acceleration = -0.05

        car.move()
        car.draw(vehicle_overlay)

        if car.acceleration == 0:
            car.color = 'Red'

        # print(str(car.length_along_lane))
        # print(str(car.lane_ptr.length))  934

        # input("Press Enter to make the car move: ")
        # display_window.blit(background, (0, 0))
        # display_window.blit(vehicle_overlay, (0, 0))


        intersections.draw(display_window)
        create_button.draw()
        #
        world.full_map.blit(vehicle_overlay, (0, 0))
        display_window.blit(world.render_visible(), (0, 0))



        # Update Display
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()