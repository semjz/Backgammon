import pygame


class Piece:
    pygame.init()    
    def __init__(self, color, radius, center):
        self.color = color
        self.radius = radius
        self.center = center
    
    def draw_piece(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.radius)        
        
    def set_center(self, x, y):
        self.center = (x, y)
    
    def __str__(self):
        return f"Piece: (color = {self.color}, center = {self.center})"

