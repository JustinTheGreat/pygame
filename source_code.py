# Pygame Project
# Source Code
# Version: 1.0
# Start Date: Nov 18, 2019

from stage_class import Stage
import pygame
from constants import *
import sys
from game_over_screen_class import GameOverScreen
from black_out_class import BlackOut

pygame.mixer.pre_init()
pygame.init()
pygame.display.set_caption(GAME_TITLE)
display_surface = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
FPS_clock = pygame.time.Clock()

# This block loads the assets found in system storage into memory for the stage to access. (Nov 24)
sprites_dict = {}
sprites_rect_dict = {}
# Loads the player assets. (Nov 24)
for k, v in PROTAGONIST_RUN_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * PLAYER_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * PLAYER_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[PROTAGONIST_RUN_CODE + str(k)] = img
    sprites_rect_dict[PROTAGONIST_RUN_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[PROTAGONIST_RUN_CODE + str(-1 * k)] = img
    sprites_rect_dict[PROTAGONIST_RUN_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in PROTAGONIST_IDLE_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * PLAYER_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * PLAYER_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[PROTAGONIST_IDLE_CODE + str(k)] = img
    sprites_rect_dict[PROTAGONIST_IDLE_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[PROTAGONIST_IDLE_CODE + str(-1 * k)] = img
    sprites_rect_dict[PROTAGONIST_IDLE_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in PROTAGONIST_ATTACK_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * PLAYER_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * PLAYER_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[PROTAGONIST_ATTACK_CODE + str(k)] = img
    sprites_rect_dict[PROTAGONIST_ATTACK_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[PROTAGONIST_ATTACK_CODE + str(-1 * k)] = img
    sprites_rect_dict[PROTAGONIST_ATTACK_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in PROTAGONIST_SPELL_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * PLAYER_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * PLAYER_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[PROTAGONIST_SPELL_CODE + str(k)] = img
    sprites_rect_dict[PROTAGONIST_SPELL_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[PROTAGONIST_SPELL_CODE + str(-1 * k)] = img
    sprites_rect_dict[PROTAGONIST_SPELL_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in PROTAGONIST_HURT_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * PLAYER_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * PLAYER_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[PROTAGONIST_HURT_CODE + str(k)] = img
    sprites_rect_dict[PROTAGONIST_HURT_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[PROTAGONIST_HURT_CODE + str(-1 * k)] = img
    sprites_rect_dict[PROTAGONIST_HURT_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in PROTAGONIST_DEATH_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * PLAYER_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * PLAYER_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[PROTAGONIST_DEATH_CODE + str(k)] = img
    sprites_rect_dict[PROTAGONIST_DEATH_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[PROTAGONIST_DEATH_CODE + str(-1 * k)] = img
    sprites_rect_dict[PROTAGONIST_DEATH_CODE + str(-1 * k)] = (rect_x, rect_y)
# Loads the sprites for the Zolot enemies. (Dec 11)
for k, v in ZOLOT_IDLE_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * ZOLOT_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * ZOLOT_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[ZOLOT_IDLE_CODE + str(k)] = img
    sprites_rect_dict[ZOLOT_IDLE_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[ZOLOT_IDLE_CODE + str(-1 * k)] = img
    sprites_rect_dict[ZOLOT_IDLE_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in ZOLOT_RUN_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * ZOLOT_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * ZOLOT_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[ZOLOT_RUN_CODE + str(k)] = img
    sprites_rect_dict[ZOLOT_RUN_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[ZOLOT_RUN_CODE + str(-1 * k)] = img
    sprites_rect_dict[ZOLOT_RUN_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in ZOLOT_HURT_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * ZOLOT_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * ZOLOT_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[ZOLOT_HURT_CODE + str(k)] = img
    sprites_rect_dict[ZOLOT_HURT_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[ZOLOT_HURT_CODE + str(-1 * k)] = img
    sprites_rect_dict[ZOLOT_HURT_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in ZOLOT_ATTACK_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * ZOLOT_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * ZOLOT_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[ZOLOT_ATTACK_CODE + str(k)] = img
    sprites_rect_dict[ZOLOT_ATTACK_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[ZOLOT_ATTACK_CODE + str(-1 * k)] = img
    sprites_rect_dict[ZOLOT_ATTACK_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in ZOLOT_DEATH_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * ZOLOT_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * ZOLOT_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[ZOLOT_DEATH_CODE + str(k)] = img
    sprites_rect_dict[ZOLOT_DEATH_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[ZOLOT_DEATH_CODE + str(-1 * k)] = img
    sprites_rect_dict[ZOLOT_DEATH_CODE + str(-1 * k)] = (rect_x, rect_y)
# Loads the sprites for the Viking troops. (Dec 13)
for k, v in VIKING_RUN_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * VIKING_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * VIKING_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[VIKING_RUN_CODE + str(k)] = img
    sprites_rect_dict[VIKING_RUN_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[VIKING_RUN_CODE + str(-1 * k)] = img
    sprites_rect_dict[VIKING_RUN_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in VIKING_IDLE_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * VIKING_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * VIKING_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[VIKING_IDLE_CODE + str(k)] = img
    sprites_rect_dict[VIKING_IDLE_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[VIKING_IDLE_CODE + str(-1 * k)] = img
    sprites_rect_dict[VIKING_IDLE_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in VIKING_ATTACK_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * VIKING_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * VIKING_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[VIKING_ATTACK_CODE + str(k)] = img
    sprites_rect_dict[VIKING_ATTACK_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[VIKING_ATTACK_CODE + str(-1 * k)] = img
    sprites_rect_dict[VIKING_ATTACK_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in VIKING_HURT_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * VIKING_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * VIKING_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[VIKING_HURT_CODE + str(k)] = img
    sprites_rect_dict[VIKING_HURT_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[VIKING_HURT_CODE + str(-1 * k)] = img
    sprites_rect_dict[VIKING_HURT_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in VIKING_DEATH_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * VIKING_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * VIKING_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[VIKING_DEATH_CODE + str(k)] = img
    sprites_rect_dict[VIKING_DEATH_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[VIKING_DEATH_CODE + str(-1 * k)] = img
    sprites_rect_dict[VIKING_DEATH_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in VIKING_SPAWN_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * VIKING_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * VIKING_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[VIKING_SPAWN_CODE + str(k)] = img
    sprites_rect_dict[VIKING_SPAWN_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[VIKING_SPAWN_CODE + str(-1 * k)] = img
    sprites_rect_dict[VIKING_SPAWN_CODE + str(-1 * k)] = (rect_x, rect_y)
# Loads the Ogre sprites. (Jan 6)
for k, v in OGRE_IDLE_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * OGRE_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * OGRE_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[OGRE_IDLE_CODE + str(k)] = img
    sprites_rect_dict[OGRE_IDLE_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[OGRE_IDLE_CODE + str(-1 * k)] = img
    sprites_rect_dict[OGRE_IDLE_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in OGRE_RUN_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * OGRE_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * OGRE_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[OGRE_RUN_CODE + str(k)] = img
    sprites_rect_dict[OGRE_RUN_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[OGRE_RUN_CODE + str(-1 * k)] = img
    sprites_rect_dict[OGRE_RUN_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in OGRE_HURT_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * OGRE_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * OGRE_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[OGRE_HURT_CODE + str(k)] = img
    sprites_rect_dict[OGRE_HURT_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[OGRE_HURT_CODE + str(-1 * k)] = img
    sprites_rect_dict[OGRE_HURT_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in OGRE_ATTACK_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * OGRE_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * OGRE_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[OGRE_ATTACK_CODE + str(k)] = img
    sprites_rect_dict[OGRE_ATTACK_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[OGRE_ATTACK_CODE + str(-1 * k)] = img
    sprites_rect_dict[OGRE_ATTACK_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in OGRE_DEATH_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * OGRE_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * OGRE_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[OGRE_DEATH_CODE + str(k)] = img
    sprites_rect_dict[OGRE_DEATH_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[OGRE_DEATH_CODE + str(-1 * k)] = img
    sprites_rect_dict[OGRE_DEATH_CODE + str(-1 * k)] = (rect_x, rect_y)
# Loads the coin sprites into memory. (Nov 26)
for k, v in COIN_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * COIN_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * COIN_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[COIN_SPRITES_CODE + str(k)] = img
    sprites_rect_dict[COIN_SPRITES_CODE + str(k)] = (rect_x, rect_y)
# Loads the background images into memory. (Nov 29)
for k, v in BACKGROUND_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * BACKGROUND_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * BACKGROUND_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[BACKGROUND_SPRITE_CODE + str(k)] = img
    sprites_rect_dict[BACKGROUND_SPRITE_CODE + str(k)] = (rect_x, rect_y)
# Loads the fireball sprites into memory. (Jan 10)
for k, v in FIREBALL_AIRBORNE_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * FIREBALL_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * FIREBALL_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[FIREBALL_AIRBORNE_CODE + str(k)] = img
    sprites_rect_dict[FIREBALL_AIRBORNE_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[FIREBALL_AIRBORNE_CODE + str(-1 * k)] = img
    sprites_rect_dict[FIREBALL_AIRBORNE_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in FIREBALL_IMPACT_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * FIREBALL_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * FIREBALL_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[FIREBALL_IMPACT_CODE + str(k)] = img
    sprites_rect_dict[FIREBALL_IMPACT_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[FIREBALL_IMPACT_CODE + str(-1 * k)] = img
    sprites_rect_dict[FIREBALL_IMPACT_CODE + str(-1 * k)] = (rect_x, rect_y)
for k, v in FIREBALL_SPAWN_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * FIREBALL_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * FIREBALL_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[FIREBALL_SPAWN_CODE + str(k)] = img
    sprites_rect_dict[FIREBALL_SPAWN_CODE + str(k)] = (rect_x, rect_y)
    img = pygame.transform.flip(img, True, False)
    sprites_dict[FIREBALL_SPAWN_CODE + str(-1 * k)] = img
    sprites_rect_dict[FIREBALL_SPAWN_CODE + str(-1 * k)] = (rect_x, rect_y)
# Loads the prop sprites. (Nov 29)
for k, v in PROP_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * PROP_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * PROP_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[PROP_SPRITE_CODE + str(k)] = img
    sprites_rect_dict[PROP_SPRITE_CODE + str(k)] = (rect_x, rect_y)
# Loads the HUD sprites. (Dec 1)
img = pygame.image.load(GOLD_COUNTER_ICON)
rect_x = round(img.get_rect().size[0] * COUNTER_HEIGHT / img.get_rect().size[1])
rect_y = COUNTER_HEIGHT
img = pygame.transform.scale(img, (rect_x, rect_y))
sprites_dict[COUNTER_ICONS_CODE + "GOLD"] = img
sprites_rect_dict[COUNTER_ICONS_CODE + "GOLD"] = (rect_x, rect_y)
for k, v in HUD_SPRITES.items():
    img = pygame.image.load(v)
    rect_x = round(img.get_rect().size[0] * HUD_SCALING_FACTOR)
    rect_y = round(img.get_rect().size[1] * HUD_SCALING_FACTOR)
    img = pygame.transform.scale(img, (rect_x, rect_y))
    sprites_dict[HUD_SPRITE_CODE + str(k)] = img
    sprites_rect_dict[HUD_SPRITE_CODE + str(k)] = (rect_x, rect_y)
# Prepares the audible assets. (Jan 15)
pygame.mixer.music.load(BACKGROUND_SONG)
pygame.mixer.music.set_volume(MUSIC_VOLUME)
defeat_sound = pygame.mixer.Sound(DEFEAT_SONG)
victory_sound = pygame.mixer.Sound(VICTORY_SONG)

success_screen = GameOverScreen(display_surface=display_surface, win_condition=True)
failure_screen = GameOverScreen(display_surface=display_surface, win_condition=False)
black_out = BlackOut(display_surface=display_surface)
current_level = 0
stage = Stage.generate_stage(level=current_level,
                             display_surface=display_surface,
                             sprites=sprites_dict,
                             sprites_rect=sprites_rect_dict)

pygame.mixer.music.play(-1)

while True:
    if stage.is_defeat:
        # The player has lost the game. (Jan 19)
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.stop()
            defeat_sound.play()
        failure_screen.work()
    elif stage.is_move_on or stage.is_interim:
        if current_level < len(LEVELS) - 1 or stage.is_interim:
            # The player moves on to the next stage. (Jan 20)
            if black_out.switch:
                # When the black-out is complete, the new stage is put into motion. (Jan 20)
                old_health = stage.main_character.health
                current_level += 1
                stage = Stage.generate_stage(level=current_level,
                                             display_surface=display_surface,
                                             sprites=sprites_dict,
                                             sprites_rect=sprites_rect_dict,
                                             food_resource=stage.food_resource,
                                             gold_resource=stage.gold_resource,
                                             mana_resource=stage.mana_resource,
                                             is_interim=True)
                stage.main_character.health = old_health
            black_out.switch = False
            stage.work()
            black_out.work()
            if black_out.is_done:
                black_out.re_init()
                stage.is_interim = False
        else:
            # The player has won the game. (Jan 19)
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
                victory_sound.play()
            success_screen.work()
    else:
        stage.work()
    pygame.display.update()
    FPS_clock.tick(FPS)
    # Reports the current state of the game. (Jan 20)
    sys.stdout.write('\r' + 500 * ' ')
    sys.stdout.write(f"\rFrame Rate: {round(FPS_clock.get_fps(), 1)}")
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
