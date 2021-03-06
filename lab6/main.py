import pygame
from pygame.draw import *
from random import randint

pygame.init()

FPS = 50
screen_width = 1200
screen_heigh = 900

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
targets = [[0, 0, 0, 0, 0, 0]]


score = 0


def new_ball(i):
    """
    Changes ball parameters in balls[]
    :param i: place in list
    """
    balls[i][0] = randint(100, 700)
    balls[i][1] = randint(100, 500)
    balls[i][2] = randint(30, 50)
    balls[i][3] = randint(1, 10)
    balls[i][4] = randint(1, 10)
    balls[i][5] = COLORS[randint(0, 5)]


def draw_ball(i):
    """
    Draws ball with parameters from balls[i]
    :param i: place in list
    """
    circle(screen, balls[i][5], (balls[i][0], balls[i][1]), balls[i][2])


def move_ball(i):
    """
    Changes ball cords in balls[i]
    :param i: place in list
    """
    r = balls[i][2]
    balls[i][0] += balls[i][3]
    balls[i][1] += balls[i][4]
    if (balls[i][0] <= r) or (balls[i][0] >= screen_width - r):
        balls[i][3] *= -1
    if (balls[i][1] <= r) or (balls[i][1] >= screen_heigh - r):
        balls[i][4] *= -1


def new_target(i):
    """
    Changes target parameters in targets[]
    :param i: place in list
    """
    targets[i][0] = randint(100, 700)
    targets[i][1] = randint(100, 500)
    targets[i][2] = randint(10, 20)
    targets[i][3] = randint(10, 30)
    targets[i][4] = randint(10, 30)
    targets[i][5] = COLORS[randint(0, 5)]


def draw_target(i):
    """
    Draws target with parameters from targets[i]
    :param i: place in list
    """
    rect(screen, targets[i][5], (targets[i][0], targets[i][1], targets[i][2], targets[i][2]))


def move_target(i):
    """
    Changes target cords in targets[i]
    :param i: place in list
    """
    r = targets[i][2]
    targets[i][0] += targets[i][3]
    targets[i][1] += targets[i][4]
    if (targets[i][0] <= r) or (targets[i][0] >= screen_width - r):
        targets[i][3] *= -1
    if (targets[i][1] <= r) or (targets[i][1] >= screen_heigh - r):
        targets[i][4] *= -1


def turn_target(i):
    """
    Reverses speed of target from targets[i]
    :param i: place in list
    """
    targets[i][3] *= -1
    targets[i][4] *= -1


def click(event):
    """
    Handles the event
    :param event: handled event
    """
    global score
    for i in range(len(balls)):
        if (event.pos[0] - balls[i][0]) ** 2 + (event.pos[1] - balls[i][1]) ** 2 <= balls[i][2] ** 2:
            score += 1
            new_ball(i)
    for i in range(len(targets)):
        if ((event.pos[0] - targets[i][0]) ** 2 <= targets[i][2] ** 2) and ((event.pos[1] - targets[i][1]) ** 2 <= targets[i][2] ** 2):
            score += 5
            new_target(i)
        elif ((event.pos[0] - targets[i][0]) ** 2 <= (targets[i][2] * 3) ** 2) and ((event.pos[1] - targets[i][1]) ** 2 <= (targets[i][2] * 3) ** 2):
            turn_target(i)


def end_game():
    """
    Adds record into bestplayers.txt
    """
    filein = open('bestplayers.txt', 'r')
    file = filein.readlines()
    record = str(score) + ' ' + name
    max = 0
    max_i = len(file)
    name_used = False
    for i in range(len(file)):
        symbols = file[i].split(maxsplit=1)
        if symbols[1] == name + '\n':
            name_used = True
            if score > int(symbols[0]):
                del file[i]
                symbols = file[0].split()
                if score > int(symbols[0]):
                    file.insert(0, record + '\n')
                else:
                    for i in range(len(file)):
                        symbols = file[i].split()
                        if score > int(symbols[0]) > max:
                            max = int(symbols[0])
                            max_i = i
                    file.insert(max_i, record + '\n')
    if name_used == False:
        symbols = file[0].split()
        if score > int(symbols[0]):
            file.insert(0, record + '\n')
        else:
            for i in range(len(file)):
                symbols = file[i].split()
                if score > int(symbols[0]) > max:
                    max = int(symbols[0])
                    max_i = i
            file.insert(max_i, record + '\n')
    fileout = open('bestplayers.txt', 'w')
    for i in range(len(file)):
        fileout.write(file[i])


def text_to_screen(screen, text, x, y, size = 50, color = (200, 000, 000)):
    """
    Displays score on screen
    :param screen:
    :param text:
    :param x:
    :param y:
    :param size:
    :param color:
    """
    text = str(text)
    font = pygame.font.SysFont('Comic Sans MS', size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))


print('Enter your name:')
name = input()

screen = pygame.display.set_mode((screen_width, screen_heigh))
myfont = pygame.font.SysFont('Comic Sans MS', 30)

pygame.display.update()
clock = pygame.time.Clock()
for i in range(len(balls)):
    new_ball(i)
    draw_ball(i)
for i in range(len(targets)):
    new_target(i)
    draw_target(i)
text_to_screen(screen, 'Score:' + str(score), 0, 0)
finished = False
soundtrack = pygame.mixer.Sound('soundtrack.mp3')
soundtrack.play()

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT or score == 99:
            soundtrack.stop()
            end_game()
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click(event)
    for i in range(len(balls)):
        draw_ball(i)
        move_ball(i)
    for i in range(len(targets)):
        draw_target(i)
        move_target(i)
    text_to_screen(screen, 'Score:' + str(score), 0, 0)
    pygame.display.update()
    screen.fill(BLACK)

pygame.quit()
