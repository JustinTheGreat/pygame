from constants import *
import pygame


class BlackOut:
    def __init__(self, **kwargs):
        self.strength = 0
        self.moving_in = True
        self.delay = False
        self.switch = False
        self.moving_out = False
        self.is_done = False
        self.frame_counter = 0
        self.display_surface = kwargs['display_surface']

    def re_init(self):
        self.strength = 0
        self.moving_in = True
        self.switch = False
        self.delay = False
        self.moving_out = False
        self.is_done = False
        self.frame_counter = 0

    def work(self):
        if self.moving_in:
            self.strength += BLACK_OUT_ANIMATION_CONSTANT
            if self.strength >= 1:
                self.strength = 1
                self.moving_in = False
                self.switch = True
                self.delay = True
            pygame.draw.rect(self.display_surface, BLACK_OUT_COLOR, (0, 0, SCREEN_WIDTH, round(self.strength * SCREEN_HEIGHT)))
        if self.delay:
            self.frame_counter += 1
            if self.frame_counter >= BLACK_OUT_DELAY:
                self.delay = False
                self.moving_out = True
            self.display_surface.fill(BLACK_OUT_COLOR)
        if self.moving_out:
            self.strength -= BLACK_OUT_ANIMATION_CONSTANT
            if self.strength <= 0:
                self.strength = 0
                self.moving_out = False
                self.is_done = True
            pygame.draw.rect(self.display_surface, BLACK_OUT_COLOR, (0, 0, self.display_surface.get_rect().size[0], round(self.strength * SCREEN_HEIGHT)))
