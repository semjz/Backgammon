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
                # select a destination on board for move.
                if game.area_selected:
                    game.dest_area = game.locate(x_mouse, y_mouse)
                    # if destination selected is legal destination.
                    if game.dest_area is not None:
                        game.move()
                # select an origin on board for move.
                else:
                    game.current_area = game.locate(x_mouse, y_mouse)
                    # if area selected is a valid origin.
                    if game.current_area is not None:
                        game.area_selected = True
                        # if mid bar has a piece, area selected must be mid bar
                        if game.mid_bar_has_piece():
                            # if current area is not mid bar game.selected_area will
                            # be assigned to False in method below, so another origin 
                            # must be selected so code in else block is repeated.
                            game.current_area_has_to_be_mid_bar()
                        # check if current area selected if legal has a pieace
                        game.check_current_area_has_piece()

        game.update(WIN)
     
    pygame.quit()

if __name__ == "__main__":
    main()

