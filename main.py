import pygame
from game import Game
from constants import *


FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Backgammon")


def main():
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
                x_mouse, y_mouse = pos[0], pos[1]
                current_tri = game.locate(x_mouse, y_mouse)
                
                
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                x_mouse, y_mouse = pos[0], pos[1]
                dest_tri = game.locate(x_mouse, y_mouse)
                
                if current_tri == "white mid bar" or current_tri == "black mid bar":
                    game.move_from_mid_bar_to_board(current_tri, dest_tri)
                    
                elif dest_tri == "white place holder" or dest_tri == "black place holder":
                    game.move_to_piece_holder(current_tri, dest_tri)
                
                else:
                    game.move_on_board(current_tri, dest_tri)

        # set up the board
        game.draw_board(WIN)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()

