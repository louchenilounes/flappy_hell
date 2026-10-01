import pygame as pg
import sys
import os
import pickle
import neat

from bird import Bird
from pipes import PipeHandler
from game_objects import Score, Sound, Background, Ground
from fire import DoomFire
from settings import *


class WatchGame:
    def __init__(self, net):
        pg.init()
        self.screen = pg.display.set_mode(RES)
        pg.display.set_caption('FlappyDoom - IA (best genome)')
        self.clock = pg.time.Clock()
        self.load_assets()
        self.sound = Sound()
        self.score = Score(self)
        self.fire = DoomFire(self)
        self.net = net
        self.new_game()

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

    def new_game(self):
        self.all_sprites_group = pg.sprite.Group()
        self.pipe_group = pg.sprite.Group()
        self.bird = Bird(self, brain=self.net, genome=None)
        self.background = Background(self)
        self.ground = Ground(self)
        self.pipe_handler = PipeHandler(self)

    def draw(self):
        self.background.draw()
        self.fire.draw()
        self.all_sprites_group.draw(self.screen)
        self.ground.draw()
        self.score.draw()
        pg.display.flip()

    def update(self):
        self.background.update()
        self.fire.update()
        self.all_sprites_group.update()
        self.ground.update()
        self.pipe_handler.update()
        self.clock.tick(FPS)

        if not self.bird.alive():
            pg.time.wait(500)
            self.new_game()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


def load_winner_net(config_path, genome_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path
    )
    with open(genome_path, 'rb') as f:
        genome = pickle.load(f)
    return neat.nn.FeedForwardNetwork.create(genome, config)


if __name__ == '__main__':
    local_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(local_dir, 'neat_config.txt')
    genome_path = os.path.join(local_dir, 'best_genome.pkl')

    net = load_winner_net(config_path, genome_path)
    game = WatchGame(net)
    game.run()
