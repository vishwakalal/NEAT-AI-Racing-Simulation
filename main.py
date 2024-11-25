from utils import *
from car import*
import pygame
import neat
import os
import time
import math

#loading and scaling images
GRASS = scale(pygame.image.load('imgs/grass.jpg'), 2.5)
TRACK = scale(pygame.image.load('imgs/track.png'), 0.9)
BORDER = scale(pygame.image.load('imgs/track-border.png'),0.9)
BORDER_MASK = pygame.mask.from_surface(BORDER)
FINISH = pygame.image.load('imgs/finish.png')
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POS = (130,250)


#initalizing window
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("riyas a blackie")

FPS = 60

#draws images onto screen
def draw(screen, images, player):
    for img, pos in images:
        screen.blit(img, pos)

    player.draw_car(screen)
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



def eval_genomes(genomes, config):
    run = True
    clock = pygame.time.Clock()
    images = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POS), (BORDER, (0, 0))]
    players = []

    nets = []
    for genome_id, genome in genomes:
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        nets.append(net)
        genome.fitness = 0
        players.append(Car(8, 3))

    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        for i, player in enumerate(players):
            # Get radar distances and points
            radars = player.get_radars(BORDER_MASK)

            # Create the 5 inputs: velocity, angle, and 3 radar distances
            inputs = [
                player.vel,                # Velocity
                player.angle,              # Angle
                radars[0],                 # Front radar distance
                radars[1],                 # Left radar distance
                radars[2],                 # Right radar distance
            ]

            # Feed inputs to the neural network
            output = nets[i].activate(inputs)

            # Control car based on output
            if output[0] > 0.5:  # Accelerate
                player.accelerate()
            if output[1] > 0.5:  # Brake/Move backward
                player.backwards()
            if output[2] > 0.5:  # Turn left
                player.rotate(left=True)
            if output[3] > 0.5:  # Turn right
                player.rotate(right=True)

            # Fitness evaluation
            genomes[i][1].fitness += 1  # Increase fitness for staying alive

            # Penalize collisions
            if player.collide(BORDER_MASK) is not None:
                genomes[i][1].fitness -= 5
                players.pop(i)
                nets.pop(i)
                break

        # Draw everything on the screen
        for player in players:
            draw(SCREEN, images, player)

        pygame.display.update()


def run_neat(config_file):
    config = neat.Config(
        neat.DefaultGenome, neat.DefaultReproduction,
        neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(eval_genomes, 50)  # Run for 50 generations

    print("Best genome:\n", winner)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run_neat(config_path)
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
#
#     if player.collide(BORDER_MASK) != None:
#         player.bounce()
#     finish_poi_collide = player.collide(FINISH_MASK, *FINISH_POS)
#     if finish_poi_collide != None:
#          if finish_poi_collide[1] == 0:
#              player.bounce()
#          else:
#              player.reset()
#              print("finsish")
# pygame.quit()