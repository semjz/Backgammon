import pygame
import pygame.gfxdraw
from piece import Piece
from number import Number
from constants import *
import time


class Board:
    pygame.init()

    def __init__(self):
        self.width_shift = WIDTH - 750
        self.board_pieces_list = self.create_board_pieces_list()
        self.White_pieces_in_mid = []
        self.black_pieces_in_mid = []
        self.numbers_list = self.creat_numbers()
        self.triangle_cicle_center = self.get_triangle_cicle_center()


    @staticmethod
    def get_paddings(number):
        
        width_padding_from_left = (50 - number.width) / 2
        height_padding = (50 - number.height) / 2 

        return width_padding_from_left, height_padding

    def shift_right(self, input):
        return input + self.width_shift / 2

    def triangle_is_not_empty(self, tri_number):
        return len(self.board_pieces_list[tri_number - 1]) > 0

    def triangle_is_not_full(self, tri_number):
        return len(self.board_pieces_list[tri_number - 1]) < 5

    # first circle center for each triangle
    def get_triangle_cicle_center(self):
        triangle_cicle_center = {}
        
        for i in range(1, 7):
            triangle_cicle_center[i] = (self.shift_right(675 - 50 * (i - 1)), 575)    
        
        for i in range(7, 13):
            triangle_cicle_center[i] = (self.shift_right(325 - 50 * (i - 7)), 575)
        
        for i in range (13, 19):
            triangle_cicle_center[i] = (self.shift_right(75 + 50 * (i - 13)), 75)
        
        for i in range (19, 25):
            triangle_cicle_center[i] = (self.shift_right(425 + 50 * (i - 19)), 75)
             
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

    def creat_numbers(self):
        self.numbers_list = []

        # bottom row numbers
        for i in range(1, 7):
            number = Number(i)
            width_padding_from_left, height_padding = self.get_paddings(number)
            x_number, y_number = self.shift_right(650 + width_padding_from_left 
                                                  - 50 * (i - 1)) , 600 + height_padding
            number.set_cords(x_number, y_number)          
            self.numbers_list.append(number)
    
        
        for i in range(7, 13):
            number = Number(i)
            width_padding_from_left, height_padding = self.get_paddings(number)
            x_number, y_number = self.shift_right(300 + width_padding_from_left 
                                                  - 50 * (i - 7)), 600 + height_padding
            number.set_cords(x_number, y_number)  
            self.numbers_list.append(number)

        
        # top row numbers
        for i in range(13, 19):
            number = Number(i)
            width_padding_from_left, height_padding = self.get_paddings(number)
            x_number, y_number = self.shift_right(50 + width_padding_from_left 
                                                  + 50 * (i - 13)), height_padding
            number.set_cords(x_number, y_number)
            self.numbers_list.append(number)

        
        for i in range(19, 25):
            number = Number(i)
            width_padding_from_left, height_padding = self.get_paddings(number)
            x_number, y_number = self.shift_right(400 + width_padding_from_left 
                                                  + 50 * (i - 19)), height_padding
            number.set_cords(x_number, y_number)
            self.numbers_list.append(number)   

        return self.numbers_list

    def draw_triangle(self, surface):
        for i in range(1,7):
            if i % 2 == 0:
                color = TAN
            else:
                color = DARK_ORANGE3
            
            left_side_down_triangles = [(self.shift_right(i*50) , 600)
                                        , (self.shift_right((i+1)*50) , 600)
                                        , (self.shift_right(75 + (i-1)*50), 350)]
            
            right_side_down_triangles = [(self.shift_right((i+7)*50), 600)
                                         , (self.shift_right((i+8)*50), 600)
                                         , (self.shift_right(425 + (i-1)*50), 350)]
            
            # down triangles
            pygame.gfxdraw.aapolygon(surface, left_side_down_triangles, color)
          
            pygame.gfxdraw.aapolygon(surface, right_side_down_triangles, color)

            # filled dwn triangles
            pygame.gfxdraw.filled_polygon(surface, left_side_down_triangles, color)
          
            pygame.gfxdraw.filled_polygon(surface, right_side_down_triangles, color)
            

        for i in range(6,0,-1):

            if i % 2 == 0:
                color = DARK_ORANGE3
            else:
                color = TAN

            left_side_up_triangles = [(self.shift_right(i*50), 50)
                                      , (self.shift_right((i+1)*50), 50)
                                      , (self.shift_right(75 + (i-1)*50), 300)]
            
            right_side_up_triangles = [(self.shift_right((i+7)*50), 50)
                                        , (self.shift_right((i+8)*50), 50)
                                        , (self.shift_right(425 + (i-1)*50), 300)]
                
            # top triangles
            pygame.gfxdraw.aapolygon(surface, left_side_up_triangles, color)
          
            pygame.gfxdraw.aapolygon(surface, right_side_up_triangles, color)

            # filled top triangles
            pygame.gfxdraw.filled_polygon(surface, left_side_up_triangles, color)
          
            pygame.gfxdraw.filled_polygon(surface, right_side_up_triangles, color)

    def create_board_pieces_list(self):
        
        self.board_pieces_list = [[] for i in range(24)]
        
        # Set up white pieces
        # Line 1
        for i in range(2):
            piece = Piece(WHITE, 25, (self.shift_right(675), 575 - i * 50))
            self.board_pieces_list[0].append(piece)
        # Line 12
        for i in range(5):
            piece = Piece(WHITE, 25, (self.shift_right(75), 575 - i * 50))
            self.board_pieces_list[11].append(piece)
        # Line 17
        for i in range(3):
            piece = Piece(WHITE, 25, (self.shift_right(275), 75 + i * 50))
            self.board_pieces_list[16].append(piece)
        # line 19
        for i in range(5):
            piece = Piece(WHITE, 25, (self.shift_right(425), 75 + i * 50))
            self.board_pieces_list[18].append(piece)

        # Set up black pieces
        # line 6
        for i in range(5):
            piece = Piece(BLACK, 25, (self.shift_right(425), 575 - i * 50))
            self.board_pieces_list[5].append(piece)
        # line 8
        for i in range(3):
            piece = Piece(BLACK, 25, (self.shift_right(275), 575 - i * 50))
            self.board_pieces_list[7].append(piece)
        # line 13
        for i in range(5):
            piece = Piece(BLACK, 25, (self.shift_right(75), 75 + i * 50))
            self.board_pieces_list[12].append(piece)
        # line 24
        for i in range(2):
            piece = Piece(BLACK, 25, (self.shift_right(675), 75 + i * 50))
            self.board_pieces_list[23].append(piece)
        
        return self.board_pieces_list

    def draw(self, surface):
        self.draw_background(surface)
        self.draw_rectangles(surface)
        
        for num in self.numbers_list:
            num.draw_number(surface)
        self.draw_triangle(surface)
        
        for i in range(24):
            for piece in self.board_pieces_list[i]:
                piece.draw_piece(surface)
        
        for piece in self.White_pieces_in_mid:
            piece.draw_piece(surface)
        
        for piece in self.black_pieces_in_mid:
            piece.draw_piece(surface)

    # maybe I can rework and clean this function
    def find_tri_number(self, x_mouse, y_mouse):
        for num in self.numbers_list:
            if(num.mouse_and_number_collision_is_detected(x_mouse, y_mouse)):
                return num.value
        return None

    def __str__(self):
        pieces = []
        for piece in self.board_pieces_list:
            pieces.append(piece.__str__())
        return f"pieces_list:{pieces}"
