import sys
from utils import *
from car import *
import pygame
import os
import time
import math

GRASS = scale(pygame.image.load("imgs/BLACK.png"), 2.5)
TRACK = scale(pygame.image.load("imgs/track.png"), 0.9)
BORDER = scale(pygame.image.load("imgs/track-border1.png"), 0.9)
BORDER_MASK = pygame.mask.from_surface(BORDER)
FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POS = (130, 250)


# initalizing window
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("user controlled")

FPS = 60


# draws images onto screen
def draw(screen, images, player):
    for img, pos in images:
        screen.blit(img, pos)

    player.cast_radars(BORDER_MASK)
    player.draw_car(screen)
    player.draw_radars(screen)
    pygame.display.update()


def move_car(player):
    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_a]:
        player.rotate(left=True)
    elif keys[pygame.K_d]:
        player.rotate(right=True)
    elif keys[pygame.K_w]:
        moving = True
        player.accelerate()
    elif keys[pygame.K_s]:
        moving = True
        player.backwards()
    if not moving:
        player.decelerate()


run = True
clock = pygame.time.Clock()
images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POS), (BORDER, (0, 0))]
player = Car(8, 3)


while run:
    clock.tick(FPS)

    draw(SCREEN, images, player)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break

    move_car(player)

    if player.collide(BORDER_MASK) != None:
        player.bounce()
    finish_poi_collide = player.collide(FINISH_MASK, *FINISH_POS)
    if finish_poi_collide != None:
        if finish_poi_collide[1] == 0:
            player.bounce()
        else:
            player.reset()
            print("finish")
pygame.quit()
