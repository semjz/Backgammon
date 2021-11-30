import pygame
from game import Game
from board import Board
from constants import *


FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Backgammon")


def main():
    pygame.init()
    running = True
    clock = pygame.time.Clock()
    
    game = Game()

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                current_tri = game.select(pos[0], pos[1])
                
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                dest_tri = game.select(pos[0], pos[1])
                if(game.move(current_tri, dest_tri, game.turn)):
                    game.change_turn()
                
        # set up the board
        game.update_baord(WIN)
        # print(board.board_pieces_list)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()
