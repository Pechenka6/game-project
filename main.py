import pygame 
import sys 
import random

pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (187,173,160)

SIZE = 4
TILE_SIZE = 100
TILE_MARGIN = 10
WIDTH = SIZE * TILE_SIZE + (SIZE + 1) * TILE_MARGIN
HEIGHT = WIDTH
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
font = pygame.font.Font(None, 48)

def main():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                continue
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()