import pygame


class Piece:
    pygame.init()    
    def __init__(self, color, radius, center, number):
        self.color = color
        self.radius = radius
        self.center = center
        self.tri_number = number
    
    def draw_piece(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.radius)        
        
    def set_center(self, x, y):
        self.center = (x, y)

    def set_tri_number(self, number):
        self.tri_number = number
    
    def __str__(self):
        return f"Piece: (color = {self.color}, center = {self.center})"

