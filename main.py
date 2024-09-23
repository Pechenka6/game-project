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

SIZE = 2
TILE_SIZE = 100
TILE_MARGIN = 10
MAX_VALUE = 2048
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

def add_new_tile(board):
    empty_tiles = [[row, col] for row in range(SIZE) for col in range(SIZE) if board[row][col] == 0]
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        board[row][col] = 2 if random.random() < 0.9 else 4

def rotate_board(board):
    return [[board[col][row] for col in range(SIZE)] for row in range(SIZE - 1, -1, -1)]

def move_left(board):
    new_board = [[0] * SIZE for _ in range(SIZE)]
    for row in range(SIZE):
        col_new = 0
        last = 0
        for col in range(SIZE):
            if board[row][col] != 0:
                if last == 0:
                    last = board[row][col]
                elif last == board[row][col]:
                    new_board[row][col_new] = 2 * last
                    col_new += 1
                    last = 0
                else:
                    new_board[row][col_new] = last
                    col_new += 1
                    last = board[row][col]
        if last != 0:
            new_board[row][col_new] = last
    return new_board

def game_over(board):
    for row in range(SIZE):
        for col in range(SIZE):
            if board[row][col] == 0:
                return False
            if board[row][col] == 2048:
                return True
            if col < SIZE - 1 and board[row][col] == board[row][col + 1]:
                return False
            if row < SIZE - 1 and board[row][col] == board[row + 1][col]:
                return False
    return True

def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def display_game_over_message():
    draw_text("Game over!", font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
    pygame.display.flip()
    pygame.time.wait(2000)


def main():
    board = [[0] * SIZE for _ in range(SIZE)]
    running = True
    add_new_tile(board)
    add_new_tile(board)
    while running:
        draw_board(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_LEFT, pygame.K_a):
                    board = move_left(board)
                elif event.key in (pygame.K_RIGHT, pygame.K_d):
                    board = rotate_board(board)
                    board = rotate_board(board)
                    board = move_left(board)
                    board = rotate_board(board)
                    board = rotate_board(board)
                elif event.key in (pygame.K_UP, pygame.K_w):
                    board = rotate_board(board)
                    board = move_left(board)
                    board = rotate_board(board)
                    board = rotate_board(board)
                    board = rotate_board(board)
                elif event.key in (pygame.K_DOWN, pygame.K_s):
                    board = rotate_board(board)
                    board = rotate_board(board)
                    board = rotate_board(board)
                    board = move_left(board)
                    board = rotate_board(board)
                add_new_tile(board)
                if game_over(board):
                    display_game_over_message()
                    running = False
        draw_board(board)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
    