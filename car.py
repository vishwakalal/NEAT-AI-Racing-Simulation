from utils import*
import math

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
        self.acceleration = 0.1

    def rotate(self, left = False, right = False):
        if left:
            self.angle += self.rotation_vel
        elif right:
            self.angle -= self.rotation_vel

    def draw_car(self, screen):
        rotate_center(screen, self.img, (self.x, self.y), self.angle)

    def move(self):
        radians = math.radians(self.angle)
        y_comp = self.vel * math.cos(radians)
        x_comp = self.vel * math.sin(radians)
        self.y -= y_comp
        self.x += x_comp

    def accelerate(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel)
        self.move()
    def backwards(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2)
        self.move()

    def decelerate(self):
        self.vel = max(self.vel - self.acceleration/2, 0)
        self.move()