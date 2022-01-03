import pygame
from board import Board
from dice import Dice
from constants import *

class Game:
    
    def __init__(self):
        self.board = Board()
        self.current_area = None
        self.dest_area = None
        self.area_selected = False
        self.dices = self.create_dices()
        self.dice_rolled = False
        self.double_dice_rolled = False
        self.valid_moves_on_board = []
        self.total_no_of_moves = 0
        self.total_move_distance_allowed_on_board = None
        self.move_distance_left_on_board = None
        
    def set_valid_moves(self):
        if self.double_dice_rolled:
            self.valid_moves_on_board = [i*self.dices[0].dice_num for i in range(1, 5)]
        else:
            self.valid_moves_on_board = [self.dices[0].dice_num, self.dices[1].dice_num, 
                                        self.dices[0].dice_num + self.dices[1].dice_num]

    def set_total_move_distance(self):
        if self.double_dice_rolled:
            self.total_move_distance_allowed_on_board = self.dices[0].dice_num * 4
        else:
            self.total_move_distance_allowed_on_board = self.dices[0].dice_num + self.dices[1].dice_num
        self.move_distance_left_on_board = self.total_move_distance_allowed_on_board
        # print(f"total move distance allowed: {self.total_move_distance_allowed_on_board}")

    def set_total_no_of_moves(self):
        if self.double_dice_rolled:
            self.total_no_of_moves = 4
        else:
            self.total_no_of_moves = 2
        # print(f"total no of moves: {self.total_no_of_moves}")

    # Locate which area of the board is selected
    def locate(self, x, y):
        # if the square for black pieces on mid bar is selected.
        if self.board.shift_right(350) < x <self.board.shift_right(400) and y < 50:
            # highlight the piece if there is a piece on mid bar.
            if self.board.black_pieces_in_mid:
                piece = self.board.black_pieces_in_mid[-1]
                if self.dice_rolled:
                    piece.highlight()
            return BLACK_MID_BAR
        # if the square for white pieces on mid bar is selected.
        elif self.board.shift_right(350) < x <self.board.shift_right(400) and y > 600:
            # highlight the piece if there is a piece on mid bar.
            if self.board.white_pieces_in_mid:
                piece = self.board.white_pieces_in_mid[-1]
                if self.dice_rolled:
                    piece.highlight()
            return WHITE_MID_BAR
        # if white piece holder is clicked on by mouse.
        if self.board.white_pieces_holder.collidepoint(x, y):
            """if an origin on board is already selected return string related 
               to this area, otherwise return None as this is not a valid area 
               as the origin it is only valid as a destination"""
            if self.area_selected:
                return WHITE_PLACE_HOLDER
            else:
                return None
        # if mouse is on black pieces holder
        elif self.board.black_pieces_holder.collidepoint(x, y):
            if self.area_selected:
                return BLACK_PLACE_HOLDER
            else:
                return None

        return self.find_tri_number(x, y)

    def place_piece_at_destination(self, piece, dest_tri_num):
        # if there are more than 5 pieces on a triangle squeeze the pieces.
        if len(self.board.pieces[dest_tri_num - 1] ) >= 5:
            self.retract_pieces_on_tri(piece, dest_tri_num)
        
        else:
            if dest_tri_num < 13:
                dest_x = self.board.triangle_first_piece_centers[dest_tri_num][0]
                # find the correct y position depending on number of pieces on
                # the triangle
                dest_y = self.board.triangle_first_piece_centers[dest_tri_num][1] \
                            - len(self.board.pieces[dest_tri_num - 1]) * 50
            else:
                dest_x = self.board.triangle_first_piece_centers[dest_tri_num][0]
                # find the correct y position depending on number of pieces on
                # the triangle
                dest_y = self.board.triangle_first_piece_centers[dest_tri_num][1] \
                            + len(self.board.pieces[dest_tri_num - 1] ) * 50
            
            piece.set_center(dest_x, dest_y)
        # set pieces new triangle number and move the piece to the right place
        # in the pieces list.
        piece.set_tri_num(dest_tri_num)
        self.board.pieces[dest_tri_num - 1].append(piece)

    def retract_pieces_on_tri(self, last_piece, dest_tri_num):
        # add one becuase a new piece is to be added to destination triangle
        #  after calling this method.
        no_of_pieces = len(self.board.pieces[dest_tri_num - 1]) + 1
        distance_between_pieces = 250 / no_of_pieces
        x = self.board.triangle_first_piece_centers[dest_tri_num][0]
        y = self.board.triangle_first_piece_centers[dest_tri_num][1]

        for piece in self.board.pieces[dest_tri_num - 1]:
            # set pieces center before updating y.
            piece.set_center(x, y)
            if dest_tri_num < 13:
                y -= distance_between_pieces
            else:
                y += distance_between_pieces
        # set the center of the piece that is to be added.
        last_piece.set_center(x, y)

    def expand_pieces_on_tri(self, dest_tri_num):
        no_of_pieces = len(self.board.pieces[dest_tri_num - 1]) 
        distance_between_pieces = 250 / no_of_pieces
        x = self.board.triangle_first_piece_centers[dest_tri_num][0]
        y = self.board.triangle_first_piece_centers[dest_tri_num][1]

        for piece in self.board.pieces[dest_tri_num - 1]:
            piece.set_center(x, y)
            if dest_tri_num < 13:
                y -= distance_between_pieces
            else:
                y += distance_between_pieces

    
    # the method can be reduced by creating a method.
    def move_from_mid_bar_to_board(self, mid_bar, dest_tri_num):
        dest_tri_pieces_list = self.board.pieces[dest_tri_num - 1]
    
        if mid_bar == WHITE_MID_BAR:
            current_tri_pieces_list = self.board.white_pieces_in_mid
            current_piece = current_tri_pieces_list.pop()
            current_piece.dehighlight()
            # if the destination triangle only has 1 piece
            if len(dest_tri_pieces_list) == 1:
                dest_tri_first_piece = dest_tri_pieces_list[0]

                # if current piece has a different color than destination
                # piece, move the destination piece to mid bar.
                if current_piece.color != dest_tri_first_piece.color:
                    # this method only moves the destination piece to mid bar.
                    self.move_piece_from_board_to_mid_bar(dest_tri_num)
            # following above this method moves piece on mid bar to destination.
            self.place_piece_at_destination(current_piece, dest_tri_num)

        if mid_bar == BLACK_MID_BAR:
            current_tri_pieces_list = self.board.black_pieces_in_mid
            current_piece = current_tri_pieces_list.pop()
            current_piece.dehighlight()
            # if the destination triangle only has 1 piece
            if len(dest_tri_pieces_list) == 1:
                dest_tri_first_piece = dest_tri_pieces_list[0]

                # if current piece has a different color than destination
                # piece, move the destination piece to mid bar.
                if current_piece.color != dest_tri_first_piece.color:
                    # this method only moves the destination piece to mid bar.
                    self.move_piece_from_board_to_mid_bar(dest_tri_num)
            # following above this method moves piece on mid bar to destination.
            self.place_piece_at_destination(current_piece, dest_tri_num)
            

    def legal_move_from_mid_bar_to_board(self, mid_bar, dest_tri_num):
        if dest_tri_num is not None:
            if dest_tri_num in (WHITE_PLACE_HOLDER, BLACK_PLACE_HOLDER):
                return False
            
            if dest_tri_num in (WHITE_MID_BAR, BLACK_MID_BAR):
                return False

            if mid_bar == WHITE_MID_BAR:
                current_pieces_list = self.board.white_pieces_in_mid
            
            if mid_bar == BLACK_MID_BAR:
                current_pieces_list = self.board.black_pieces_in_mid
            
            if len(current_pieces_list) > 0:
                current_piece =  current_pieces_list[-1]
                dest_tri_pieces_list = self.board.pieces[dest_tri_num - 1]
                
                # if there are 1 or 2 pieces on destination, move is 
                # definitely valid.
                if len(dest_tri_pieces_list) in (0,1):
                    return True
                
                # if there are more than 1 pieces on destination, colors of
                # current and destination pieces needs to be compared.
                # if the color are different the move is illegall becuase
                # a piece can't be place on a triangle with 1 or more pieces 
                # of diffrent color.
                elif len(dest_tri_pieces_list) > 1:
                    dest_tri_first_piece = dest_tri_pieces_list[0]
                    
                    if current_piece.color == dest_tri_first_piece.color:
                        return True
                    else:
                        return False
            else:
                return False


    def move_on_board(self, current_tri_num, dest_tri_num, highlight = False):
        current_tri_pieces_list = self.board.pieces[current_tri_num - 1]
        current_piece = current_tri_pieces_list.pop()
        dest_tri_pieces_list = self.board.pieces[dest_tri_num - 1]

        current_piece.dehighlight()
        
        if highlight:
            current_piece.highlight()

        # if the destination triangle only has 1 piece
        if len(dest_tri_pieces_list) == 1:
            dest_tri_first_piece = dest_tri_pieces_list[0]
            
            # if current piece has a different color than destination
            # piece, move the destination piece to mid bar.
            if current_piece.color != dest_tri_first_piece.color:
                print("remove")
                self.move_piece_from_board_to_mid_bar(dest_tri_num)
        # if there are more than 5 pieces at current triangle expand
        # pieces on triangle after removing a piece.
        if len(self.board.pieces[current_tri_num - 1]) >= 5:
            self.expand_pieces_on_tri(current_tri_num)
        self.place_piece_at_destination(current_piece, dest_tri_num)
        
        self.total_no_of_moves -= 1
                
    
    def legel_move_on_board(self, current_tri_num, dest_tri_num):
        if current_tri_num is None and dest_tri_num is None:
            return False

        current_tri_pieces_list = self.board.pieces[current_tri_num - 1]
        current_piece = current_tri_pieces_list[-1]
        
        # when moving on bard destination can'be mid bar.
        if dest_tri_num in (BLACK_MID_BAR, WHITE_MID_BAR):
            return False
        # if piece is moving in the right direction in the board.
        if Game.correct_move_direction(current_piece, current_tri_num, dest_tri_num):
            dest_tri_pieces_list = self.board.pieces[dest_tri_num - 1]
            
            # if there are 1 or 2 pieces on destination, move is 
            # definitely valid.
            if len(dest_tri_pieces_list) in (0,1):
                return True
            # if there are more than 1 pieces on destination, colors of
            # current and destination pieces needs to be compared.
            # if the color are different the move is illegall becuase
            # a piece can't be place on a triangle with 1 or more pieces 
            # of diffrent color.
            elif len(dest_tri_pieces_list) > 1:
                dest_tri_first_piece = dest_tri_pieces_list[0]
                if current_piece.color == dest_tri_first_piece.color:
                    return True
                else:
                    return False
        else:
            False



    """ This method returns True if white piece is moving clock-wise
        and if black piece is moving anti-clock-wise """
    @staticmethod
    def correct_move_direction(piece, current_tri_num, dest_tri_num):
        if piece.color == WHITE:
            return dest_tri_num - current_tri_num > 0
        if piece.color == BLACK:
            return dest_tri_num - current_tri_num < 0
            

    def move_to_piece_holder(self, current_tri_num, place_holder):
        current_tri_pieces_list = self.board.pieces[current_tri_num - 1]
        current_piece = current_tri_pieces_list.pop()
        current_piece.dehighlight()
        
        # if there are more than 5 pieces on a triangle, expand the pieces
        # when removing a piece.
        if len(self.board.pieces[current_tri_num - 1]) >= 5:
            self.expand_pieces_on_tri(current_tri_num)
        
        if place_holder == WHITE_PLACE_HOLDER:
            self.board.white_pieces.pop()
            self.board.white_pieces_holder_list.append(current_piece)
        
        elif place_holder == BLACK_PLACE_HOLDER:
            self.board.black_pieces.pop()
            self.board.black_pieces_holder_list.append(current_piece)


    def legal_move_to_holders(self, current_tri_num, place_holder):
        if current_tri_num is not None:
            if current_tri_num in (WHITE_PLACE_HOLDER, BLACK_PLACE_HOLDER):
                return False

            if self.board.triangle_is_not_empty(current_tri_num):
                current_tri_pieces_list = self.board.pieces[current_tri_num - 1]
                current_piece = current_tri_pieces_list[-1]
                
                if current_piece.color == WHITE:
                    if place_holder == BLACK_PLACE_HOLDER:
                        return False
                    for piece in self.board.white_pieces:
                        # if a piece is outside home base move is illegal.
                        # home base is from 19 to 24
                        if piece.tri_num < 19:
                            return False
                    return True
                
                elif current_piece.color == BLACK:
                    if place_holder == WHITE_PLACE_HOLDER:
                        return False
                    for piece in self.board.black_pieces:
                        # if a piece is outside home base move is illegal.
                        # home base is from 1 to 6
                        if piece.tri_num > 6:
                            return False
                    return True
            else:
                return False

    def move_piece_from_board_to_mid_bar(self, tri_num):
        piece = self.board.pieces[tri_num - 1].pop()
        
        if piece.color == WHITE:
            # x,y corresponding to mid bar
            x = self.board.shift_right(375)
            y = 575 - len(self.board.white_pieces_in_mid) * 25 
            piece.set_center(x, y)
            self.board.white_pieces_in_mid.append(piece)

        
        elif piece.color == BLACK:
            # x,y corresponding to mid bar
            x = self.board.shift_right(375)
            y = 75 + len(self.board.black_pieces_in_mid) * 25
            piece.set_center(x, y)
            self.board.black_pieces_in_mid.append(piece)

    # check if the selected origin has piece, if the selected area 
    # doesn't have a piece self.area_selected must be False.
    def check_current_area_has_piece(self):
        if self.current_area == WHITE_MID_BAR:
            if not self.board.white_pieces_in_mid:
                self.area_selected = False
        
        elif self.current_area == BLACK_MID_BAR:
            if not self.board.black_pieces_in_mid:
                self.area_selected = False
        
        elif self.current_area is not None:
            if not self.board.triangle_is_not_empty(self.current_area):
                self.area_selected = False

    # main move method that calls appropriate movement methods depending on
    # area selected on the board.
    def move(self):
        # after movement is done self.area_selected nust be False.
        if self.current_area == WHITE_MID_BAR or self.current_area == BLACK_MID_BAR:
            if self.legal_move_from_mid_bar_to_board(self.current_area, self.dest_area):
                self.move_from_mid_bar_to_board(self.current_area, self.dest_area)
                self.area_selected = False
            
        elif self.dest_area == WHITE_PLACE_HOLDER or self.dest_area == BLACK_PLACE_HOLDER:
            if self.legal_move_to_holders(self.current_area, self.dest_area):
                self.move_to_piece_holder(self.current_area, self.dest_area)
                self.area_selected = False
        
        else:
            if self.double_dice_rolled:
                self.moves_on_board_double_dice()
            else:
                move_distance = abs(self.dest_area - self.current_area)
                if move_distance == self.total_move_distance_allowed_on_board:
                    if not self.moves_on_board_single_dice([self.dices[0].dice_num, self.dices[1].dice_num]):
                        self.moves_on_board_single_dice([self.dices[1].dice_num, self.dices[0].dice_num])
                else:
                    if self.legel_move_on_board(self.current_area, self.dest_area):
                        if self.is_valid_move_on_board(self.current_area, self.dest_area):
                            self.move_on_board(self.current_area, self.dest_area)
                            self.area_selected = False


        
    def moves_on_board_double_dice(self):
        if self.is_valid_move_on_board(self.current_area, self.dest_area):
            current_piece = self.board.pieces[self.current_area - 1][-1]
            move_distance = abs(self.dest_area - self.current_area)
            total_no_of_moves = self.total_no_of_moves
            no_of_moves_made = int(move_distance / self.dices[0].dice_num)
            current_area = self.current_area

            for i in range(no_of_moves_made):
                if current_piece.color == WHITE:
                    dest_area = current_area + self.dices[0].dice_num
                else:
                    dest_area = current_area - self.dices[0].dice_num
                
                if self.legel_move_on_board(current_area, dest_area):
                    if self.is_valid_move_on_board(current_area, dest_area):
                        self.move_on_board(current_area, dest_area)
                        self.total_no_of_moves -= 1
                    else:
                        if self.total_no_of_moves != total_no_of_moves:
                            self.move_on_board(current_area, self.current_area, True)
                            self.total_no_of_moves = total_no_of_moves
                        return
                else:
                    if self.total_no_of_moves != total_no_of_moves:
                        self.move_on_board(current_area, self.current_area, True)
                        self.total_no_of_moves = total_no_of_moves
                    return
                
                if current_piece.color == WHITE:
                    current_area += self.dices[0].dice_num
                else:
                    current_area -= self.dices[0].dice_num
            
            self.area_selected = False
            
            

    def moves_on_board_single_dice(self, moves_in_between):
        current_piece = self.board.pieces[self.current_area - 1][-1]
        total_no_of_moves = self.total_no_of_moves
        current_area = self.current_area        
        for move in moves_in_between:
            if current_piece.color == WHITE: 
                dest_area = current_area + move
            else:
                dest_area = current_area - move
            print(f"current_area: {current_area}")
            print(f"dest_area: {dest_area}")
            print(f"legal: {self.legel_move_on_board(current_area, dest_area)}")
            if self.legel_move_on_board(current_area, dest_area):
                if self.is_valid_move_on_board(current_area, dest_area):
                    self.move_on_board(current_area, dest_area)
                    self.total_no_of_moves -= 1
                else:
                    if self.total_no_of_moves != total_no_of_moves:
                        self.move_on_board(current_area, self.current_area, True)
                        self.total_no_of_moves = total_no_of_moves
                    return False
            else:
                if self.total_no_of_moves != total_no_of_moves:
                    self.move_on_board(current_area, self.current_area, True)
                    self.total_no_of_moves = total_no_of_moves
                return False

            current_area = dest_area

        self.area_selected = False
        return True


    def is_valid_move_on_board(self, current_area, dest_area):
        move_ditsnace = abs(dest_area - current_area)
        if move_ditsnace in self.valid_moves_on_board:
            self.valid_moves_on_board
            return True
        else:
            return False

    
    # Find the triangle number that mouse cursor clicked on.
    def find_tri_number(self, x_mouse, y_mouse):
        for num in self.board.numbers:
            if num.collides_with_mouse(x_mouse, y_mouse):
                """Only highlight the last piece on triangle if the triangle is
                   selected to start a move (as the origin of move) and the triangle
                   actually has piece."""
                if not self.area_selected and self.board.triangle_is_not_empty(num.value):
                    # Last piece on the triangle 
                    piece = self.board.pieces[num.value - 1][-1]
                    # only highight the piece if mid bar is empty.
                    if not self.mid_bar_has_piece():
                        if self.dice_rolled:
                            piece.highlight()
                return num.value
        return None


    def mid_bar_has_piece(self):
        pieces_in_mid = self.board.white_pieces_in_mid + self.board.black_pieces_in_mid
        if pieces_in_mid:
            return True
        return False

    # check if current area is mid bar and if it is not area selected on the
    # board is illegal so self.area_selected must be False
    def current_area_has_to_be_mid_bar(self):
        if self.current_area not in (BLACK_MID_BAR, WHITE_MID_BAR):
            self.area_selected = False
    
    def undo(self):
        if self.current_area == BLACK_MID_BAR:
            current_tri_pieces_list = self.board.black_pieces_in_mid
        elif self.current_area == WHITE_MID_BAR:
            current_tri_pieces_list = self.board.white_pieces_in_mid
        else:    
            current_tri_pieces_list = self.board.pieces[self.current_area - 1]
        current_piece = current_tri_pieces_list[-1]
        current_piece.dehighlight()
        self.area_selected = False

    def create_dices(self):
        dices = []
        for i in range(2):
            dices.append(Dice(40, 40, WHITE, 30 + i *50, 305))
        return dices
        

    def draw_dices(self, surface):
        for dice in self.dices:
            dice.draw(surface)

    def roll_dices(self):
        self.double_dice_rolled = False
        for dice in self.dices:
            dice.roll()
        if self.dices[0].dice_num == self.dices[1].dice_num:
            self.double_dice_rolled = True
        self.dice_rolled = True
        self.set_valid_moves()
        self.set_total_move_distance()
        self.set_total_no_of_moves()
    
    def check_for_button_click(self, x_mouse, y_mouse):
        for btn in self.board.buttons.values():
            if btn.collide_with_mouse(x_mouse, y_mouse):
                btn.clicked = True
                

    def this_buttuon_is_clicked(self, btn_name):
        btn = self.board.buttons[btn_name]
        if btn.clicked:
            btn.set_color(TAN)
        return btn.clicked


    def reset_button_colors(self):
        for btn in self.board.buttons.values():
            btn.set_color(WHITE)

    def unclick_all_buttons(self):
        for btn in self.board.buttons.values():
            btn.clicked = False


    def update(self, surface):
        self.board.draw_board(surface)
        if self.total_no_of_moves != 0:
            self.draw_dices(surface)
        if self.total_no_of_moves == 0:
            self.dice_rolled = False
        pygame.display.update()
