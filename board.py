import pygame
import pygame.gfxdraw
from pygame.locals import Rect
from piece import Piece
from number import Number
from constants import *


class Board:
    pygame.init()

    def __init__(self):
        self.width_shift = WIDTH - 750
        self.black_pieces = []
        self.white_pieces = []
        self.pieces = self.create_pieces_list()
        self.white_pieces_in_mid = []
        self.black_pieces_in_mid = []
        self.white_pieces_holder_list = []
        self.black_pieces_holder_list = []
        self.white_pieces_holder = Rect(0, 0, 0, 0)
        self.black_pieces_holder = Rect(0, 0, 0, 0)
        self.numbers = self.creat_numbers()
        self.triangle_first_circle_centers = self.get_triangle_first_circle_centers()
  

    @staticmethod
    def calc_num_paddings(number):
        
        width_padding = (50 - number.width) / 2
        height_padding = (50 - number.height) / 2 

        return width_padding, height_padding
    
    
    def add_num_paddings(self, number, x, y):
        width_padding, height_padding = Board.calc_num_paddings(number)
        new_x = self.shift_right(x + width_padding)
        new_y = y + height_padding
        return new_x, new_y


    def shift_right(self, width):
        return width + self.width_shift / 2

    def triangle_is_not_empty(self, tri_num):
        return len(self.pieces[tri_num - 1]) > 0

    def triangle_is_not_full(self, tri_num):
        return len(self.pieces[tri_num - 1]) < 5

    # first circle center for each triangle
    def get_triangle_first_circle_centers(self):
        triangle_first_circle_centers = {}
        
        for i in range(1, 7):
            triangle_first_circle_centers[i] = (self.shift_right(675 - 50 * (i - 1)), 575)    
        
        for i in range(7, 13):
            triangle_first_circle_centers[i] = (self.shift_right(325 - 50 * (i - 7)), 575)
        
        for i in range (13, 19):
            triangle_first_circle_centers[i] = (self.shift_right(75 + 50 * (i - 13)), 75)
        
        for i in range (19, 25):
            triangle_first_circle_centers[i] = (self.shift_right(425 + 50 * (i - 19)), 75)
             
        return triangle_first_circle_centers     
           
    def draw_background(self, surface):
        surface.fill(BACKGROUND_COLOR)

    def draw_rectangles(self, surface):
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

        # pieces holders
        self.white_pieces_holder = Rect(self.shift_right(750), 50, 50, 180)
        self.black_pieces_holder = Rect(self.shift_right(750), 420, 50, 180)
        
        # draw pieces holders
        pygame.draw.rect(surface, BROWN, self.white_pieces_holder)
        pygame.draw.rect(surface, BROWN, self.black_pieces_holder)


    def creat_numbers(self):
        self.numbers = []

        # bottom numbers
        for i in range(1, 7):
            number = Number(i)
            x_number, y_number = self.add_num_paddings(number, 650 - 50 * (i - 1) , 600) 
            number.set_cords(x_number, y_number)          
            self.numbers.append(number)
    
        
        for i in range(7, 13):
            number = Number(i)
            x_number, y_number = self.add_num_paddings(number, 300 - 50 * (i - 7), 600)
            number.set_cords(x_number, y_number)  
            self.numbers.append(number)

        
        # top numbers
        for i in range(13, 19):
            number = Number(i)
            x_number, y_number = self.add_num_paddings(number, 50 + 50 * (i - 13), 0)
            number.set_cords(x_number, y_number)
            self.numbers.append(number)

        
        for i in range(19, 25):
            number = Number(i)
            x_number, y_number = self.add_num_paddings(number, 400 + 50 * (i - 19), 0)
            number.set_cords(x_number, y_number)
            self.numbers.append(number)   

        return self.numbers

    def draw_triangle(self, surface):
        # down triangles
        for i in range(1,7):
            if i % 2 == 0:
                color = TAN
            else:
                color = DARK_ORANGE3
            
            # left side triangle to be drawn
            left_side_down_triangle = [(self.shift_right(i*50) , 600)
                                        , (self.shift_right((i+1)*50) , 600)
                                        , (self.shift_right(75 + (i-1)*50), 350)]
            
            # right side triangle to be drawn
            right_side_down_triangle = [(self.shift_right((i+7)*50), 600)
                                         , (self.shift_right((i+8)*50), 600)
                                         , (self.shift_right(425 + (i-1)*50), 350)]
            
            # draw an anti aliasing polygan
            pygame.gfxdraw.aapolygon(surface, left_side_down_triangle, color)
          
            pygame.gfxdraw.aapolygon(surface, right_side_down_triangle, color)

            # draw a filled polygan
            pygame.gfxdraw.filled_polygon(surface, left_side_down_triangle, color)
          
            pygame.gfxdraw.filled_polygon(surface, right_side_down_triangle, color)
            
        # top triangles
        for i in range(6,0,-1):

            if i % 2 == 0:
                color = DARK_ORANGE3
            else:
                color = TAN

            # left side triangle to be drawn
            left_side_up_triangle = [(self.shift_right(i*50), 50)
                                      , (self.shift_right((i+1)*50), 50)
                                      , (self.shift_right(75 + (i-1)*50), 300)]
            
            # right side triangle to be drawn
            right_side_up_triangle = [(self.shift_right((i+7)*50), 50)
                                        , (self.shift_right((i+8)*50), 50)
                                        , (self.shift_right(425 + (i-1)*50), 300)]
                
            # draw an anti aliasing polygan
            pygame.gfxdraw.aapolygon(surface, left_side_up_triangle, color)
          
            pygame.gfxdraw.aapolygon(surface, right_side_up_triangle, color)

            # draw a filled polygan
            pygame.gfxdraw.filled_polygon(surface, left_side_up_triangle, color)
          
            pygame.gfxdraw.filled_polygon(surface, right_side_up_triangle, color)

    def create_pieces_list(self):
        
        pieces = [[] for i in range(24)]
        
        # Set up white pieces
        # Line 1
        for i in range(2):
            piece = Piece(WHITE, 25, (self.shift_right(675), 575 - i * 50), 1)
            self.white_pieces.append(piece)
            pieces[0].append(piece)
        # Line 12
        for i in range(5):
            piece = Piece(WHITE, 25, (self.shift_right(75), 575 - i * 50), 12)
            self.white_pieces.append(piece)
            pieces[11].append(piece)
        # Line 17
        for i in range(3):
            piece = Piece(WHITE, 25, (self.shift_right(275), 75 + i * 50), 18)
            self.white_pieces.append(piece)
            pieces[16].append(piece)
        # line 19
        for i in range(5):
            piece = Piece(WHITE, 25, (self.shift_right(425), 75 + i * 50), 20)
            self.white_pieces.append(piece)
            pieces[18].append(piece)

        # Set up black pieces
        # line 6
        for i in range(5):
            piece = Piece(BLACK, 25, (self.shift_right(425), 575 - i * 50), 6)
            self.black_pieces.append(piece)
            pieces[5].append(piece)
        # line 8
        for i in range(3):
            piece = Piece(BLACK, 25, (self.shift_right(275), 575 - i * 50), 8)
            self.black_pieces.append(piece)
            pieces[7].append(piece)
        # line 13
        for i in range(5):
            piece = Piece(BLACK, 25, (self.shift_right(75), 75 + i * 50), 13)
            self.black_pieces.append(piece)
            pieces[12].append(piece)
        # line 24
        for i in range(2):
            piece = Piece(BLACK, 25, (self.shift_right(675), 75 + i * 50), 25)
            self.black_pieces.append(piece)
            pieces[23].append(piece)
        
        return pieces

    def draw_board(self, surface):
        
        self.draw_background(surface)
        self.draw_rectangles(surface)
        
        for num in self.numbers:
            num.draw_number(surface)
        
        self.draw_triangle(surface)
        
        for i in range(24):
            for piece in self.pieces[i]:
                piece.draw_piece(surface)
        
        for piece in self.white_pieces_in_mid:
            piece.draw_piece(surface)
        
        for piece in self.black_pieces_in_mid:
            piece.draw_piece(surface)

        for i in range(len(self.white_pieces_holder_list)):
            pygame.draw.rect(surface, WHITE, (self.shift_right(750), 50 + i * 12, 50, 10))

        for i in range(len(self.black_pieces_holder_list)):
            pygame.draw.rect(surface, BLACK, (self.shift_right(750), 590 - i * 12, 50, 10))
            

    # find the triangle number that mouse cursor is on.
    def find_tri_number(self, x_mouse, y_mouse):
        for num in self.numbers:
            if(num.mouse_and_number_collision(x_mouse, y_mouse)):
                return num.value
        return None
