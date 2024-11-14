from utils import *
from car import*
import pygame
import time
import math

#loading and scaling images
GRASS = scale(pygame.image.load('imgs/grass.jpg'), 2.5)
TRACK = scale(pygame.image.load('imgs/track.png'), 0.9)
BORDER = scale(pygame.image.load('imgs/track-border.png'),0.9)
FINISH = pygame.image.load('imgs/finish.png')


#initalizing window
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("riyas a bitch")

FPS = 60


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