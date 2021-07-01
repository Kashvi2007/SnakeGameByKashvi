# importing all the modules
import pygame
import random
from pygame.locals import *
import os

# initialising the modules
pygame.init()
pygame.mixer.init()

# Creating window
screen_width = 1200
screen_height = 1000
gameWindow = pygame.display.set_mode((screen_width, screen_height))

# Game Title
pygame.display.set_caption("Snakes game")
pygame.display.update()
clock = pygame.time.Clock()
font = pygame.font.SysFont('poor richard', 55)

# images
bg = pygame.image.load('images\\bg.jpg')
bg = pygame.transform.scale(bg, (screen_width, screen_height)).convert_alpha()

w_bg = pygame.image.load('images\\wallpaper_bg.jpg')
w_bg = pygame.transform.scale(
    w_bg, (screen_width, screen_height)).convert_alpha()

t_bg = pygame.image.load('images\\welcome_text.png')
t_bg = pygame.transform.scale(t_bg, (501, 304)).convert_alpha()

game_o_text = pygame.image.load('images\\game_over.png')
game_o_text = pygame.transform.scale(game_o_text, (701, 504)).convert_alpha()


# Colors
red = 255, 0, 0
black = 0, 0, 0

def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])


def plot_snake(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])


def welcome():
    exit_game = True
    pygame.mixer.music.load('music\\welcome.mp3')
    pygame.mixer.music.play()

    while exit_game:
        gameWindow.blit(w_bg, (0, 0))
        gameWindow.blit(t_bg, (300, 300))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = False

            if event.type == pygame.KEYDOWN:
                gameloop()
        

        pygame.display.update()
        clock.tick(40)


def gameloop():
    # global variables
    exit_game = False
    game_over = False

    snake_x = 45
    snake_y = 55

    velocity_x = 0
    velocity_y = 0

    snk_list = []
    snk_length = 1

    food_x = random.randint(20, screen_width / 2)
    food_y = random.randint(20, screen_height / 2)

    score = 0  # initial score will be 0
    speed = 5

    snake_size = 30
    fps = 40  # frames per second

    # reading and creating a file if it doesn't exist
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")
    with open("hiscore.txt", "r") as f:
        hiscore = f.read()

    pygame.mixer.music.load('music\\game.mp3')
    pygame.mixer.music.play()
    pygame.mixer.music.rewind()

    # Game Loop
    while not exit_game:

        # displaying and writing the hiscore of the game after the game loops exits
        if game_over:
            with open("hiscore.txt", "w") as f:
                f.write(str(hiscore))
            gameWindow.blit(game_o_text, (200, 100))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop()

        else:

            # handling the events in the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        velocity_x = speed
                        velocity_y = 0

                    if event.key == pygame.K_LEFT:
                        velocity_x = -speed
                        velocity_y = 0

                    if event.key == pygame.K_UP:
                        velocity_y = -speed
                        velocity_x = 0

                    if event.key == pygame.K_DOWN:
                        velocity_y = speed
                        velocity_x = 0

                    # cheat code
                    if event.key == pygame.K_q:
                        score += 10

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            # eating the food and incrementing the score
            if (
                abs(snake_x - food_x) < snake_size
                and abs(snake_y - food_y) < snake_size
            ):
                score += 10
                speed += 0.05
                food_x = random.randint(20, screen_width // 2)
                food_y = random.randint(20, screen_height // 2)
                snk_length += 5

                if score > int(hiscore) or hiscore == '':
                    hiscore = score

            # displaying the score on the screen
            gameWindow.blit(bg, (0, 0))
            text_screen(
                "Score: " + str(score) + "  Hiscore: " +
                str(hiscore), red, 5, 5
            )

            pygame.draw.rect(gameWindow, red, [
                             food_x, food_y, snake_size, snake_size])  # food

            # incrementing the length of the snake
            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                game_over = True
                pygame.mixer.music.load('music\\explosion.mp3')
                pygame.mixer.music.play()

            # ending the game when it crashes with the wall
            if (
                snake_x < 0
                or snake_x > screen_width
                or snake_y < 0
                or snake_y > screen_height
            ):
                game_over = True
                pygame.mixer.music.load('music\\explosion.mp3')
                pygame.mixer.music.play()

            plot_snake(gameWindow, black, snk_list, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()