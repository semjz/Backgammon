from board import Board
from constants import *
import time

class Game:
    
    def __init__(self):
        self.board = Board()
        
    def select(self, x, y):
        if self.board.shift_right(350) < x <self.board.shift_right(400) and y < 50:
            return "black mid bar" 
        elif self.board.shift_right(350) < x <self.board.shift_right(400) and y > 600:
            return "white mid bar"
 
        if self.board.white_pieces_holder.collidepoint(x,y):
            return "white place holder"
        elif self.board.black_pieces_holder.collidepoint(x,y):
            return "black place holder"

        return self.board.find_tri_number(x, y)

    def place_piece_at_destination(self, piece, dest_tri_num):
        if dest_tri_num < 13:
            des_x = self.board.triangle_first_circle_centers[dest_tri_num][0]
            dest_y = self.board.triangle_first_circle_centers[dest_tri_num][1] \
                    - len(self.board.pieces[dest_tri_num - 1]) * 50
        else:
            des_x = self.board.triangle_first_circle_centers[dest_tri_num][0]
            dest_y = self.board.triangle_first_circle_centers[dest_tri_num][1] \
                    + len(self.board.pieces[dest_tri_num - 1]) * 50
        
        piece.set_center(des_x, dest_y)
        print(dest_tri_num)
        piece.set_tri_num(dest_tri_num)
        self.board.pieces[dest_tri_num - 1].append(piece)
    
    def move_from_mid_bar_to_board(self, mid_bar, dest_tri_num):
        
        if dest_tri_num is not None:
            if self.legal_move_from_mid_bar_to_board(mid_bar, dest_tri_num):
                if mid_bar == "white mid bar":
                    piece = self.board.white_pieces_in_mid.pop()
                    self.place_piece_at_destination(piece, dest_tri_num)

                if mid_bar == "black mid bar":
                    piece = self.board.black_pieces_in_mid.pop()
                    self.place_piece_at_destination(piece, dest_tri_num)
            

    def legal_move_from_mid_bar_to_board(self, mid_bar, dest_tri_num):
        if mid_bar == "white mid bar":
            current_pieces_list = self.board.white_pieces_in_mid
        
        elif mid_bar == "black mid bar":
            current_pieces_list = self.board.black_pieces_in_mid
        
        if len(current_pieces_list) > 0 and self.board.triangle_is_not_full(dest_tri_num):
            current_piece =  current_pieces_list[-1]
            dest_tri_pieces_list = self.board.pieces[dest_tri_num - 1]
            try:
                dest_tri_first_piece = dest_tri_pieces_list[0]
            # if there are no pieces on the triangle.
            except IndexError:
                return True    

            if len(dest_tri_pieces_list) == 1 and current_piece.color != dest_tri_first_piece.color:
                self.remove_piece_from_board(dest_tri_num)
                return True
            
            if current_piece.color == dest_tri_first_piece.color:
                return True
        
            else:
                for i in range(len(dest_tri_pieces_list) - 1):
                    if dest_tri_pieces_list[i].color == dest_tri_pieces_list[i + 1].color:
                        return False
                return True
        else:
            return False


    def move_on_board(self, current_tri_num, dest_tri_num):
        if current_tri_num is not None and dest_tri_num is not None:            
                    
            if self.legel_move_on_board(current_tri_num, dest_tri_num):
                dest_tri_pieces_list = self.board.pieces[dest_tri_num - 1]
                
                # if the destination triangle only has 1 piece
                if len(dest_tri_pieces_list) == 1:
                    current_tri_pieces_list = self.board.pieces[current_tri_num - 1]
                    current_piece = current_tri_pieces_list[-1]
                    dest_tri_first_piece = dest_tri_pieces_list[0]
                    
                    # if current piece has a different color than destination
                    # piece, move the destination piece to mid bar.
                    if current_piece.color != dest_tri_first_piece.color:
                        self.remove_piece_from_board(dest_tri_num)

                piece = self.board.pieces[current_tri_num - 1].pop()
                self.place_piece_at_destination(piece, dest_tri_num)
                
    
    def legel_move_on_board(self, current_tri_num, dest_tri_num):
        if dest_tri_num == "white mid bar" or  dest_tri_num == "black mid bar":
            return False

        if current_tri_num == "white place holder" or  current_tri_num == "black place holder":
            return False

        if self.board.triangle_is_not_empty(current_tri_num) and self.board.triangle_is_not_full(dest_tri_num): 
            current_tri_pieces_list = self.board.pieces[current_tri_num - 1]
            current_piece = current_tri_pieces_list[-1]
            dest_tri_pieces_list = self.board.pieces[dest_tri_num - 1]
            
            if len(dest_tri_pieces_list) in (0,1):
                return True

            elif len(dest_tri_pieces_list) > 1:
                dest_tri_first_piece = dest_tri_pieces_list[0]
                if current_piece.color == dest_tri_first_piece.color:
                    return True
                else:
                    return False
        else:
            return False


    def move_to_piece_holder(self, current_tri_num, place_holder):
        if current_tri_num is not None: 
            if self.legal_move_to_holders(current_tri_num, place_holder):
                piece = self.board.pieces[current_tri_num - 1].pop()
                print("legal move")
                
                if place_holder == "white place holder":
                    self.board.white_pieces_holder_list.append(piece)
                
                elif place_holder == "black place holder":
                    self.board.black_pieces_holder_list.append(piece)
                    print(self.board.black_pieces_holder_list)


    def legal_move_to_holders(self, current_tri_num, place_holder):
        if current_tri_num == "white place holder" or current_tri_num == "black place holder":
            return False

        if self.board.triangle_is_not_empty(current_tri_num):
            current_tri_pieces_list = self.board.pieces[current_tri_num - 1]
            current_piece = current_tri_pieces_list[-1]
            
            if current_piece.color == WHITE:
                if place_holder == "black place holder":
                    return False
                for piece in self.board.white_pieces:
                    if piece.tri_num < 19:
                        return False
                    self.board.white_pieces.pop()
                return True
            
            elif current_piece.color == BLACK:
                if place_holder == "white place holder":
                    return False
                for piece in self.board.black_pieces:
                    time.sleep(0.1)
                    print(piece.tri_num)
                    if piece.tri_num > 6:
                        return False
                    # remove the piece from black pieces because the moves is valid.
                    self.board.black_pieces.pop()
                return True
            return True
        else:
            return False

    def remove_piece_from_board(self, tri_num):
        piece = self.board.pieces[tri_num - 1].pop()
        
        if piece.color == WHITE:
            x = self.board.shift_right(375)
            y = 575 - len(self.board.white_pieces_in_mid) * 25 
            piece.set_center(x, y)
            self.board.white_pieces_in_mid.append(piece)
        
        elif piece.color == BLACK:
            x = self.board.shift_right(375)
            y = 75 + len(self.board.black_pieces_in_mid) * 25
            piece.set_center(x, y)
            self.board.black_pieces_in_mid.append(piece)


    def draw_board(self, surface):
        self.board.draw_board(surface)
