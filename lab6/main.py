import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 2
screen_width = 1200
screen_heigh = 900
screen = pygame.display.set_mode((screen_width, screen_heigh))

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

# 0 - x, 1 - y, 2 - r, 3 - v_x, 4 - v_y
balls = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]]


score = 0


def new_ball(ball_n):
    balls[ball_n][0] = randint(100, 700)
    balls[ball_n][1] = randint(100, 500)
    balls[ball_n][2] = randint(30, 50)
    balls[ball_n][3] = randint(1, 50)
    balls[ball_n][4] = randint(1, 50)
    balls[ball_n][5] = COLORS[randint(0, 5)]


def draw_ball(ball_n):
    circle(screen, balls[ball_n][5], (balls[ball_n][0], balls[ball_n][1]), balls[ball_n][2])


def move_ball(ball_n):
    r = balls[ball_n][2]
    balls[ball_n][0] += balls[ball_n][3]
    balls[ball_n][1] += balls[ball_n][4]
    if (balls[ball_n][0] <= r) or (balls[ball_n][0] >= screen_width - r):
        balls[ball_n][3] *= -1
    if (balls[ball_n][1] <= r) or (balls[ball_n][1] >= screen_heigh - r):
        balls[ball_n][4] *= -1


def click(event):
    global score
    for i in range(len(balls)):
        if (event.pos[0] - balls[i][0]) ** 2 + (event.pos[1] - balls[i][1]) ** 2 <= balls[i][2] ** 2:
            score += 1
            new_ball(i)


pygame.display.update()
clock = pygame.time.Clock()
for i in range(len(balls)):
    new_ball(i)
    draw_ball(i)
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print(score)
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    for i in range(len(balls)):
        draw_ball(i)
        move_ball(i)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
