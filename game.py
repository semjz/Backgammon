import pygame
from board import Board
from constants import *

class Game:
    
    def __init__(self):
        self.board = Board()
        self.turn = WHITE
        
    def select(self, x, y):
        if self.board.shift_right(350) < x <self.board.shift_right(400) and y < 50:
            return 25
        elif self.board.shift_right(350) < x <self.board.shift_right(400) and y > 600:
            return 26
 
        if self.board.white_pieces_holder.collidepoint(x,y):
            return 27
        elif self.board.black_pieces_holder.collidepoint(x,y):
            return 28

        return self.board.find_tri_number(x, y)

    def move(self, current_tri_number, dest_tri_number, turn):
               
        if current_tri_number is not None and dest_tri_number is not None:
           
            if self.board.triangle_is_not_empty(current_tri_number) and self.board.triangle_is_not_full(dest_tri_number):
                
                if self.legel_move(current_tri_number, dest_tri_number, turn):
                    piece = self.board.board_pieces_list[current_tri_number - 1].pop()

                    if dest_tri_number < 13:
                        des_x = self.board.triangle_cicle_center[dest_tri_number][0]
                        dest_y = self.board.triangle_cicle_center[dest_tri_number][1] \
                                - len(self.board.board_pieces_list[dest_tri_number - 1]) * 50
                    else:
                        des_x = self.board.triangle_cicle_center[dest_tri_number][0]
                        dest_y = self.board.triangle_cicle_center[dest_tri_number][1] \
                                + len(self.board.board_pieces_list[dest_tri_number - 1]) * 50
                    
                    piece.set_center(des_x, dest_y)
                    piece.set_tri_number(dest_tri_number)
                    self.board.board_pieces_list[dest_tri_number - 1].append(piece)
                    
                    return True
    
    def legel_move(self, current_tri_number, dest_tri_number, turn):
        if dest_tri_number == 25:
            return False
        
        elif dest_tri_number == 26:
            return False
        
        if current_tri_number == 25:
            current_tri_pieces_list = self.board.white_pieces_in_mid

        elif current_tri_number == 26:
            current_tri_pieces_list = self.board.black_pieces_in_mid

        else:
            current_tri_pieces_list = self.board.board_pieces_list[current_tri_number - 1]
        
        current_piece = current_tri_pieces_list[-1]
        
        dest_tri_pieces_list = self.board.board_pieces_list[dest_tri_number - 1]
        try:
            dest_tri_first_piece = dest_tri_pieces_list[0]
        # if there are no pieces on the triangle.
        except IndexError:
            return True
        
        # # if it's not the piece's turn
        # if current_piece.color != turn:
        #     return False        

        if len(dest_tri_pieces_list) == 1:
            if current_piece.color != dest_tri_first_piece.color:
                self.remove_piece_from_board(dest_tri_number)
            return True
        
        if current_piece.color == dest_tri_first_piece.color:
            return True
    
        else:
            for i in range(len(dest_tri_pieces_list) - 1):
                if dest_tri_pieces_list[i].color == dest_tri_pieces_list[i + 1].color:
                    return False
            return True

    def move_to_piece_holder(self, current_tri_number, dest_tri_number):
        if current_tri_number is not None and dest_tri_number is not None: 
            if self.board.triangle_is_not_empty(current_tri_number) \
                and self.legal_move_to_holders(current_tri_number, dest_tri_number):
                
                piece = self.board.board_pieces_list[current_tri_number - 1].pop()
                if piece.color == WHITE:
                    self.board.white_pieces_holder_list.append(piece)
                elif piece.color == BLACK:
                    self.board.black_pieces_holder_list.append(piece)

    
    def legal_move_to_holders(self, current_tri_number, dest_tri_number):
        current_tri_pieces_list = self.board.board_pieces_list[current_tri_number - 1]
        current_piece = current_tri_pieces_list[-1]
        
        if current_piece.color == WHITE:
            if dest_tri_number == 28:
                return False
            for piece in self.board.white_pieces_list:
                if piece.tri_number < 19:
                    return False
            return True
        
        elif current_piece.color == BLACK:
            if dest_tri_number == 27:
                return False
            for piece in self.board.black_pieces_list:
                if piece.tri_number > 6:
                    return False
            return True




    def remove_piece_from_board(self, triangle_number):
        piece = self.board.board_pieces_list[triangle_number - 1].pop()
        
        if piece.color == WHITE:
            x = self.board.shift_right(375)
            y = 75 + len(self.board.white_pieces_in_mid) * 25
            piece.set_center(x, y)
            self.board.white_pieces_in_mid.append(piece)
        
        elif piece.color == BLACK:
            x = self.board.shift_right(375)
            y = 575 - len(self.board.black_pieces_in_mid) * 25
            piece.set_center(x, y)
            self.board.black_pieces_in_mid.append(piece)


    def draw_baord(self, surface):
        self.board.draw(surface)

    def change_turn(self):
        if self.turn == WHITE:
            self.turn = BLACK
        
        elif self.turn == BLACK:
            self.turn = WHITE