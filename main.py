# main.py

import sys

import pygame
from sys import exit

import gui
from node import Node
from road import Lane
from road import Road
from vehicles import Car
import user_tools
import world_map
from gui import Button
import display_window

def hello_world():
    print(f'Hello World :3')


# Setup Display Window / Pygame
display_window = display_window.Display_Window()

# Setup Time
clock = pygame.time.Clock()

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

    # Temporary
    display_window.world.draw_build_points()
    display_window.populate_road_partitions()

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


    ######################################################################################
    # Testing
    # Road_Builder Testing
    new_road = user_tools.build_road((3000,900),(12000,9000), "Six-Lane Road")
    new_road.build_geometry()
    new_road.draw(display_window.world.full_map)

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
        display_window.canvas.blit(display_window.world.render_visible(), (0, 0))

        # Grab Mouse Position
        mouse_pos = pygame.mouse.get_pos()

        # Check for button hover
        button.check_hover(mouse_pos)
        button.draw(display_window.canvas)

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
                display_window.world.zoom_camera(wheel_scroll)

            # Event Left Click Mouse
            if event.type == pygame.MOUSEBUTTONDOWN:

                if waiting_for_clicks > 0:
                    # Save Click Position
                    prev_clicks.append(mouse_pos)
                    if len(prev_clicks) > 20:   # Click Queue Max Capacity = 20 Positions
                        prev_clicks.pop()
                    waiting_for_clicks -=1
                if waiting_for_clicks == 0 and next_action == 'Build Road':
                    start = display_window.world.get_world_coordinates((prev_clicks[-2][0], prev_clicks[-2][1]))
                    end = display_window.world.get_world_coordinates((prev_clicks[-1][0], prev_clicks[-1][1]))
                    # road_buffer = user_tools.build_road(start, end, 'Two-Lane Road')
                    # road_buffer.build_geometry()
                    # road_buffer.draw(display_window.world.full_map)
                    next_action = ''
                    # Road Network Building
                    display_window.world.road_network.add_road(start, end, 'Two-Lane Road')
                    display_window.world.draw_road_graph()
                    # print('Road should be build.')

                # Check if over button
                button.check_click(mouse_pos)

        # Get all currently pressed keys
        keys = pygame.key.get_pressed()

        # Move the camera based on key input
        dx, dy = 0, 0
        if keys[pygame.K_w]:
            dy -= display_window.world.camera.speed
        if keys[pygame.K_s]:
            dy += display_window.world.camera.speed
        if keys[pygame.K_a]:
            dx -=  display_window.world.camera.speed
        if keys[pygame.K_d]:
            dx +=  display_window.world.camera.speed

        display_window.world.camera.move(dx, dy)


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