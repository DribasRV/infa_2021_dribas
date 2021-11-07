import math
from random import choice
from random import randint

import pygame

FPS = 30

RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = 0x000000
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 800
HEIGHT = 600


class Ball:
    def __init__(self, screen: pygame.Surface, x=40, y=450):
        """ Конструктор класса ball

        Args:
        x - начальное положение мяча по горизонтали
        y - начальное положение мяча по вертикали
        """
        self.screen = screen
        self.x = x
        self.y = y
        self.r = 10
        self.vx = 0
        self.vy = 0
        self.color = choice(GAME_COLORS)
        self.live = 30

    def move(self):
        """Переместить мяч по прошествии единицы времени.

        Метод описывает перемещение мяча за один кадр перерисовки. То есть, обновляет значения
        self.x и self.y с учетом скоростей self.vx и self.vy, силы гравитации, действующей на мяч,
        и стен по краям окна (размер окна 800х600).
        """
        if self.x < 0:
            self.vx *= -0.75
            self.x = 0
        elif self.x > WIDTH:
            self.vx *= -0.75
            self.x = WIDTH
        if self.y < 0:
            self.vy *= -0.75
            self.vx *= 0.95
            self.y = 0
        elif self.y > HEIGHT:
            self.vy *= -0.75
            self.vx *= 0.95
            self.y = HEIGHT
        self.x += self.vx
        self.y += self.vy
        self.vy += 1

    def draw(self):
        pygame.draw.circle(
            self.screen,
            self.color,
            (self.x, self.y),
            self.r
        )

    def hittest(self, obj):
        """Функция проверяет сталкивалкивается ли данный обьект с целью, описываемой в обьекте obj.

        Args:
            obj: Обьект, с которым проверяется столкновение.
        Returns:
            Возвращает True в случае столкновения мяча и цели. В противном случае возвращает False.
        """
        if (self.x - obj.x) ** 2 + (self.y - obj.y) ** 2 <= (self.r + obj.r) ** 2:
            return True
        else:
            return False


class Gun:
    vx = 0
    vy = 0

    def __init__(self, screen):
        self.screen = screen
        self.f2_power = 10
        self.f2_on = 0
        self.an = 1
        self.color = GREY
        self.x = 20
        self.y = 450
        self.width = 40
        self.height = 100
        self.picture = slippers[0]

    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):
        """Выстрел мячом.

        Происходит при отпускании кнопки мыши.
        Начальные значения компонент скорости мяча vx и vy зависят от положения мыши.
        """
        global balls, bullet
        bullet += 1
        new_ball = Ball(self.screen, self.x, self.y)
        new_ball.r += 5
        self.an = math.atan2((event.pos[1] - new_ball.y), (event.pos[0] - new_ball.x))
        new_ball.vx = self.f2_power * math.cos(self.an)
        new_ball.vy = self.f2_power * math.sin(self.an)
        balls.append(new_ball)
        self.f2_on = 0
        self.f2_power = 10

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            self.an = math.atan2((self.y - event.pos[1]), (event.pos[0] - self.x))
        if self.f2_on:
            self.picture = slippers[1]
        else:
            self.picture = slippers[0]

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0:
            self.x = 0
        elif self.x > WIDTH:
            self.x = WIDTH
        if self.y < 0:
            self.y = 0
        elif self.y > HEIGHT:
            self.y = HEIGHT

    def draw(self):
        slipper = pygame.transform.scale(self.picture, (int(self.width + 2 * self.f2_power), self.height))
        slipper = pygame.transform.rotate(slipper, self.an * 180 / math.pi)
        screen.blit(slipper, (self.x, self.y - ((self.width ** 2 + self.height ** 2) ** 0.5) * math.sin(self.an)))

    def power_up(self):
        if self.f2_on:
            if self.f2_power < 100:
                self.f2_power += 1
            self.color = RED
        else:
            self.color = GREY


class Target:
    points = 0
    live = 1
    screen = pygame.Surface((0, 0))
    x = 0
    y = 0
    vx = 0
    vy = 0
    r = 1
    color = RED

    def refresh(self, screen):
        self.screen = screen
        self.live = 1
        self.x = randint(600, 780)
        self.y = randint(300, 550)
        self.vx = randint(-5, 5)
        self.vy = randint(-5, 5)
        self.r = randint(2, 50)
        self.color = RED
        self.picture = choice(cockroaches)

    def __init__(self, screen):
        """ Инициализация новой цели. """
        self.refresh(screen)

    def hit(self, pts=1):
        """Попадание шарика в цель."""
        pass

    def move(self):
        self.x += self.vx
        self.y += self.vy
        if self.x < 0:
            self.vx *= -1
            self.x = 0
        elif self.x > WIDTH:
            self.vx *= -1
            self.x = WIDTH
        if self.y < 0:
            self.vy *= -1
            self.y = 0
        elif self.y > HEIGHT:
            self.vy *= -1
            self.y = HEIGHT

    def draw(self):
        cockroach = pygame.transform.scale(self.picture, (int(2 * self.r), int(2 * self.r)))
        screen.blit(cockroach, (int(self.x - self.r), int(self.y - self.r)))


def display_points():
    screen.blit(Font.render('Your points: ' + str(points), True, BLACK), (25, 25))


def display_bullets():
    screen.blit(Font.render('Targets killed for ' + str(bullets) + ' balls', True, BLACK), (25, 75))


pygame.init()
Font = pygame.font.SysFont('Comic Sans', 40)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
balls = []

cockroaches = [pygame.image.load('files/pictures/cockroach_1.png'), pygame.image.load('files/pictures/cockroach_2.png')]
slippers = [pygame.image.load('files/pictures/slipper_normal.png'), pygame.image.load('files/pictures/slipper_red.png')]

points = 0
bullet = 0
bullets = 0
frames_with_bullets = 0

clock = pygame.time.Clock()
gun = Gun(screen)
number_of_targets = 2
targets = [Target(screen) for i in range(number_of_targets)]
finished = False

while not finished:
    screen.fill(WHITE)
    gun.draw()
    for t in targets:
        if t.live:
            t.draw()
    for b in balls:
        b.draw()
    display_points()
    if frames_with_bullets != 0:
        frames_with_bullets -= 1
        display_bullets()
    pygame.display.update()

    clock.tick(FPS)
    moved = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            gun.fire2_start(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            gun.fire2_end(event)
        elif event.type == pygame.MOUSEMOTION:
            gun.targetting(event)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                gun.vy = -5
            elif event.key == pygame.K_s:
                gun.vy = 5
            elif event.key == pygame.K_a:
                gun.vx = -5
            elif event.key == pygame.K_d:
                gun.vx = 5
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                gun.vy = 0
            elif event.key == pygame.K_s:
                gun.vy = 0
            elif event.key == pygame.K_a:
                gun.vx = 0
            elif event.key == pygame.K_d:
                gun.vx = 0

    for b in balls:
        b.move()
        for t in targets:
            if b.hittest(t) and t.live:
                t.live = 0
                t.hit()

    hitted = True
    for t in targets:
        if t.live == 1:
            hitted = False
    if hitted:
        bullets = bullet
        bullet = 0
        points += 1
        balls = []
        frames_with_bullets = 150
        for t in targets:
            t.refresh(screen)

    for t in targets:
        t.move()

    gun.move()
    gun.power_up()

pygame.quit()
