import pygame as pg
import sys
import os
import pickle
import neat

from bird import Bird
from pipes import PipeHandler
from game_objects import Sound, Background, Ground
from fire import DoomFire
from settings import *


class TrainGame:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        pg.display.set_caption('FlappyDoom - Entrainement NEAT')
        self.clock = pg.time.Clock()
        self.load_assets()
        self.sound = Sound()
        self.fire = DoomFire(self)
        self.stat_font = pg.font.Font('assets/font/doom.ttf', 50)
        self.generation = 0
        self.best_fitness = -1
        self.best_genome_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), 'best_genome.pkl'
        )

    def load_assets(self):
        # identique à FlappyDoom.load_assets (main.py)
        self.bird_images = [pg.image.load(f'assets/bird/{i}.png').convert_alpha() for i in range(5)]
        bird_image = self.bird_images[0]
        bird_size = bird_image.get_width() * BIRD_SCALE, bird_image.get_height() * BIRD_SCALE
        self.bird_images = [pg.transform.scale(sprite, bird_size) for sprite in self.bird_images]

        self.background_image = pg.image.load('assets/images/bg.png').convert()
        self.background_image = pg.transform.scale(self.background_image, RES)

        self.ground_image = pg.image.load('assets/images/ground.png').convert()
        self.ground_image = pg.transform.scale(self.ground_image, (WIDTH, GROUND_HEIGHT))

        self.top_pipe_image = pg.image.load('assets/images/top_pipe.png').convert_alpha()
        self.top_pipe_image = pg.transform.scale(self.top_pipe_image, (PIPE_WIDTH, PIPE_HEIGHT))
        self.bottom_pipe_image = pg.transform.flip(self.top_pipe_image, False, True)

        mask_image = pg.image.load('assets/bird/mask.png').convert_alpha()
        mask_size = mask_image.get_width() * BIRD_SCALE, mask_image.get_height() * BIRD_SCALE
        self.mask_image = pg.transform.scale(mask_image, mask_size)

    def run_generation(self, genomes, config):
        """Callback appelé par neat-python à chaque génération.
        Signature imposée par la librairie : (genomes, config)."""
        self.generation += 1

        self.all_sprites_group = pg.sprite.Group()
        self.pipe_group = pg.sprite.Group()
        self.background = Background(self)
        self.ground = Ground(self)
        self.pipe_handler = PipeHandler(self)

        birds = []
        for genome_id, genome in genomes:
            genome.fitness = 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            bird = Bird(self, brain=net, genome=genome)
            birds.append(bird)

        # référence utilisée par PipeHandler.generate_pipes() (voir note ci-dessus)
        self.bird = birds[0]

        max_frames = FPS * 90  # sécurité : ~90s simulées max par génération
        frame = 0

        while len(birds) > 0 and frame < max_frames:
            frame += 1
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()

            self.background.update()
            self.fire.update()
            self.all_sprites_group.update()
            self.ground.update()
            self.pipe_handler.update()

            birds = [b for b in birds if b.alive()]

            self.draw(len(birds))
            self.clock.tick(0)  # pas de limite : l'entraînement va aussi vite que possible

        print(f'Génération {self.generation} — score (tuyaux passés): {self.pipe_handler.passed_pipes}')

        gen_best_genome = max((g for _, g in genomes), key=lambda g: g.fitness)
        if gen_best_genome.fitness > self.best_fitness:
            self.best_fitness = gen_best_genome.fitness
            with open(self.best_genome_path, 'wb') as f:
                pickle.dump(gen_best_genome, f)
            print(f'  -> nouveau record sauvegardé (fitness={self.best_fitness:.2f}) dans best_genome.pkl')

    def draw(self, alive_count):
        self.background.draw()
        self.fire.draw()
        self.all_sprites_group.draw(self.screen)
        self.ground.draw()
        self.draw_stats(alive_count)
        pg.display.flip()

    def draw_stats(self, alive_count):
        text = self.stat_font.render(
            f'Gen {self.generation}  |  Vivants: {alive_count}  |  Score: {self.pipe_handler.passed_pipes}',
            True, 'white'
        )
        self.screen.blit(text, (20, 20))


def run_neat(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )

    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())

    game = TrainGame()

    N_GENERATIONS = 50
    winner = population.run(game.run_generation, N_GENERATIONS)

    with open(game.best_genome_path, 'wb') as f:
        pickle.dump(winner, f)

    print('\nMeilleur génome :\n', winner)
    print(f'Sauvegardé dans : {game.best_genome_path}')


if __name__ == '__main__':
    local_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(local_dir, 'neat_config.txt')
    run_neat(config_path)