import pygame
from pygame.locals import *
import random

# Color
COLOR_BLACK = ((0, 0, 0))
COLOR_WHITE = ((255, 255, 255))
COLOR_RED = ((255, 0, 0))

# Config Game
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Pong')
screen_ret = screen.get_rect()
clock = pygame.time.Clock()
FPS = 30


class Racket:
    def __init__(self, image):
        self.image = pygame.Surface((10, 50))
        self.image.fill(COLOR_WHITE)
        self.image_ret = self.image.get_rect()
        self.image_ret[0] = 20
        self.image_ret[1] = 250

    def move(self, vx, vy):
        self.image_ret.move_ip(vx, vy)

    def realize_racket(self):
        screen.blit(self.image, self.image_ret)
        self.image_ret.clamp_ip(screen.get_rect())

racket = Racket((10, 10))
vx = 0
vy = 0
uppress = False
downpress = False


class Ball:
    def __init__(self, image):
            self.image = pygame.Surface((10, 10))
            self.image.fill(COLOR_RED)
            self.image_ret = self.image.get_rect()
            self.velocity = 15
            self.set_ball()

    def random(self):
        while True:
            num = random.uniform(-1.0, 1.0)
            if num > -.5 and num < 0.5:
                continue
            else:
                return num

    def set_ball(self):
        x = self.random()
        y = self.random()
        self.image_ret.x = screen_ret.centerx
        self.image_ret.y = screen_ret.centery
        self.speed = [x, y]
        self.pos = list(screen_ret.center)

    def colission_wall(self):
        if self.image_ret.y < 0 or self.image_ret.y > screen_ret.bottom:
            self.speed[1] *= -1

        if self.image_ret.x < 0 or self.image_ret.x > screen_ret.right:
            self.speed[0] *= -1
            if self.image_ret.x < 0:
                score.points -= 1

    def colission_racket(self, racket_ret):
        if self.image_ret.colliderect(racket_ret):
            score.points += 1
            self.speed[0] *= -1

    def move(self):
        self.pos[0] += self.speed[0] * self.velocity
        self.pos[1] += self.speed[1] * self.velocity
        self.image_ret.center = self.pos

    def update(self, racket_ret):
        self.colission_racket(racket_ret)
        self.colission_wall()
        self.move()

    def realize_ball(self):
        screen.blit(self.image, self.image_ret)

ball = Ball((15, 15))


class Score:
    def __init__(self):
        pygame.font.init()
        self.font = pygame.font.Font(None, 36)
        self.points = 10

    def count(self):
        self.text = self.font.render('Points: ' + str(self.points), 1, (COLOR_WHITE))
        self.textpos = self.text.get_rect()
        self.textpos.centerx = screen.get_width() / 2
        screen.blit(self.text, self.textpos)
        screen.blit(screen, (0, 0))

    def lose(self):
        if self.points == 0:
            pygame.quit()

score = Score()


game_over = False
while game_over != True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                uppress = True
                vy = -10
            if event.key == pygame.K_DOWN:
                downpress = True
                vy = 10

        if event.type == pygame.KEYUP:
            if event.key == K_UP:
                uppress = False
                if downpress:
                    vy = 10
                else:
                    vy = 0
            if event.key == K_DOWN:
                downpress = False
                if uppress:
                    vy = -10
                else:
                    vy = 0

    screen.fill(COLOR_BLACK)

    racket.realize_racket()
    racket.move(vx, vy)

    ball.realize_ball()
    ball.update(racket.image_ret)

    score.count()
    score.lose()

    pygame.display.update()

pygame.quit()
