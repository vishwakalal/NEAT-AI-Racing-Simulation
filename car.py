import pygame
import math
from utils import *


class Car:
    IMG = CAR
    START = (160, 190)

    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 270
        self.x, self.y = self.START
        self.acceleration = 0.1
        self.radar_angles = [-60, -30, 0, 30, 60]
        self.radar_data = []

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel

    def draw_car(self, win):
        rotate_center(win, self.img, (self.x, self.y), self.angle + 90)

    def move(self):
        radians = math.radians(self.angle)
        y_comp = self.vel * math.sin(radians)
        x_comp = self.vel * math.cos(radians)
        self.y += y_comp
        self.x -= x_comp

    def accelerate(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()

    def backwards(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel / 2)
        self.move()

    def decelerate(self):
        self.vel = max(self.vel - (self.acceleration / 2), 0)
        self.move()

    def collide(self, mask, x=0, y=0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x), int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def bounce(self):
        self.vel = -self.vel
        self.move()

    def reset(self):
        self.x, self.y = self.START
        self.angle = 270
        self.vel = 0

    def cast_radars(self, mask):
        self.radar_data.clear()
        for angles in self.radar_angles:
            length = 0
            x = int(self.x + self.img.get_width() / 2)
            y = int(self.y + self.img.get_height() / 2)

            angle = math.radians((self.angle + 180) + angles)

            while length < 150:
                tempX = int(x + math.cos(angle) * length)
                tempY = int(y - math.sin(angle) * length)
                mask_width, mask_height = mask.get_size()

                if 0 <= tempX < mask_width and 0 <= tempY < mask_height:
                    # hits wall
                    if mask.get_at((tempX, tempY)) == 1:
                        break
                else:
                    break
                length += 1
            self.radar_data.append(length)

    def draw_radars(self, win):
        for i, angles in enumerate(self.radar_angles):
            angle = math.radians((self.angle + 180) + angles)
            origin_x = int(self.x + self.img.get_width() / 2)
            origin_y = int(self.y + self.img.get_height() / 2)
            end_x = int(origin_x + math.cos(angle) * self.radar_data[i])
            end_y = int(origin_y - math.sin(angle) * self.radar_data[i])

            pygame.draw.line(win, (0, 0, 255), (origin_x, origin_y), (end_x, end_y), 2)
            pygame.draw.circle(win, (255, 0, 0), (end_x, end_y), 3)
