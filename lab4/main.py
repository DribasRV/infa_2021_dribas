import pygame
from pygame.draw import *

pygame.init()

window_w = 600
window_h = 800
FPS = 30
screen = pygame.display.set_mode((window_w, window_h))


# background
def bg_bird(x, y, angle):
    pass


def bg():
    h1 = window_h * 0.1
    h2 = window_h * 0.05
    h3 = window_h * 0.1
    h4 = window_h * 0.15
    h5 = window_h * 0.1
    h6 = window_h * 0.5
    rect(screen, (33,33,120), (0, 0, window_w, h1))
    rect(screen, (141,95,211), (0, h1, window_w, h2))
    rect(screen, (205,135,222), (0, h2, window_w, h3))
    rect(screen, (222,135,170), (0, h3, window_w, h4))
    rect(screen, (255,153,85), (0, h4, window_w, h5))
    rect(screen, (0,102,128), (0, h5, window_w, h6))


# bird
def bird_head():
    pass


def bird_wing():
    pass


def bird_paw():
    pass


def bird():
    pass


# fish
def fish_eye():
    pass


def fish_head():
    pass


def fish_fin():
    pass


def fish_body():
    pass


def fish():
    pass

bg()
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True


pygame.quit()