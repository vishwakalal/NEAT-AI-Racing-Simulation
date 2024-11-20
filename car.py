from utils import*
import math

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
    def bounce(self):
        self.vel = -self.vel
        self.move()
    def reset(self):
        self.x, self.y = self.START
        self.angle = 270
        self.vel = 0