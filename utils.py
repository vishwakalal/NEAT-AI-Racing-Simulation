import pygame


# scaling images
def scale(img, factor):
    size = round(img.get_width() * factor), round(img.get_height() * factor)
    return pygame.transform.scale(img, size)


# rotating image about its center
def rotate_center(win, image, top_left, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=top_left).center)

    win.blit(rotated_image, new_rect.topleft)


CAR = scale(pygame.image.load("imgs/car.png"), 0.07)
GRASS = scale(pygame.image.load("imgs/BLACK.png"), 2.5)
TRACK = scale(pygame.image.load("imgs/track.png"), 0.9)
BORDER = scale(pygame.image.load("imgs/track-border1.png"), 0.9)
BORDER_MASK = pygame.mask.from_surface(BORDER)
FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POS = (130, 250)
CHECKPOINTS = [
    pygame.Rect(152, 125, 30, 30),
    pygame.Rect(100, 58, 30, 30),
    pygame.Rect(43, 165, 30, 30),
    pygame.Rect(43, 280, 30, 30),
    pygame.Rect(43, 445, 30, 30),
    pygame.Rect(103, 523, 30, 30),
    pygame.Rect(160, 585, 30, 30),
    pygame.Rect(234, 653, 30, 30),
    pygame.Rect(322, 712, 30, 30),
    pygame.Rect(387, 689, 30, 30),
    pygame.Rect(394, 560, 30, 30),
    pygame.Rect(490, 468, 30, 30),
    pygame.Rect(575, 510, 30, 30),
    pygame.Rect(581, 585, 30, 30),
    pygame.Rect(580, 659, 30, 30),
    pygame.Rect(655, 707, 30, 30),
    pygame.Rect(730, 485, 30, 30),
    pygame.Rect(715, 380, 30, 30),
    pygame.Rect(575, 342, 30, 30),
    pygame.Rect(395, 300, 30, 30),
    pygame.Rect(575, 235, 30, 30),
    pygame.Rect(712, 160, 30, 30),
    pygame.Rect(575, 52, 30, 30),
    pygame.Rect(300, 75, 30, 30),
    pygame.Rect(255, 185, 30, 30),
    pygame.Rect(215, 386, 30, 30),
    pygame.Rect(152, 290, 30, 30),
    # old rectangles
    # pygame.Rect(140, 120, 75, 40),
    # pygame.Rect(95, 40, 40, 75),
    # pygame.Rect(25, 160, 75, 40),
    # pygame.Rect(25, 275, 75, 40),
    # pygame.Rect(25, 440, 75, 40),
    # pygame.Rect(89, 520, 58, 37),
    # pygame.Rect(140, 580, 75, 40),
    # pygame.Rect(220, 650, 58, 37),
    # pygame.Rect(317, 690, 40, 75),
    # pygame.Rect(382, 680, 40, 48),
    # pygame.Rect(372, 580, 75, 40),
    # pygame.Rect(485, 444, 40, 75),
    # pygame.Rect(560, 580, 75, 40),
    # pygame.Rect(650, 695, 40, 75),
    # pygame.Rect(700, 480, 75, 40),
    # pygame.Rect(570, 330, 40, 75),
    # pygame.Rect(367, 295, 75, 40),
    # pygame.Rect(570, 223, 40, 75),
    # pygame.Rect(700, 155, 75, 40),
    # pygame.Rect(570, 40, 40, 75),
    # pygame.Rect(243, 180, 75, 40),
    # pygame.Rect(210, 374, 40, 75),
    # pygame.Rect(140, 285, 75, 40),
    # old trying to make swaures
    # pygame.Rect(157.5, 120, 35, 35),
    # pygame.Rect(95, 52.5, 40, 40),
    # pygame.Rect(37.5, 160, 40, 40),
    # pygame.Rect(37.5, 275, 40, 40),
    # pygame.Rect(37.5, 440, 40, 40),
    # pygame.Rect(98.5, 518.5, 40, 40),
    # pygame.Rect(140, 580, 75, 40),
    # pygame.Rect(220, 650, 58, 37),
    # pygame.Rect(317, 690, 40, 75),
    # pygame.Rect(382, 680, 40, 48),
    # pygame.Rect(372, 580, 75, 40),
    # pygame.Rect(485, 444, 40, 75),
    # pygame.Rect(560, 580, 75, 40),
    # pygame.Rect(650, 695, 40, 75),
    # pygame.Rect(700, 480, 75, 40),
    # pygame.Rect(570, 330, 40, 75),
    # pygame.Rect(367, 295, 75, 40),
    # pygame.Rect(570, 223, 40, 75),
    # pygame.Rect(700, 155, 75, 40),
    # pygame.Rect(570, 40, 40, 75),
    # pygame.Rect(243, 180, 75, 40),
    # pygame.Rect(210, 374, 40, 75),
    # pygame.Rect(140, 285, 75, 40),
]
