import sys
from utils import *
from car import*
import pygame
import os
import neat
import time
import math

current_gen = 0
    #loading and scaling images
    # GRASS = scale(pygame.image.load('imgs/grass.jpg'), 2.5)
    # TRACK = scale(pygame.image.load('imgs/track.png'), 0.9)
    # BORDER = scale(pygame.image.load('imgs/track-border.png'),0.9)
    # BORDER_MASK = pygame.mask.from_surface(BORDER)
    # FINISH = pygame.image.load('imgs/finish.png')
    # FINISH_MASK = pygame.mask.from_surface(FINISH)
    # FINISH_POS = (130,250)


    #initalizing window
def initialize():
    pygame.init()
    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("racing sim")
    return SCREEN,WIDTH, HEIGHT

FPS = 60

    #draws images onto screen
def draw(screen, images, cars, generation):
    for img, pos in images:
        screen.blit(img, pos)

    for car in cars:
        car.draw_car(screen)

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

    # run = True
    # clock = pygame.time.Clock()
    # images = [(GRASS, (0,0)), (TRACK, (0,0)), (FINISH, FINISH_POS), (BORDER, (0,0))]
    # player = Car(8,3)
    #
    #
    # while run:
    #     clock.tick(FPS)
    #
    #     draw(SCREEN, images, player)
    #     pygame.display.update()
    #     for event in pygame.event.get():
    #         if event.type == pygame.QUIT:
    #             run = False
    #             break
    #
    #     move_car(player)
    #     player.check_collision(BORDER_MASK,FINISH_MASK,FINISH_POS)
    # pygame.quit()

def eval_genomes(genomes, config):
    SCREEN, WIDTH, HEIGHT = initialize()
    images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POS), (BORDER, (0, 0))]
    nets = []
    cars = []

    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        cars.append(Car(8,3))
        genome.fitness = 0

    clock = pygame.time.Clock()
    generation_font = pygame.font.SysFont("Arial", 30)
    alive_font = pygame.font.SysFont("Arial", 20)

    global current_gen
    current_gen += 1

    counter = 0

    while len(cars) > 0 and counter <= 1000:
        clock.tick(FPS)
        counter += 1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        for car in cars:
            car.draw_car(SCREEN)

        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))
            if choice == 0:  # Left
                car.angle += 10
            elif choice == 1:  # Right
                car.angle -= 10
            elif choice == 2:  # Slow Down
                if car.vel - 2 >= 12:
                    car.vel -= 2
            else:  # Speed Up
                car.vel += 2

        still_alive = 0
        for i,car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(BORDER_MASK,FINISH_MASK,FINISH_POS)
                genomes[i][1].fitness += car.get_reward()
        if still_alive == 0:
            break
        counter += 1
        if counter == 30 * 40:
            break

        draw(SCREEN, images, cars, current_gen)
        for car in cars:
            if car.is_alive():
                car.draw(SCREEN)

        text = generation_font.render("Generation: " + str(current_gen), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        SCREEN.blit(text, text_rect)

        text = alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        SCREEN.blit(text, text_rect)

        pygame.display.flip()


if __name__ == "__main__":
        # Load Config
    config_path = "./config.txt"
    config = neat.config.Config(neat.DefaultGenome,
                                    neat.DefaultReproduction,
                                    neat.DefaultSpeciesSet,
                                    neat.DefaultStagnation,
                                    config_path)

        # Create Population And Add Reporters
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

        # Run Simulation For A Maximum of 1000 Generations
    population.run(eval_genomes, 1000)