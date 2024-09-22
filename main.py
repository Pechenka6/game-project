import pygame 
import sys 
import random

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (187, 173, 160)
COLORS = {
    2 : (238, 228, 218),
    4 : (237, 224, 200),
    8 : (242, 177, 121),
    16 : (245, 149, 99),
    32 : (246, 124, 95),
    64 : (246, 94, 59),
    128 : (237, 207, 114),
    256 : (237, 204, 97),
    512 : (237, 200, 80),
    1024 : (237, 197, 63),
    2048 : (237, 194, 46)
}

SIZE = 4
TILE_SIZE = 100
TILE_MARGIN = 10
WIDTH = SIZE * TILE_SIZE + (SIZE + 1) * TILE_MARGIN
HEIGHT = WIDTH
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
font = pygame.font.Font(None, 48)

def draw_board(board):
    screen.fill(GREY)
    for row in range (SIZE):
        for col in range(SIZE):
            value = board[row][col]
            color = COLORS.get(value, BLACK)
            rect = pygame.Rect(
                col * TILE_SIZE + (col + 1) * TILE_MARGIN,
                row * TILE_SIZE + (row + 1) * TILE_MARGIN,
                TILE_SIZE,
                TILE_SIZE,
            )
            pygame.draw.rect(screen, color, rect)
            if value:
                text = font.render(str(value), True, BLACK if value <= 4 else WHITE)
                text_rect = text.get_rect(center=rect.center)
                screen.blit(text, text_rect)
    pygame.display.flip()

def main():
    board = [[0] * SIZE for _ in range(SIZE)]
    running = True
    while running:
        draw_board(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                continue
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
