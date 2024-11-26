from utils import*
import math
import pygame
class Car:
    IMG = CAR
    START = (160,190)
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 270
        self.x, self.y = self.START
        self.acceleration = 0.1
        self.is_alive = True
        self.radars = []
        self.drawing_radars = []
        self.distance = 0
        self.time = 0
        self.center = [self.x + self.img.get_width() / 2, self.y + self.img.get_height() / 2]

    def rotate(self, left=False, right=False):
        if left:
            self.angle += self.rotation_vel
        if right:
            self.angle -= self.rotation_vel

    def draw_car(self, win):
        rotate_center(win, self.img, (self.x, self.y), self.angle+90)

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
        self.vel = max(self.vel - self.acceleration, - self.max_vel/2)
        self.move()

    def decelerate(self):
        self.vel = max(self.vel - (self.acceleration / 2), 0)
        self.move()
    def collide(self, mask, x = 0, y = 0):
        car_mask = pygame.mask.from_surface(self.img)
        offset = (int(self.x - x),int(self.y - y))
        poi = mask.overlap(car_mask, offset)
        return poi

    def check_collision(self,border_mask, finish_mask, finish_pos):
        self.is_alive = True
        if self.collide(border_mask) is not None:
            self.is_alive = False
            self.bounce()

    def draw_radar(self, screen):
        for radar in self.radars:
            position = radar[0]
            pygame.draw.line(screen, (0, 255, 0), self.center, position, 1)
            pygame.draw.circle(screen, (0, 255, 0), position, 5)


    def check_radar(self, degree, border_mask, finish_mask, finish_pos):
        length = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # While We Don't Hit BORDER_COLOR AND length < 300 (just a max) -> go further and further
        while not self.collide(border_mask) is not None and length < 300:
            length = length + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Calculate Distance To Border And Append To Radars List
        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])

    def update(self,border_mask, finish_mask, finish_pos):
        if self.vel == 0:
            self.vel = self.max_vel/2

        self.x = max(self.x, 20)
        self.x = min(self.x, border_mask.get_size()[0] - 20)
        self.y = max(self.y, 20)
        self.y = min(self.y, border_mask.get_size()[1] - 20)

        self.center = [self.x + self.img.get_width() / 2, self.y + self.img.get_height() / 2]

        self.check_collision(border_mask, finish_mask, finish_pos)

        self.radars.clear()
        for d in range(-90, 120, 45):
            self.check_radar(d, border_mask, finish_mask, finish_pos)

    def get_data(self):
        # Get Distances To Border
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

    def is_alive(self):
        return self.is_alive

    def get_reward(self):
        return self.distance / (self.img.get_width() / 2)

    def bounce(self):
        self.vel = -self.vel
        self.move()


    def reset(self):
        self.x, self.y = self.START
        self.angle = 270
        self.vel = 0
