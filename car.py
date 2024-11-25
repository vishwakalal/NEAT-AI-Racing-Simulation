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
        rotate_center(win, self.img, (self.x, self.y), self.angle + 90)
        self.draw_radars(win)

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

    def get_radars(self, mask):
        mask_width, mask_height = mask.get_size()  # Use get_size() to get dimensions
        distances = []
        radar_points = []

        for angle in [0, -45, 45]:  # Front, Left, Right angles
            radar_angle = math.radians(self.angle + angle)
            for dist in range(1, 150):  # Radar range
                x = int(self.x - math.cos(radar_angle) * dist)
                y = int(self.y - math.sin(radar_angle) * dist)

                # Ensure the radar point is within the mask boundaries
                if 0 <= x < mask_width and 0 <= y < mask_height:
                    if mask.get_at((x, y)):  # Check for collisions
                        radar_points.append((x, y))
                        distances.append(dist)
                        break
            else:
                # If no collision, extend radar to maximum range
                radar_points.append((self.x - math.cos(radar_angle) * 150,
                                     self.y - math.sin(radar_angle) * 150))
                distances.append(150)  # Max range

        self.radar_points = radar_points  # Save points for drawing
        return distances

    def draw_radars(self, win):
        for point in self.radar_points:
            pygame.draw.line(win, (255, 0, 0), (self.x, self.y), point, 1)  # Red lines
            pygame.draw.circle(win, (0, 255, 0), (int(point[0]), int(point[1])), 3)  # Green dots
