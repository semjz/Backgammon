import pygame


class Piece:   
    def __init__(self, color, radius, center, number):
        self.color = color
        self.radius = radius
        self.center = center
        self.tri_num = number
    
    def draw_piece(self, surface):
        pygame.draw.circle(surface, self.color, self.center, self.radius)        
        
    def set_center(self, x, y):
        self.center = (x, y)

    def set_tri_num(self, number):
        self.tri_num = number

    

