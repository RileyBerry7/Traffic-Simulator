# main.py
######################################################################
import sys

import pygame
from sys import exit

import gui
from road import Node
from road import Lane
from road import Road
from vehicles import Car
from intersections import four_way_stop
import user_tools
import world_map
from gui import Button

def hello_world():
    print(f'Hello World :3')

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

# Create a resizable window that fits within the screen
display_window = pygame.display.set_mode((window_width, window_height), pygame.RESIZABLE)
display_window.fill(SCREEN_COLOR)  # White background
pygame.display.set_caption('Traffic Simulator')
clock = pygame.time.Clock()

# World Map Setup
world = world_map.World_Map(window_width, window_height)
world.default_camera()

# Load Images
build_img = pygame.image.load('GUI/build_img.png').convert_alpha()

######################################################################################
# Setup GUI

# Button Testing
def action_build_road():
    """Changes two global state variables."""
    global waiting_for_clicks
    global next_action
    waiting_for_clicks = 2
    next_action = 'Build Road'


text = "Build Road"
font = pygame.font.Font(None, 30)
color = 'brown1'
hover = 'firebrick'
txt_color = 'antiquewhite2'
action = action_build_road
border = 7
button = gui.Button(45,20,
                    120, 50,
                    text, font, color, hover,
                    txt_color, action, border)

######################################################################################################
# Game State Variables
waiting_for_clicks = 0
next_action = ''
prev_clicks = []

########################################################################################################################
# Main Loop
def main():

    # hello_world()

    # Road_Builder Testing
    new_road = user_tools.build_road((3000,900),(12000,9000), "Six-Lane Road")
    new_road.build_geometry()
    new_road.draw(world.full_map)

    # Car Testing
    car = Car(new_road, 'Right', 0)
    car.coordinates = new_road.right_lanes[0].start_node.coordinates

########################################################################################################################
    # Game Loop
    while True:

        global prev_clicks
        global waiting_for_clicks
        global next_action

        # Display to Window
        display_window.blit(world.render_visible(), (0, 0))

        # Grab Mouse Position
        mouse_pos = pygame.mouse.get_pos()

        # Check for button hover
        button.check_hover(mouse_pos)
        button.draw(display_window)

        ###############################################################################
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

            # Event Left Click Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:

                if waiting_for_clicks > 0:
                    # Save Click Position
                    prev_clicks.append(mouse_pos)
                    if len(prev_clicks) > 20:   # Click Queue Max Capacity = 20 Positions
                        prev_clicks.pop()
                    waiting_for_clicks -=1
                if waiting_for_clicks == 0 and next_action == 'Build Road':
                    start = world.get_world_coordinates((prev_clicks[-2][0], prev_clicks[-2][1]))
                    end = world.get_world_coordinates((prev_clicks[-1][0], prev_clicks[-1][1]))
                    road_buffer = user_tools.build_road(start, end, 'Two-Lane Road')
                    road_buffer.build_geometry()
                    road_buffer.draw(world.full_map)
                    next_action = ''
                    print('Road should be build.')

                # Check if over button
                button.check_click(mouse_pos)

        # Get all currently pressed keys
        keys = pygame.key.get_pressed()

        # Move the camera based on key input
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= world.camera.speed
        if keys[pygame.K_s]:
            dy += world.camera.speed
        if keys[pygame.K_a]:
            dx -= world.camera.speed
        if keys[pygame.K_d]:
            dx += world.camera.speed

        world.camera.move(dx, dy)


            #####################################################################

        # Car Testing - Very Laggy!
        # Clear vehicles every frame
        # vehicle_overlay = pygame.surface.Surface((10500, 17200), pygame.SRCALPHA)
        # vehicle_overlay.fill((0, 0, 0, 0))
        # counter +=  1
        # car.acceleration = 25
        # if counter > 2000:
        #     car.acceleration = -0.05
        # car.move()
        # car.draw(vehicle_overlay)
        # if car.acceleration == 0:
        #     car.color = 'Red'
        # world.full_map.blit(vehicle_overlay, (0, 0))

        # Update Display
        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    main()