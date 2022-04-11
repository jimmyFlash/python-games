import pygame

"""
class represents the player object 
in this case just a rectangle with defined color and position on screen 
"""


class Player:
    def __init__(self, x, y, p_width, p_height, color):
        self.x = x
        self.y = y
        self.height = p_height
        self.width = p_width
        self.color = color
        self.rect = (self.x, self.y, self.width, self.height)
        self.vel = 1  # amount of pixels to offset per key press

    # render the rectangle on screen
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    # update the position base don arrow key presses in the four directions
    def move(self):

        key_pressed = pygame.key.get_pressed()

        if key_pressed[pygame.K_LEFT]:
            self.x -= self.vel
        if key_pressed[pygame.K_RIGHT]:
            self.x += self.vel
        if key_pressed[pygame.K_UP]:
            self.y -= self.vel
        if key_pressed[pygame.K_DOWN]:
            self.y += self.vel

        self.update()

    # update rectangle object offset properties on screen
    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)
