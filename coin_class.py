from constants import *


class Coin:
    def __init__(self, **kwargs):
        self.pos_x = kwargs['pos_x']
        self.pos_y = kwargs['pos_y']
        self.pos_z = COIN_HEIGHT
        self.sprite_ref = COIN_INITIAL_SPRITE
        self.animation_counter = 0
        self.sprite = 1
        self.parent = None

    def work(self):
        # Computes the sprite that will be drawn on the screen by the stage. (Nov 26)
        self.animation_counter += 1
        if self.animation_counter >= COIN_ANIMATION_FRAMES:
            self.animation_counter = 0
            self.sprite += 1
            if self.sprite > len(COIN_SPRITES):
                self.sprite = 1
        self.sprite_ref = COIN_SPRITES_CODE + str(self.sprite)
        # Collision detection with the player will be coded here... (Nov 26)
        if self.parent.is_touching(base_obj=self,
                                   target_obj=self.parent.main_character,
                                   depth_sensitivity=COIN_DEPTH_SENSITIVITY):
            self.parent.gold_resource += 1
            self.parent.coins.remove(self)
