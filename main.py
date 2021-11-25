import pygame
from constants import *
from board import Board

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Backgammon")


def main():
    pygame.init()
    running = True
    clock = pygame.time.Clock()

    board = Board()
    board.create_pieces_list()
    board.creat_numbers(WIN)

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                a = board.find_tri_number(pos[0], pos[1])
                
            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                b = board.find_tri_number(pos[0], pos[1])
                board.move(a, b)

        # set up the board
        board.draw(WIN)
        pygame.display.update()
        
    pygame.quit()

if __name__ == "__main__":
    main()
