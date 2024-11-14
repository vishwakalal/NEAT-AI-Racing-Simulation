import pygame

#scaling images
def scale(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)

#rotating image about its center
def rotate_center(screen, img, top_left, angle):
    rotated = pygame.transform.rotate(img, angle)
    new_rect = rotated.get_rect(center = img.get_rect(topleft = top_left).center)
    screen.blit(rotated, new_rect.topleft)


CAR = scale(pygame.image.load('imgs/car.png'),0.15)