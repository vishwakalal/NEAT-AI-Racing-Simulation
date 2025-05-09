import neat
import pygame
import os
import time
from car import *
from utils import *

WIDTH = TRACK.get_width()
HEIGHT = TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("ai sim")
pygame.font.init()
FONT = pygame.font.SysFont("arial", 20)


def draw(win, images, car, generation, fitness):
    for img, pos in images:
        win.blit(img, pos)
    car.draw_car(win)
    pygame.display.update()


def draw_text(win, text, pos, color=(255, 255, 255)):
    label = FONT.render(text, True, color)
    win.blit(label, pos)


def eval_genomes(genomes, config, generation):
    cars = []
    nets = []
    ge_map = []

    for genome_id, genome in genomes:
        genome.fitness = 0
        net = neat.nn.FeedForwardNetwork.create(genome, config)
        car = Car(3, 6)
        cars.append(car)
        nets.append(net)
        ge_map.append(genome)

    clock = pygame.time.Clock()
    images = [
        (GRASS, (0, 0)),
        (TRACK, (0, 0)),
        (FINISH, FINISH_POS),
        (BORDER, (0, 0)),
    ]
    run = True
    max_frames = 500
    frame = 0

    counter = []
    for _ in cars:
        counter.append(0)
    finish_flag = []
    for _ in cars:
        finish_flag.append(False)
    car_checkpoint_index = []
    for _ in cars:
        car_checkpoint_index.append(0)
    checkpoint_timers = []
    for _ in cars:
        checkpoint_timers.append(0)

    while run and frame < max_frames and len(cars) > 0:
        clock.tick(60)
        frame += 0.5
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        WIN.fill((0, 0, 0))
        for img, pos in images:
            WIN.blit(img, pos)

        # for checkpoint in CHECKPOINTS:
        #     pygame.draw.rect(WIN, (0, 0, 255), checkpoint, 2)

        for i in reversed(range(len(cars))):
            car = cars[i]
            checkpoint_timers[i] += 1
            car.cast_radars(BORDER_MASK)
            inputs = [dist / 150 for dist in car.radar_data]
            output = nets[i].activate(inputs)

            if output[0] > 0.5:
                car.rotate(left=True)
            if output[1] > 0.5:
                car.rotate(right=True)
            if output[2] > 0.5:
                car.accelerate()
                counter[i] = 0
            else:
                car.decelerate()
                counter[i] += 1

            car.move()
            car.draw_car(WIN)

            ge_map[i].fitness += 0.2
            avg_radar = sum(car.radar_data) / len(car.radar_data)
            ge_map[i].fitness += (avg_radar / 150) * 0.3

            if car_checkpoint_index[i] < len(CHECKPOINTS):
                checkpoint_rect = CHECKPOINTS[car_checkpoint_index[i]]
                car_rect = pygame.Rect(
                    car.x, car.y, car.IMG.get_width(), car.IMG.get_height()
                )
                if car_rect.colliderect(checkpoint_rect):
                    ge_map[i].fitness += 50 + (15 * car_checkpoint_index[i])
                    car_checkpoint_index[i] += 1
                    checkpoint_timers[i] = 0

            finish_poi = car.collide(FINISH_MASK, *FINISH_POS)
            if not finish_flag[i] and finish_poi:
                if finish_poi[1] == 0:
                    del cars[i]
                    del nets[i]
                    del ge_map[i]
                    del counter[i]
                    del finish_flag[i]
                    continue
                else:
                    ge_map[i].fitness += 250
                    finish_flag[i] = True
            if checkpoint_timers[i] > 150:
                del cars[i]
                del nets[i]
                del ge_map[i]
                del counter[i]
                del finish_flag[i]
                del car_checkpoint_index[i]
                del checkpoint_timers[i]
                continue
            if car.collide(BORDER_MASK) or counter[i] > 100:
                del cars[i]
                del nets[i]
                del ge_map[i]
                del counter[i]
                del finish_flag[i]

        draw_text(WIN, f"Generation: {generation}", (10, HEIGHT - 50))
        draw_text(WIN, f"Cars remaining: {len(cars)}", (10, HEIGHT - 25))
        pygame.display.update()


def run(config_path):
    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)

    winner = population.run(
        lambda genomes, config: eval_genomes(genomes, config, population.generation), 50
    )


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
