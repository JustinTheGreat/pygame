from function_library import *
from constants import *


class Fireball:
    def __init__(self, **kwargs):
        self.pos_x = kwargs['pos_x']
        self.pos_y = kwargs['pos_y']
        self.pos_z = kwargs['pos_z']
        self.direction = kwargs['direction']
        self.is_moving = True
        self.is_spawning = True
        self.x_vel = FIREBALL_INITIAL_SPEED * self.direction
        self.parent = None
        # These variables keep track of the fireball's current sprite. (Jan 10)
        self.animation_frame_counter = 0
        self.spawn_sprite = 1
        self.move_sprite = 1
        self.impact_sprite = 1
        self.sprite_ref = FIREBALL_INITIAL_SPRITE
        # Makes sure that the fireball can deal damage to enemies. (Jan 13)
        self.is_hazardous = True

    def check_obstacles(self):
        # Checks if the fireball has hit an obstacle. (Jan 10)
        if self.is_moving:
            if self.pos_x + FIREBALL_STOP_DISTANCE > self.parent.max_limit:
                self.pos_x = self.parent.max_limit - FIREBALL_STOP_DISTANCE
                self.is_moving = False
                self.animation_frame_counter = 0
            if self.pos_x - FIREBALL_STOP_DISTANCE < self.parent.min_limit:
                self.pos_x = self.parent.min_limit + FIREBALL_STOP_DISTANCE
                self.is_moving = False
                self.animation_frame_counter = 0
            for obj in self.parent.enemies:
                if self.parent.is_touching(base_obj=self, target_obj=obj, depth_sensitivity=FIREBALL_DEPTH_SENSITIVITY) and not obj.is_dead:
                    self.is_moving = False
                    self.animation_frame_counter = 0

    def move(self):
        # Makes the fireball move. (Jan 10)
        if self.is_moving:
            if abs(self.x_vel) < FIREBALL_MAX_SPEED:
                self.x_vel += FIREBALL_ACCELERATION * self.direction
                if abs(self.x_vel) > FIREBALL_MAX_SPEED:
                    self.x_vel = sign_of(self.x_vel) * FIREBALL_MAX_SPEED
            self.pos_x += self.x_vel

    def compute_sprite(self):
        self.animation_frame_counter += 1
        if self.is_moving:
            if self.is_spawning:
                if self.animation_frame_counter >= FIREBALL_SPAWN_FRAMES:
                    self.animation_frame_counter = 0
                    self.spawn_sprite += 1
                    if self.spawn_sprite > len(FIREBALL_SPAWN_SPRITES):
                        self.is_spawning = False
                    else:
                        self.sprite_ref = FIREBALL_SPAWN_CODE + str(self.spawn_sprite * self.direction)
                        self.pos_z += FIREBALL_Z_CORRECTION
            else:
                if self.animation_frame_counter >= FIREBALL_MOVE_FRAMES:
                    self.animation_frame_counter = 0
                    self.move_sprite += 1
                    if self.move_sprite > len(FIREBALL_AIRBORNE_SPRITES):
                        self.move_sprite = 1
                self.sprite_ref = FIREBALL_AIRBORNE_CODE + str(self.move_sprite * self.direction)
        else:
            if self.animation_frame_counter >= FIREBALL_IMPLODE_FRAMES:
                self.animation_frame_counter = 0
                if self.impact_sprite < len(FIREBALL_IMPACT_SPRITES):
                    self.impact_sprite += 1
                else:
                    # Removes the fireball from the stage. (Jan 10)
                    self.parent.fireballs.remove(self)
            self.sprite_ref = FIREBALL_IMPACT_CODE + str(self.impact_sprite * self.direction)

    def work(self):
        self.check_obstacles()
        self.compute_sprite()
        self.move()
