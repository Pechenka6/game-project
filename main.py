import pygame 
import sys 
import random

pygame.init()

pygame.mixer.init()

pygame.mixer.music.load('background_music.mp3')  
pygame.mixer.music.play(-1)  

#merge_sound = pygame.mixer.Sound('merge_sound.wav')  

music_on = True
sound_on = True

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (187, 173, 160)
LIGHT_GREY = (200, 200, 200)
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
DIFFICULTY_OPTIONS = {
    "Easy": 1,
    "Medium": 1.5,
    "Hard": 2
}

SIZE = 4
TILE_SIZE = 100
TILE_MARGIN = 10
MAX_VALUE = 2048
WIDTH = 450
HEIGHT = 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")
font = pygame.font.Font(None, 48)

def draw_board(board):
    screen.fill(GREY)
    for row in range (len(board)):
        for col in range(len(board)):
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
    empty_tiles = [[row, col] for row in range(len(board)) for col in range(len(board)) if board[row][col] == 0]
    if empty_tiles:
        row, col = random.choice(empty_tiles)
        board[row][col] = 2 if random.random() < 0.9 else 4

def rotate_board(board):
    return [[board[col][row] for col in range(len(board))] for row in range(len(board) - 1, -1, -1)]

def move_left(board):
    new_board = [[0] * len(board) for _ in range(len(board))]
    for row in range(len(board)):
        col_new = 0
        last = 0
        for col in range(len(board)):
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

def game_over(board, diffficulty):
    if 2048 in board:
         return True
    for row in range(len(board)):
        for col in range(len(board)):
            if board[row][col] == 0:
                return False
            if board[row][col] == 2048 * (8 ** (diffficulty - 1)) ** 2:
                return True
            if col < len(board) - 1 and board[row][col] == board[row][col + 1]:
                return False
            if row < len(board) - 1 and board[row][col] == board[row + 1][col]:
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

def draw_button(text, x, y, width, height, color, hover_color):
    mouse = pygame.mouse.get_pos()
    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(screen, hover_color, (x, y, width, height))
    else:
        pygame.draw.rect(screen, color, (x, y, width, height))
    draw_text(text, font, BLACK, screen, x + width // 2, y + height // 2)
    
def main_menu():
    while True:
        screen.fill(GREY)
        draw_text("Main Menu", font, WHITE, screen, WIDTH // 2, HEIGHT // 4)

        draw_button("Play", 125, 150, 200, 50, LIGHT_GREY, WHITE)
        draw_button("Settings", 125, 220, 200, 50, LIGHT_GREY, WHITE)
        draw_button("Exit", 125, 290, 200, 50, LIGHT_GREY, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 125 <= event.pos[0] <= 325:
                    if 150 <= event.pos[1] <= 200:
                        difficulty_menu()
                    elif 220 <= event.pos[1] <= 270:
                        settings_menu()
                    elif 290 <= event.pos[1] <= 340:
                        pygame.quit()
                        sys.exit()

        pygame.display.flip()

def difficulty_menu():
    while True:
        screen.fill(GREY)
        draw_text("Select Difficulty", font, WHITE, screen, WIDTH // 2, HEIGHT // 4)

        y_position = 150
        for difficulty in DIFFICULTY_OPTIONS.keys():
            draw_button(difficulty, 125, y_position, 200, 50, LIGHT_GREY, WHITE)
            y_position += 70

        draw_button("Back", 125, y_position, 200, 50, LIGHT_GREY, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 125 <= event.pos[0] <= 325:
                    if 150 <= event.pos[1] <= 200:
                        start_game(DIFFICULTY_OPTIONS["Easy"])
                    elif 220 <= event.pos[1] <= 270:
                        start_game(DIFFICULTY_OPTIONS["Medium"])
                    elif 290 <= event.pos[1] <= 340:
                        start_game(DIFFICULTY_OPTIONS["Hard"])
                    elif y_position <= event.pos[1] <= y_position + 50:
                        return  

        pygame.display.flip()

def settings_menu():
    global music_on, sound_on
    while True:
        screen.fill(GREY)
        draw_text("Settings", font, WHITE, screen, WIDTH // 2, HEIGHT // 4)

        draw_button(f"Music: {'On' if music_on else 'Off'}", 125, 150, 200, 50, LIGHT_GREY, WHITE)
        draw_button(f"Sound: {'On' if sound_on else 'Off'}", 125, 220, 200, 50, LIGHT_GREY, WHITE)
        draw_button("Back", 125, 290, 200, 50, LIGHT_GREY, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 125 <= event.pos[0] <= 325:
                    if 150 <= event.pos[1] <= 200:
                        music_on = not music_on
                        if music_on:
                            pygame.mixer.music.play(-1)
                        else:
                            pygame.mixer.music.stop() 
                    elif 220 <= event.pos[1] <= 270:
                        sound_on = not sound_on
                    elif 290 <= event.pos[1] <= 340:
                        return 
        pygame.display.flip()

def pause_menu():
    while True:
        screen.fill(GREY)
        draw_text("Paused", font, WHITE, screen, WIDTH // 2, 50)

        button_height = 50
        button_spacing = 20
        total_height = (button_height * 3) + (button_spacing * 2)  
        start_y = (HEIGHT - total_height) // 2 

        draw_button("Resume", 125, 80, 200, 50, LIGHT_GREY, WHITE)
        draw_button("Settings", 125, 150, 200, 50, LIGHT_GREY, WHITE)
        draw_button("Main menu", 125, 220, 200, 50, LIGHT_GREY, WHITE)
        draw_button("Exit", 125, 290, 200, 50, LIGHT_GREY, WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if 125 <= event.pos[0] <= 325:
                    if 80 <= event.pos[1] <= 130:
                        return
                    elif 150 <= event.pos[1] <= 200:
                        settings_menu()
                    elif 220 <= event.pos[1] <= 270:
                        return main_menu()
                    elif 290 <= event.pos[1] <= 340:
                        pygame.quit()
                        sys.exit()
        pygame.display.flip()



def start_game(diffficulty):
    size = int(SIZE * diffficulty)
    global WIDTH, HEIGHT, screen
    WIDTH = size * TILE_SIZE + (size + 1) * TILE_MARGIN
    HEIGHT = WIDTH
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    board = [[0] * size for _ in range(size)]
    running = True
    game_paused = False
    add_new_tile(board)
    add_new_tile(board)
    while running:
        if game_paused:
            pause_menu()
            game_paused = False 

        screen.fill(GREY)
        draw_text("Game Running", font, WHITE, screen, WIDTH // 2, HEIGHT // 4)  
        draw_board(board)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_over(board, diffficulty):
                    display_game_over_message()
                    running = False
                    main_menu()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  
                    game_paused = True
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
        draw_board(board)
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main_menu()
    