import pygame as pg
from settings import *
from collections import deque


class Bird(pg.sprite.Sprite):
    def __init__(self, game, brain=None, genome=None):
        super().__init__(game.all_sprites_group)
        self.game = game
        self.image = game.bird_images[0]
        self.mask = pg.mask.from_surface(game.mask_image)
        self.rect = self.image.get_rect()
        self.rect.center = BIRD_POS

        self.images = deque(game.bird_images)
        self.animation_event = pg.USEREVENT + 0
        pg.time.set_timer(self.animation_event, BIRD_ANIMATION_TIME)

        self.falling_velocity = 0
        self.first_jump = False
        self.angle = 0

        # --- mode IA ---
        self.brain = brain          # réseau NEAT (None = mode manuel)
        self.genome = genome        # génome NEAT associé (pour le fitness)
        self.last_passed_pipes = 0  # pour le bonus de fitness par tuyau passé
        if self.brain is not None:
            self.first_jump = True  # l'oiseau IA "vole" dès le départ (pas d'attente de clic)

    def check_collision(self):
        hit = pg.sprite.spritecollide(self, self.game.pipe_group, dokill=False,
                                      collided=pg.sprite.collide_mask)
        out_of_bounds = self.rect.bottom > GROUND_Y or self.rect.top < -self.image.get_height()

        if self.brain is not None:
            # mode IA : on tue seulement cet oiseau, pas de reset global
            if hit or out_of_bounds:
                self.kill()
            return

        # mode manuel : comportement original inchangé
        if hit or out_of_bounds:
            self.game.sound.hit_sound.play()
            pg.time.wait(1000)
            self.game.new_game()

    def rotate(self):
        if self.first_jump:
            if self.falling_velocity < -BIRD_JUMP_VALUE:
                self.angle = BIRD_JUMP_ANGLE
            else:
                self.angle = max(-2.5 * self.falling_velocity, -90)
            self.image = pg.transform.rotate(self.image, self.angle)
            # new mask
            mask_image = pg.transform.rotate(self.game.mask_image, self.angle)
            self.mask = pg.mask.from_surface(mask_image)

    def jump(self):
        if self.brain is None:
            self.game.sound.wing_sound.play()
        self.first_jump = True
        self.falling_velocity = BIRD_JUMP_VALUE

    def use_gravity(self):
        if self.first_jump:
            self.falling_velocity += GRAVITY
            self.rect.y += self.falling_velocity + 0.5 * GRAVITY

    def think(self):
        """Mode IA : calcule les inputs, interroge le réseau, décide de sauter."""
        next_pipe = self.game.pipe_handler.get_next_pipe(self)

        if next_pipe is not None:
            horizontal_dist = next_pipe.rect.left - self.rect.left
            gap_y = next_pipe.gap_y
        else:
            horizontal_dist = WIDTH
            gap_y = HEIGHT / 2

        inputs = (
            self.rect.centery / HEIGHT,
            self.falling_velocity / abs(BIRD_JUMP_VALUE * 3),
            horizontal_dist / WIDTH,
            gap_y / HEIGHT,
        )

        output = self.brain.activate(inputs)
        if output[0] > 0.5:
            self.jump()

    def update(self):
        if self.brain is not None:
            if not self.alive():
                return
            self.think()
            if self.genome is not None:
                self.genome.fitness += 0.1  # récompense de survie par frame

                current_passed = self.game.pipe_handler.passed_pipes
                if current_passed > self.last_passed_pipes:
                    self.genome.fitness += 5 * (current_passed - self.last_passed_pipes)
                    self.last_passed_pipes = current_passed

        self.check_collision()
        self.use_gravity()

    def animate(self):
        self.images.rotate(-1)
        self.image = self.images[0]

    def check_event(self, event):
        if self.brain is not None:
            return  # mode IA : pas de contrôle souris/clavier

        if event.type == self.animation_event:
            self.animate()
            self.rotate()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.jump()