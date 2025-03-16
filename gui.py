# gui.py
# contains all gui code

import pygame

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color, text_color, action=None, border_radius=10):
        """
        Creates a button object.

        :param x: X position of the button.
        :param y: Y position of the button.
        :param width: Width of the button.
        :param height: Height of the button.
        :param text: Text to display on the button.
        :param font: Pygame font object.
        :param color: Default button color.
        :param hover_color: Button color when hovered over.
        :param text_color: Color of the button text.
        :param action: Function to execute when clicked.
        :param border_radius: Roundness of the button corners.
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.action = action
        self.border_radius = border_radius
        self.is_hovered = False

    def draw(self, screen):
        """Draws the button with hover effect."""
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, current_color, self.rect, border_radius=self.border_radius)

        # Render text
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def check_hover(self, mouse_pos):
        """Checks if the mouse is hovering over the button."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def check_click(self, mouse_pos):
        """Checks if the button is clicked and triggers the action."""
        if self.rect.collidepoint(mouse_pos) and self.action:
            self.action()

# Example usage:
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    font = pygame.font.Font(None, 36)

    def button_clicked():
        print("Button clicked!")

    button = Button(100, 100, 200, 60, "Click Me", font, (50, 150, 255), (30, 130, 235), (255, 255, 255), button_clicked)

    running = True
    while running:
        screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()

        button.check_hover(mouse_pos)
        button.draw(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                button.check_click(mouse_pos)

        pygame.display.flip()

    pygame.quit()
