from utils import *
import pygame
import time
import math

#loading and scaling images
GRASS = scale(pygame.image.load('imgs/grass.jpg'), 2.5)
TRACK = scale(pygame.image.load('imgs/track.png'), 0.9)
BORDER = scale(pygame.image.load('imgs/track-border.png'),0.9)
FINISH = pygame.image.load('imgs/finish.png')
CAR = scale(pygame.image.load('imgs/car.png'),0.18)

#initalizing window
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("riyas a bitch")

FPS = 60

class Car:
    IMG = CAR
    START = (160,200)
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START

    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw_car(self, screen):
        rotate_center(screen, self.img, (self.x, self.y), self.angle)

def draw(screen, images, player):
    for img, pos in images:
        screen.blit(img, pos)

    player.draw_car(screen)
    pygame.display.update()


run = True
clock = pygame.time.Clock()
images = [(GRASS, (0,0)), (TRACK, (0,0))]
player = Car(4,4)


pygame.display.update()

while run:
    clock.tick(FPS)

    draw(SCREEN, images, player)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
pygame.quit()