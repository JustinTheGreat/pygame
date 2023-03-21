import pygame
from constants import *


class GameOverScreen:
    def __init__(self, **kwargs):
        self.display_surface = kwargs['display_surface']
        if kwargs['win_condition']:
            # Draws the winning screen. (Dec 29)
            surface = pygame.Surface((GAME_OVER_SCREEN_WIDTH, GAME_OVER_SCREEN_HEIGHT))
            surface.fill(GAME_OVER_SCREEN_BORDER_COLOR)
            pygame.draw.rect(surface, GAME_OVER_SCREEN_SUCCESSFUL_FILL_COLOR, (GAME_OVER_SCREEN_BORDER_WIDTH, GAME_OVER_SCREEN_BORDER_WIDTH,
                                                                               GAME_OVER_SCREEN_WIDTH - 2 * GAME_OVER_SCREEN_BORDER_WIDTH,
                                                                               GAME_OVER_SCREEN_HEIGHT - 2 * GAME_OVER_SCREEN_BORDER_WIDTH))
            text = pygame.font.Font.render(pygame.font.SysFont(GAME_OVER_SCREEN_FONT_TYPE, GAME_OVER_SCREEN_FONT_SIZE),
                                           GAME_OVER_SUCCESSFUL_MESSAGE, True, GAME_OVER_SCREEN_FONT_COLOR, GAME_OVER_SCREEN_SUCCESSFUL_FILL_COLOR)
            text_pos = ((GAME_OVER_SCREEN_WIDTH - text.get_rect().size[0]) // 2,
                        (GAME_OVER_SCREEN_HEIGHT - text.get_rect().size[1]) // 2)
            surface.blit(text, text_pos)
            self.content = surface
        else:
            # Draws the losing screen. (Dec 29)
            surface = pygame.Surface((GAME_OVER_SCREEN_WIDTH, GAME_OVER_SCREEN_HEIGHT))
            surface.fill(GAME_OVER_SCREEN_BORDER_COLOR)
            pygame.draw.rect(surface, GAME_OVER_SCREEN_UNSUCCESSFUL_FILL_COLOR, (GAME_OVER_SCREEN_BORDER_WIDTH, GAME_OVER_SCREEN_BORDER_WIDTH,
                                                                                 GAME_OVER_SCREEN_WIDTH - 2 * GAME_OVER_SCREEN_BORDER_WIDTH,
                                                                                 GAME_OVER_SCREEN_HEIGHT - 2 * GAME_OVER_SCREEN_BORDER_WIDTH))
            text = pygame.font.Font.render(pygame.font.SysFont(GAME_OVER_SCREEN_FONT_TYPE, GAME_OVER_SCREEN_FONT_SIZE),
                                           GAME_OVER_UNSUCCESSFUL_MESSAGE, True, GAME_OVER_SCREEN_FONT_COLOR, GAME_OVER_SCREEN_UNSUCCESSFUL_FILL_COLOR)
            text_pos = ((GAME_OVER_SCREEN_WIDTH - text.get_rect().size[0]) // 2,
                        (GAME_OVER_SCREEN_HEIGHT - text.get_rect().size[1]) // 2)
            surface.blit(text, text_pos)
            self.content = surface
        self.animation_frame_counter = GAME_OVER_SCREEN_ANIMATION_FRAMES
        self.size = GAME_OVER_SCREEN_DISPLAY_MIN_SIZE

    def work(self):
        if self.size <= 1:
            self.animation_frame_counter += 1
            if self.animation_frame_counter >= GAME_OVER_SCREEN_ANIMATION_FRAMES:
                self.animation_frame_counter = 0
                img = pygame.transform.scale(self.content, (round(GAME_OVER_SCREEN_WIDTH * self.size),
                                                            round(GAME_OVER_SCREEN_HEIGHT * self.size)))
                img_pos = ((SCREEN_WIDTH - img.get_rect().size[0]) // 2,
                           (SCREEN_HEIGHT - img.get_rect().size[1]) // 2)
                self.display_surface.blit(img, img_pos)
                self.size += GAME_OVER_SCREEN_DISPLAY_SIZE_INC
