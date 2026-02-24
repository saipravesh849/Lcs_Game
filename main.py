import pygame
import sys

pygame.init()


WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LCS Hybrid Visualizer - Stable Version")

font = pygame.font.SysFont(None, 36)
small_font = pygame.font.SysFont(None, 26)


WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (50,50,255)
GREEN = (0,200,0)
RED = (200,0,0)
GRAY = (180,180,180)
LIGHT_GRAY = (230,230,230)
YELLOW = (255,255,0)

clock = pygame.time.Clock()


input_box1 = pygame.Rect(150, 50, 400, 40)
input_box2 = pygame.Rect(150, 110, 400, 40)


restart_button = pygame.Rect(800, 600, 120, 40)
quit_button = pygame.Rect(950, 600, 120, 40)


str1 = ""
str2 = ""
active_box = None

dp = []
rows = 0
cols = 0
cell_size = 35

i_build = 1
j_build = 1

back_i = 0
back_j = 0

lcs_result = ""

game_state = "input"  



def reset_game():
    global str1, str2, dp, rows, cols
    global active_box, lcs_result
    global i_build, j_build, back_i, back_j
    global game_state

    str1 = ""
    str2 = ""
    dp = []
    rows = 0
    cols = 0
    active_box = None
    lcs_result = ""

    i_build = 1
    j_build = 1
    back_i = 0
    back_j = 0

    game_state = "input"


def initialize_lcs():
    global dp, rows, cols, i_build, j_build, back_i, back_j

    rows = len(str1) + 1
    cols = len(str2) + 1
    dp = [[0]*cols for _ in range(rows)]

    i_build = 1
    j_build = 1

    back_i = rows - 1
    back_j = cols - 1



def draw():
    screen.fill(WHITE)

    title = font.render("LCS Hybrid Visualizer", True, BLACK)
    screen.blit(title, (400, 10))

    
    screen.blit(small_font.render("String 1:", True, BLACK), (50, 60))
    screen.blit(small_font.render("String 2:", True, BLACK), (50, 120))

   
    c1 = BLUE if active_box == 1 else GRAY
    c2 = BLUE if active_box == 2 else GRAY

    pygame.draw.rect(screen, LIGHT_GRAY, input_box1)
    pygame.draw.rect(screen, LIGHT_GRAY, input_box2)
    pygame.draw.rect(screen, c1, input_box1, 2)
    pygame.draw.rect(screen, c2, input_box2, 2)

    screen.blit(font.render(str1, True, BLACK), (input_box1.x+5, input_box1.y+5))
    screen.blit(font.render(str2, True, BLACK), (input_box2.x+5, input_box2.y+5))

    
    if game_state != "input":
        start_x = 100
        start_y = 200

        for i in range(rows):
            for j in range(cols):

                rect = pygame.Rect(start_x + j*cell_size,
                                   start_y + i*cell_size,
                                   cell_size, cell_size)

                
                if game_state == "backtrack" and (i == back_i and j == back_j):
                    pygame.draw.rect(screen, YELLOW, rect)

                pygame.draw.rect(screen, BLACK, rect, 1)

                value = small_font.render(str(dp[i][j]), True, BLUE)
                screen.blit(value, (rect.x+8, rect.y+8))

    
    if game_state == "result":

        screen.blit(font.render(f"LCS: {lcs_result}", True, GREEN), (750, 450))
        screen.blit(font.render(f"Length: {len(lcs_result)}", True, RED), (750, 500))

        pygame.draw.rect(screen, GREEN, restart_button)
        pygame.draw.rect(screen, RED, quit_button)

        screen.blit(small_font.render("Restart", True, WHITE),
                    (restart_button.x+25, restart_button.y+10))
        screen.blit(small_font.render("Quit", True, WHITE),
                    (quit_button.x+35, quit_button.y+10))

    pygame.display.update()



running = True

while running:
    clock.tick(12)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        
        if game_state == "input":

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box1.collidepoint(event.pos):
                    active_box = 1
                elif input_box2.collidepoint(event.pos):
                    active_box = 2
                else:
                    active_box = None

            if event.type == pygame.KEYDOWN and active_box is not None:

                if event.key == pygame.K_RETURN:
                    if active_box == 1:
                        active_box = 2
                    else:
                        if str1 and str2:
                            initialize_lcs()
                            game_state = "build"

                elif event.key == pygame.K_BACKSPACE:
                    if active_box == 1:
                        str1 = str1[:-1]
                    else:
                        str2 = str2[:-1]

                else:
                    if event.unicode.isprintable():
                        if active_box == 1:
                            str1 += event.unicode
                        else:
                            str2 += event.unicode

        
        elif game_state == "build":

            if i_build < rows:
                if str1[i_build-1] == str2[j_build-1]:
                    dp[i_build][j_build] = 1 + dp[i_build-1][j_build-1]
                else:
                    dp[i_build][j_build] = max(dp[i_build-1][j_build],
                                               dp[i_build][j_build-1])

                j_build += 1
                if j_build >= cols:
                    j_build = 1
                    i_build += 1
            else:
                game_state = "backtrack"

        
        elif game_state == "backtrack":

            if back_i > 0 and back_j > 0:
                if str1[back_i-1] == str2[back_j-1]:
                    lcs_result = str1[back_i-1] + lcs_result
                    back_i -= 1
                    back_j -= 1
                elif dp[back_i-1][back_j] > dp[back_i][back_j-1]:
                    back_i -= 1
                else:
                    back_j -= 1
            else:
                game_state = "result"

        
        elif game_state == "result":

            if event.type == pygame.MOUSEBUTTONDOWN:

                if restart_button.collidepoint(event.pos):
                    reset_game()

                elif quit_button.collidepoint(event.pos):
                    running = False

    draw()

pygame.quit()
sys.exit()