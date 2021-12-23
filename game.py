import pygame
from board import Board
from constants import *

class Game:
    
    def __init__(self):
        self.board = Board()
        self.current_area = None
        self.dest_area = None
        

    # locate the area of board. 
    def locate(self, x, y):
        if self.board.shift_right(350) < x <self.board.shift_right(400) and y < 50:
            self.board.area_selected = True
            return BLACK_MID_BAR
        elif self.board.shift_right(350) < x <self.board.shift_right(400) and y > 600:
            self.board.area_selected  = True
            return WHITE_MID_BAR

        if self.board.white_pieces_holder.collidepoint(x, y):
            if self.board.area_selected:
                return WHITE_PLACE_HOLDER
            else:
                return None
        elif self.board.black_pieces_holder.collidepoint(x, y):
            if self.board.area_selected:
                return BLACK_PLACE_HOLDER
            else:
                return None
        return self.board.find_tri_number(x, y)

    def place_piece_at_destination(self, piece, dest_tri_num):
        if dest_tri_num < 13:
            dest_x = self.board.triangle_first_circle_centers[dest_tri_num][0]
            dest_y = self.board.triangle_first_circle_centers[dest_tri_num][1] \
                    - len(self.board.pieces[dest_tri_num - 1]) * 50
        else:
            dest_x = self.board.triangle_first_circle_centers[dest_tri_num][0]
            dest_y = self.board.triangle_first_circle_centers[dest_tri_num][1] \
                    + len(self.board.pieces[dest_tri_num - 1]) * 50
        
        piece.set_center(dest_x, dest_y)
        piece.set_tri_num(dest_tri_num)
        self.board.pieces[dest_tri_num - 1].append(piece)
    
    # the method can be reduced by creating a method.
    def move_from_mid_bar_to_board(self, mid_bar, dest_tri_num):
        if dest_tri_num is not None:
            if self.legal_move_from_mid_bar_to_board(mid_bar, dest_tri_num):
                dest_tri_pieces_list = self.board.pieces[dest_tri_num - 1]
         
                if mid_bar == WHITE_MID_BAR:
                    # if the destination triangle only has 1 piece
                    if len(dest_tri_pieces_list) == 1:
                        current_tri_pieces_list = self.board.white_pieces_in_mid
                        current_piece = current_tri_pieces_list[-1]
                        dest_tri_first_piece = dest_tri_pieces_list[0]

                        # if current piece has a different color than destination
                        # piece, move the destination piece to mid bar.
                        if current_piece.color != dest_tri_first_piece.color:
                            self.remove_piece_from_board_to_mid_bar(dest_tri_num)
                    
                    piece = self.board.white_pieces_in_mid.pop()
                    self.place_piece_at_destination(piece, dest_tri_num)

                if mid_bar == BLACK_MID_BAR:
                    # if the destination triangle only has 1 piece
                    if len(dest_tri_pieces_list) == 1:
                        current_tri_pieces_list = self.board.black_pieces_in_mid
                        current_piece = current_tri_pieces_list[-1]
                        dest_tri_first_piece = dest_tri_pieces_list[0]

                        # if current piece has a different color than destination
                        # piece, move the destination piece to mid bar.
                        if current_piece.color != dest_tri_first_piece.color:
                            self.remove_piece_from_board_to_mid_bar(dest_tri_num)
                    
                    piece = self.board.black_pieces_in_mid.pop()
                    self.place_piece_at_destination(piece, dest_tri_num)
            

    def legal_move_from_mid_bar_to_board(self, mid_bar, dest_tri_num):
        
        if dest_tri_num == WHITE_PLACE_HOLDER or dest_tri_num == BLACK_PLACE_HOLDER:
            return False

        if mid_bar == WHITE_MID_BAR:
            current_pieces_list = self.board.white_pieces_in_mid
        
        if mid_bar == BLACK_MID_BAR:
            current_pieces_list = self.board.black_pieces_in_mid
        
        if len(current_pieces_list) > 0 and self.board.triangle_is_not_full(dest_tri_num):
            current_piece =  current_pieces_list[-1]
            dest_tri_pieces_list = self.board.pieces[dest_tri_num - 1]

            if len(dest_tri_pieces_list) in (0,1):
                return True
            
            # more than one pieces at destination
            elif len(dest_tri_pieces_list) > 1:
                dest_tri_first_piece = dest_tri_pieces_list[0]
                
                # if current piece and destination piece color are same.
                if current_piece.color == dest_tri_first_piece.color:
                    return True
                else:
                    return False
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
                        self.remove_piece_from_board_to_mid_bar(dest_tri_num)

                piece = self.board.pieces[current_tri_num - 1].pop()
                self.place_piece_at_destination(piece, dest_tri_num)
                
    
    def legel_move_on_board(self, current_tri_num, dest_tri_num):
        if current_tri_num == dest_tri_num:
            return False

        if dest_tri_num == WHITE_MID_BAR or  dest_tri_num == BLACK_MID_BAR:
            return False

        if current_tri_num == WHITE_PLACE_HOLDER or  current_tri_num == BLACK_PLACE_HOLDER:
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
                
                if place_holder == WHITE_PLACE_HOLDER:
                    self.board.white_pieces.pop()
                    self.board.white_pieces_holder_list.append(piece)
                
                elif place_holder == BLACK_PLACE_HOLDER:
                    self.board.black_pieces.pop()
                    self.board.black_pieces_holder_list.append(piece)


    def legal_move_to_holders(self, current_tri_num, place_holder):
        if current_tri_num == WHITE_PLACE_HOLDER or current_tri_num == BLACK_PLACE_HOLDER:
            return False

        if self.board.triangle_is_not_empty(current_tri_num):
            current_tri_pieces_list = self.board.pieces[current_tri_num - 1]
            current_piece = current_tri_pieces_list[-1]
            
            if current_piece.color == WHITE:
                if place_holder == BLACK_PLACE_HOLDER:
                    return False
                for piece in self.board.white_pieces:
                    # if a piece is not at home base.
                    if piece.tri_num < 19:
                        return False
                return True
            
            elif current_piece.color == BLACK:
                if place_holder == WHITE_PLACE_HOLDER:
                    return False
                for piece in self.board.black_pieces:
                    # if a piece is not at home base.
                    if piece.tri_num > 6:
                        return False
                return True
        else:
            return False

    def move(self):
        if self.current_area == WHITE_MID_BAR or self.current_area == BLACK_MID_BAR:
            self.move_from_mid_bar_to_board(self.current_area, self.dest_area)
            
        elif self.dest_area == WHITE_PLACE_HOLDER or self.dest_area == BLACK_PLACE_HOLDER:
            self.move_to_piece_holder(self.current_area, self.dest_area)
        
        else:
            self.move_on_board(self.current_area, self.dest_area)
        self.board.area_selected = False

    def remove_piece_from_board_to_mid_bar(self, tri_num):
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

    def check_current_area_has_piece(self):
        if self.current_area == WHITE_MID_BAR:
            if not self.board.white_pieces_in_mid:
                self.board.area_selected = False
        
        elif self.current_area == BLACK_MID_BAR:
            if not self.board.black_pieces_in_mid:
                self.board.area_selected = False
        
        elif self.current_area != None:
            if not self.board.triangle_is_not_empty(self.current_area):
                self.board.area_selected = False

    def update(self, surface):
        self.board.draw_board(surface)
        pygame.display.update()
