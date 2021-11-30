import pygame
from board import Board
from constants import *

class Game:
    
    def __init__(self):
        self.board = Board()
        self.turn = WHITE
        
    def select(self, x, y):
        return self.board.find_tri_number(x, y)

    def move(self, current_tri_number, dest_tri_number, turn):
               
        if current_tri_number is not None and dest_tri_number is not None:
           
            if self.board.triangle_is_not_empty(current_tri_number) and self.board.triangle_is_not_full(dest_tri_number):
                
                if self.legel_move(current_tri_number, dest_tri_number):
                    piece = self.board.board_pieces_list[current_tri_number - 1].pop()
                    
                    if piece.color != turn:
                        self.board.board_pieces_list[current_tri_number - 1].append(piece)
                        return False

                    if dest_tri_number < 13:
                        des_x = self.board.triangle_cicle_center[dest_tri_number][0]
                        dest_y = self.board.triangle_cicle_center[dest_tri_number][1] \
                                - len(self.board.board_pieces_list[dest_tri_number - 1]) * 50
                    else:
                        des_x = self.board.triangle_cicle_center[dest_tri_number][0]
                        dest_y = self.board.triangle_cicle_center[dest_tri_number][1] \
                                + len(self.board.board_pieces_list[dest_tri_number - 1]) * 50
                    
                    piece.set_center(des_x, dest_y)
                    self.board.board_pieces_list[dest_tri_number - 1].append(piece)
                    
                    return True

    
    def legel_move(self, current_tri_number, dest_tri_number):
        current_tri_pieces_list = self.board.board_pieces_list[current_tri_number - 1]
        current_piece = current_tri_pieces_list[-1]
        
        dest_tri_pieces_list = self.board.board_pieces_list[dest_tri_number - 1]
        if len(dest_tri_pieces_list) == 0 or len(dest_tri_pieces_list) == 1:
            return True
        
        dest_tri_first_piece = dest_tri_pieces_list[0]
        if current_piece.color == dest_tri_first_piece.color:
            return True
    
        else:
            for i in range(len(dest_tri_pieces_list) - 1):
                if dest_tri_pieces_list[i].color == dest_tri_pieces_list[i + 1].color:
                    return False
            return True


    def update_baord(self, surface):
        self.board.draw(surface)

    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        
        elif self.turn == BLACK:
            self.turn = WHITE