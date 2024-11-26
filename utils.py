import pygame

#scaling images
def scale(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

#rotating image about its center
def rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)

    win.blit(rotated_image, new_rect.topleft)

CAR = scale(pygame.image.load('imgs/car.png'),0.12)
GRASS = scale(pygame.image.load('imgs/grass.jpg'), 2.5)
TRACK = scale(pygame.image.load('imgs/track.png'), 0.9)
BORDER = scale(pygame.image.load('imgs/track-border.png'),0.9)
BORDER_MASK = pygame.mask.from_surface(BORDER)
FINISH = pygame.image.load('imgs/finish.png')
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POS = (130,250)