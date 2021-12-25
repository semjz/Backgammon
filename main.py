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
                if game.board.area_selected:
                    game.dest_area = game.locate(x_mouse, y_mouse)
                    game.move()
                else:
                    game.current_area = game.locate(x_mouse, y_mouse)
                    if game.mid_bar_has_piece():
                        game.current_area_has_to_be_mid_bar()
                    game.check_current_area_has_piece()

        game.update(WIN)
     
    pygame.quit()

if __name__ == "__main__":
    main()

