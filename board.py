import pygame
import pygame.gfxdraw
from piece import Piece
from number import Number
from constants import *


class Board:
    pygame.init()
    
    @staticmethod
    def get_paddings(number):
        width_padding = (50 - number.width) / 2
        height_padding = (50 - number.height) / 2   
        return width_padding, height_padding

    def __init__(self):
        # This variable contains the structure of pieces objects on the baord.
        self.board_list = [[] for i in range(24)]
        self.numbers = []
        self.width_shift = WIDTH - 750
        self.triangle_cicle_center = self.get_triangle_cicle_center()
    
    def __str__(self):
        numbers = []
        for num in self.numbers:
            numbers.append(num.__str__())
        return f"{numbers}"

    def shift_right(self, input):
        return input + self.width_shift / 2

    def triangle_is_not_empty(self, tri_number):
        return len(self.board_list[tri_number - 1]) > 0

    def triangle_is_not_full(self, tri_number):
        return len(self.board_list[tri_number - 1]) < 5

    # first circle center for each triangle
    def get_triangle_cicle_center(self):
        triangle_cicle_center = {}
        for i in range(1, 13):
            if i > 6:
                triangle_cicle_center[i] = (self.shift_right(75) + 50 * (i - 1) + 50, 575)    
            else:
                triangle_cicle_center[i] = (self.shift_right(75) + 50 * (i - 1), 575)
        
        for i in range (24, 12, -1):
            if i < 19:
                triangle_cicle_center[i] = (self.shift_right(75) + 50 * (24 - i) + 50, 75)
            else:
                triangle_cicle_center[i] = (self.shift_right(75) + 50 * (24 - i), 75)
             
        return triangle_cicle_center     
           
    def draw_background(self, surface):
        surface.fill(BACKGROUND_COLOR)

    def draw_rectangles(self, surface):
        self.draw_background(surface)
        # left border
        pygame.draw.rect(surface, GRAY, (0, 0, self.shift_right(50), HEIGHT))
        # right border
        pygame.draw.rect(surface, GRAY, (self.shift_right(700), 0, self.shift_right(50), HEIGHT))
        # middle border
        pygame.draw.rect(surface, GRAY, (self.shift_right(350), 0, 50, HEIGHT))
        # top border
        pygame.draw.rect(surface, GRAY, (0, 0, WIDTH, 50))
        # bottom border
        pygame.draw.rect(surface, GRAY, (0, 600, WIDTH, 50))

        # middle line
        pygame.draw.line(surface, BLACK, (WIDTH/2, 0),(WIDTH/2, HEIGHT))

    def creat_numbers(self, surface):
        # bottom row numbers
        for i in range(1,7):
            number = Number(i)
            width_padding, height_padding = self.get_paddings(number)
            x_number, y_number = self.shift_right(50 + width_padding + 50 * (i - 1)), 600 + height_padding
            number.set_cords(x_number, y_number)          
            self.numbers.append(number)
    
        
        for i in range(7,13):
            number = Number(i)
            width_padding, height_padding = self.get_paddings(number)
            x_number, y_number = self.shift_right(400 + width_padding + 50 * (i - 7)), 600 + height_padding
            number.set_cords(x_number, y_number)  
            self.numbers.append(number)

        
        # top row numbers
        for i in range(13,19):
            number = Number(i)
            width_padding, height_padding = self.get_paddings(number)
            x_number, y_number = self.shift_right(400 + width_padding + 50 * (18 - i)), height_padding
            number.set_cords(x_number, y_number)
            self.numbers.append(number)

        
        for i in range(19,25):
            number = Number(i)
            width_padding, height_padding = self.get_paddings(number)
            x_number, y_number = self.shift_right(50 + width_padding + 50 * (24 - i)), height_padding
            number.set_cords(x_number, y_number)
            self.numbers.append(number)    

    def draw_triangle(self, surface):
        for i in range(1,7):
            if i % 2 == 0:
                color = TAN
            else:
                color = DARK_ORANGE3

            # down triangles
            pygame.gfxdraw.aapolygon(surface, [(self.shift_right(i*50) , 600), (self.shift_right((i+1)*50) , 600), (self.shift_right(75 + (i-1)*50), 350)], color)
          
            pygame.gfxdraw.aapolygon(surface, [(self.shift_right((i+7)*50), 600), (self.shift_right((i+8)*50), 600), (self.shift_right(425 + (i-1)*50), 350)], color)

            
            pygame.gfxdraw.filled_polygon(surface, [(self.shift_right(i*50) , 600), (self.shift_right((i+1)*50) , 600), (self.shift_right(75 + (i-1)*50) , 350)], color)
          
            pygame.gfxdraw.filled_polygon(surface, [(self.shift_right((i+7)*50) , 600), (self.shift_right((i+8)*50) , 600), (self.shift_right(425 + (i-1)*50), 350)], color)
            

        for i in range(6,0,-1):

            if i % 2 == 0:
                color = DARK_ORANGE3
            else:
                color = TAN
                
            # top triangles
            pygame.gfxdraw.aapolygon(surface, [(self.shift_right(i*50), 50), (self.shift_right((i+1)*50), 50), (self.shift_right(75 + (i-1)*50), 300)], color)
          
            pygame.gfxdraw.aapolygon(surface, [(self.shift_right((i+7)*50), 50), (self.shift_right((i+8)*50), 50), (self.shift_right(425 + (i-1)*50), 300)], color)

            # filled top triangles
            pygame.gfxdraw.filled_polygon(surface, [(self.shift_right(i*50), 50), (self.shift_right((i+1)*50), 50), (self.shift_right(75 + (i-1)*50), 300)], color)
          
            pygame.gfxdraw.filled_polygon(surface, [(self.shift_right((i+7)*50), 50), (self.shift_right((i+8)*50), 50), (self.shift_right(425 + (i-1)*50), 300)], color)

    def create_pieces_list(self):
        # Set up white pieces
        # Line 1
        for i in range(5):
            piece = Piece(WHITE, 25, (self.shift_right(75), 575 - i * 50))
            self.board_list[0].append(piece)
        # Line 12
        for i in range(2):
            piece = Piece(WHITE, 25, (self.shift_right(675), 575 - i * 50))
            self.board_list[11].append(piece)
        # Line 18
        for i in range(5):
            piece = Piece(WHITE, 25, (self.shift_right(425), 75 + i * 50))
            self.board_list[17].append(piece)
        # line 20
        for i in range(3):
            piece = Piece(WHITE, 25, (self.shift_right(275), 75 + i * 50))
            self.board_list[19].append(piece)

        # Set up black pieces
        # line 5
        for i in range(3):
            piece = Piece(BLACK, 25, (self.shift_right(275), 575 - i * 50))
            self.board_list[4].append(piece)
        # line 7
        for i in range(5):
            piece = Piece(BLACK, 25, (self.shift_right(425), 575 - i * 50))
            self.board_list[6].append(piece)
        # line 13
        for i in range(2):
            piece = Piece(BLACK, 25, (self.shift_right(675), 75 + i * 50))
            self.board_list[12].append(piece)
        # line 24
        for i in range(5):
            piece = Piece(BLACK, 25, (self.shift_right(75), 75 + i * 50))
            self.board_list[23].append(piece)

    
    # maybe I can rework and clean this function
    def move(self, current_tri_number, dest_tri_number):
        if current_tri_number is not None and dest_tri_number is not None:
            if self.triangle_is_not_empty(current_tri_number) and self.triangle_is_not_full(dest_tri_number):
                piece = self.board_list[current_tri_number-1].pop()
                if dest_tri_number < 13:
                    des_x = self.triangle_cicle_center[dest_tri_number][0]
                    dest_y = self.triangle_cicle_center[dest_tri_number][1] - len(self.board_list[dest_tri_number - 1]) * 50
                else:
                    des_x = self.triangle_cicle_center[dest_tri_number][0]
                    dest_y = self.triangle_cicle_center[dest_tri_number][1] + len(self.board_list[dest_tri_number - 1]) * 50
                piece.set_center(des_x, dest_y)
                self.board_list[dest_tri_number - 1].append(piece)


    def draw(self, surface):
        self.draw_background(surface)
        self.draw_rectangles(surface)
        for num in self.numbers:
            num.draw_number(surface)
        self.draw_triangle(surface)
        for i in range(24):
            for piece in self.board_list[i]:
                piece.draw_piece(surface)

    # maybe I can rework and clean this function
    def find_tri_number(self, x_mouse, y_mouse):
        for num in self.numbers:
            if(num.mouse_and_number_collision_is_detected(x_mouse, y_mouse)):
                return num.value
        return None
