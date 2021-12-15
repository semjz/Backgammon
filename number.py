import pygame
from constants import *

class Number:
    pygame.init()
    font = pygame.font.SysFont("Arial", 15)
    
    def __init__(self, value):
        self.value = value
        self.rendered_number = Number.font.render(str(value), True, BLACK)
        self.width = self.rendered_number.get_width()
        self.height = self.rendered_number.get_height()
        self.x_cord = 0
        self.y_cord = 0

    
    def mouse_and_number_collision(self, x_mouse, y_mouse):
        if self.width < 10:
            return (self.x_cord - 5 < x_mouse < self.x_cord + self.width + 5) and (self.y_cord < y_mouse < self.y_cord + self.height)
        else:
            return (self.x_cord - 2 < x_mouse < self.x_cord + self.width + 2) and (self.y_cord < y_mouse < self.y_cord + self.height)

    def set_cords(self, x, y):
        self.x_cord = x
        self.y_cord = y

    def draw_number(self, surface):
        surface.blit(self.rendered_number, (self.x_cord, self.y_cord))


