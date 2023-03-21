import pygame
from constants import *
from function_library import *
from viking_class import Viking
from fireball_class import Fireball


class Protagonist:
    def __init__(self, **kwargs):
        self.pos_x = kwargs['pos_x']
        self.pos_y = kwargs['pos_y']
        self.pos_z = 0
        self.parent = None
        self.health = kwargs['health']
        # The player's speed is zero at first. (Nov 20)
        self.velocity = (0, 0)
        self.vertical_speed = 0
        # This variable prohibits the player from simply holding down various buttons. (Jan 10)
        self.attack_key_released = True
        self.spell_key_released = True
        self.spawn_key_released = True
        # These variables keep track of the main character's current sprite. (Nov 23)
        self.animation_frame_counter = 0
        self.run_sprite = 1
        self.idle_sprite = 1
        self.death_sprite = 1
        self.slash_attack_sprite = 0
        self.spell_attack_sprite = 0
        self.hurt_sprite = 1
        self.direction = kwargs['direction']
        self.is_in_motion = False
        self.is_attacking = False
        self.is_casting_spell = False
        self.is_hurt = False
        self.is_dying = False
        self.sprite_ref = PLAYER_INITIAL_SPRITE
        self.spell_frame_counter = 0
        # These variables help with hit detection. (Dec 30)
        self.previous_attackers = {}
        self.is_hazardous = False

    def move(self):
        control = False
        keys = pygame.key.get_pressed()
        if (keys[GO_RIGHT] or keys[GO_LEFT] or keys[GO_UP] or keys[GO_DOWN]) and not (self.is_attacking or self.is_casting_spell or self.is_hurt or self.is_dying):
            acceleration_direction = (0, 0)
            if keys[GO_RIGHT]:
                self.direction = 1
                control = True
                acceleration_direction = vector_addition(acceleration_direction, RIGHT)
            if keys[GO_LEFT]:
                if not control:
                    self.direction = -1
                acceleration_direction = vector_addition(acceleration_direction, LEFT)
            if keys[GO_UP]:
                acceleration_direction = vector_addition(acceleration_direction, UP)
            if keys[GO_DOWN]:
                acceleration_direction = vector_addition(acceleration_direction, DOWN)
            # Minor change to address the error caused when opposite keys are pressed at the same time. (Nov 22)
            if magnitude_of(acceleration_direction) == 0:
                acceleration = (0, 0)
            else:
                acceleration = scalar_multiplication(PLAYER_ACCELERATION / magnitude_of(acceleration_direction),
                                                     acceleration_direction)
            self.velocity = vector_addition(self.velocity, acceleration)
            if magnitude_of(self.velocity) > PLAYER_MAX_SPEED:
                self.velocity = scalar_multiplication(PLAYER_MAX_SPEED / magnitude_of(self.velocity), self.velocity)
        # Handles the knockback effect that occurs when the player is hit. (Dec 28)
        if self.is_hurt:
            if magnitude_of(self.velocity) == 0:
                deceleration = (0, 0)
            elif self.pos_z == 0:
                deceleration = scalar_multiplication(-1 * DEFAULT_KNOCKBACK_DAMPENING / magnitude_of(self.velocity), self.velocity)
            else:
                deceleration = scalar_multiplication(-1 * DEFAULT_AIR_KNOCKBACK_DAMPENING / magnitude_of(self.velocity), self.velocity)
            self.velocity = vector_addition(self.velocity, deceleration)
            if magnitude_of(self.velocity) < DEFAULT_KNOCKBACK_DAMPENING:
                self.velocity = (0, 0)
                self.is_hurt = False
        # Adjusts the player's height. (Jan 7)
        if self.is_dying:
            if self.pos_z > PROTAGONIST_DEATH_Z:
                self.vertical_speed += DEFAULT_Z_CORRECTION
                self.pos_z -= self.vertical_speed
            if self.pos_z <= PROTAGONIST_DEATH_Z:
                self.pos_z = PROTAGONIST_DEATH_Z
                self.vertical_speed = 0
        elif not self.is_casting_spell:
            if self.pos_z > 0:
                self.vertical_speed += DEFAULT_Z_CORRECTION
                self.pos_z -= self.vertical_speed
            if self.pos_z <= 0:
                self.pos_z = 0
                self.vertical_speed = 0
        # Slight change made to handle the friction in both components separately. (Nov 22)
        if not (self.is_casting_spell or self.is_hurt or self.is_dying):
            new_vel_x = self.velocity[0]
            new_vel_y = self.velocity[1]
            if not(logical_xor(keys[GO_RIGHT], keys[GO_LEFT])) or self.is_attacking:
                new_vel_x -= sign_of(new_vel_x) * PLAYER_DECELERATION
                if abs(new_vel_x) < PLAYER_DECELERATION:
                    new_vel_x = 0
            if not(logical_xor(keys[GO_UP], keys[GO_DOWN])) or self.is_attacking:
                new_vel_y -= sign_of(new_vel_y) * PLAYER_DECELERATION
                if abs(new_vel_y) < PLAYER_DECELERATION:
                    new_vel_y = 0
            self.velocity = (new_vel_x, new_vel_y)
        # Change the position of the player. (Nov 20)
        self.pos_x += self.velocity[0]
        self.pos_y += self.velocity[1]
        # Test for touching sides of the screen. (Nov 20)
        if not self.is_dying:
            if not self.parent.is_over():
                if self.pos_x > self.parent.max_limit - PLAYER_HORIZONTAL_STOP_DISTANCE:
                    self.pos_x = self.parent.max_limit - PLAYER_HORIZONTAL_STOP_DISTANCE
                    if self.is_hurt and self.velocity[0] > 0:
                        # Makes the player bounce from the boundary wall as a result of knockback. (Dec 28)
                        if magnitude_of(self.velocity) >= MIN_BOUNCE_SPEED:
                            self.velocity = (-1 * self.velocity[0], 0)
                            self.direction = 1
                        else:
                            self.velocity = (0, 0)
                            self.is_hurt = False
                    else:
                        self.velocity = (0, self.velocity[1])
            if self.pos_x < self.parent.min_limit + PLAYER_HORIZONTAL_STOP_DISTANCE:
                self.pos_x = self.parent.min_limit + PLAYER_HORIZONTAL_STOP_DISTANCE
                if self.is_hurt and self.velocity[0] < 0:
                    # Makes the player bounce from the boundary wall as a result of knockback. (Dec 28)
                    if magnitude_of(self.velocity) >= MIN_BOUNCE_SPEED:
                        self.velocity = (-1 * self.velocity[0], 0)
                        self.direction = -1
                    else:
                        self.velocity = (0, 0)
                        self.is_hurt = False
                else:
                    self.velocity = (0, self.velocity[1])
            if self.pos_y > self.parent.bottom_limit:
                self.pos_y = self.parent.bottom_limit
                self.velocity = (self.velocity[0], 0)
            if self.pos_y < self.parent.top_limit:
                self.pos_y = self.parent.top_limit
                self.velocity = (self.velocity[0], 0)

    def compute_sprite(self):
        self.animation_frame_counter += 1
        if self.is_dying:
            if self.animation_frame_counter >= PROTAGONIST_DEATH_FRAMES:
                self.animation_frame_counter = 0
                if self.death_sprite < len(PROTAGONIST_DEATH_SPRITES):
                    self.death_sprite += 1
                # Terminates the player's death animation. (Jan 7)
                if self.death_sprite == len(PROTAGONIST_DEATH_SPRITES) and self.pos_z == PROTAGONIST_DEATH_Z:
                    self.velocity = (0, 0)
                    # Triggers the game over screen. (Jan 7)
                    self.parent.is_defeat = True
                self.sprite_ref = PROTAGONIST_DEATH_CODE + str(self.death_sprite * self.direction)
        elif self.is_hurt:
            if self.animation_frame_counter >= PROTAGONIST_HURT_FRAMES:
                self.animation_frame_counter = 0
                if self.hurt_sprite < len(PROTAGONIST_HURT_SPRITES):
                    self.hurt_sprite += 1
            self.sprite_ref = PROTAGONIST_HURT_CODE + str(self.hurt_sprite * self.direction)
        elif self.is_casting_spell:
            # Handles the spell casting animation for the character. (Dec 5)
            self.spell_frame_counter += 1
            if self.animation_frame_counter >= PROTAGONIST_SPELL_ATTACK_FRAMES:
                self.animation_frame_counter = 0
                self.spell_attack_sprite += 1
                if self.spell_attack_sprite > len(PROTAGONIST_SPELL_SPRITES):
                    # Resetting the frame counter once the attack has concluded. (Dec 5)
                    self.animation_frame_counter = 0
                    self.is_casting_spell = False
                    self.spell_attack_sprite = 0
                    # Ensures that the player lands properly. (Dec 5)
                    self.spell_frame_counter = 0
                else:
                    # Spawns a fireball object into the stage. (Jan 13)
                    if self.spell_attack_sprite == PROTAGONIST_SPELL_EXECUTE_SPRITE and self.parent.mana_resource >= FIREBALL_COST:
                        fireball = Fireball(pos_x=self.pos_x + PROTAGONIST_SPELL_EXECUTE_X * self.direction,
                                            pos_y=self.pos_y + PROTAGONIST_SPELL_EXECUTE_Y,
                                            pos_z=self.pos_z + PROTAGONIST_SPELL_EXECUTE_Z,
                                            direction=self.direction)
                        fireball.parent = self.parent
                        self.parent.fireballs.append(fireball)
                        # Reduces the mana resource available to the player. (Jan 13)
                        self.parent.mana_resource -= FIREBALL_COST
                    self.sprite_ref = PROTAGONIST_SPELL_CODE + str(self.spell_attack_sprite * self.direction)
        elif self.is_attacking:
            # Handles the attacking animations for the character. (Nov 28)
            if self.animation_frame_counter >= PROTAGONIST_SLASH_ATTACK_FRAMES:
                self.animation_frame_counter = 0
                self.slash_attack_sprite += 1
                if self.slash_attack_sprite > len(PROTAGONIST_ATTACK_SPRITES):
                    # Resetting the frame counter once the attack has concluded. (Nov 28)
                    self.animation_frame_counter = 0
                    self.is_attacking = False
                    self.slash_attack_sprite = 0
                    # Makes sure that there isn't any leftover velocity from the player's momentum. (Nov 28)
                    self.velocity = (0, 0)
                else:
                    self.sprite_ref = PROTAGONIST_ATTACK_CODE + str(self.slash_attack_sprite * self.direction)
        elif magnitude_of(self.velocity) != 0:
            # Handles the running animations for the character. (Nov 28)
            # Resetting the frame counter if the state of motion is changed. (Nov 22)
            if not self.is_in_motion:
                self.idle_sprite = 1
                self.animation_frame_counter = 0
                self.is_in_motion = True
            # Determines if the current frame displayed for the main character needs to be updated. (Nov 22)
            if self.animation_frame_counter >= PROTAGONIST_RUN_FRAMES:
                self.animation_frame_counter = 0
                self.run_sprite += 1
                if self.run_sprite > len(PROTAGONIST_RUN_SPRITES):
                    self.run_sprite = 1
            # Stores the sprite reference for the object's current sprite. (Nov 24)
            self.sprite_ref = PROTAGONIST_RUN_CODE + str(self.run_sprite * self.direction)
        else:
            # Handles the idle animations for the character. (Nov 28)
            # Resetting the frame counter if the state of motion is changed. (Nov 22)
            if self.is_in_motion:
                self.run_sprite = 1
                self.animation_frame_counter = 0
                self.is_in_motion = False
            # Determines if the current frame displayed for the main character needs to be updated. (Nov 22)
            if self.animation_frame_counter >= PROTAGONIST_IDLE_FRAMES:
                self.animation_frame_counter = 0
                self.idle_sprite += 1
                if self.idle_sprite > len(PROTAGONIST_IDLE_SPRITES):
                    self.idle_sprite = 1
            # Stores the sprite reference for the object's current sprite. (Nov 24)
            self.sprite_ref = PROTAGONIST_IDLE_CODE + str(self.idle_sprite * self.direction)

    def slash_attack(self):
        keys = pygame.key.get_pressed()
        if keys[SLASH_ATTACK]:
            if self.attack_key_released and (not self.is_attacking) and (not self.is_casting_spell):
                self.is_attacking = True
                self.animation_frame_counter = 0
                self.slash_attack_sprite = 0
            self.attack_key_released = False
        else:
            self.attack_key_released = True

    def spell_attack(self):
        keys = pygame.key.get_pressed()
        if keys[SPELL_ATTACK]:
            if self.spell_key_released and (not self.is_attacking) and (not self.is_casting_spell) and (magnitude_of(self.velocity) >= PLAYER_MIN_SPELL_SPEED):
                self.is_casting_spell = True
                self.spell_frame_counter = 0
                self.spell_attack_sprite = 0
                self.animation_frame_counter = 0
            self.spell_key_released = False
        else:
            self.spell_key_released = True
        # Computes the vertical position of the player. (Dec 9)
        if self.is_casting_spell:
            x_range = len(PROTAGONIST_SPELL_SPRITES) * PROTAGONIST_SPELL_ATTACK_FRAMES
            value = -1 * (x_range / 2) + self.spell_frame_counter
            self.pos_z = PLAYER_SPELL_A / (abs(pow(value, PLAYER_SPELL_N)) + PLAYER_SPELL_B) + PLAYER_SPELL_C

    def get_hurt(self):
        if not self.is_dying:
            workplace = self.parent.enemies
            for obj in workplace:
                control, impact_direction = self.parent.is_touching(base_obj=self, target_obj=obj, depth_sensitivity=PLAYER_DEPTH_SENSITIVITY, direction_out=True)
                if control and obj.is_hazardous and obj.direction != impact_direction and str(obj) not in self.previous_attackers.keys():
                    self.health -= DAMAGE_DICT[obj.__class__.__name__]
                    self.is_attacking = False
                    self.is_casting_spell = False
                    if self.health > 0:
                        # Initiates the player's hurt animation. (Jan 6)
                        self.is_hurt = True
                        self.hurt_sprite = 1
                        self.direction = impact_direction
                        self.velocity = (-1 * impact_direction * DEFAULT_KNOCKBACK_SPEED, 0)
                        self.animation_frame_counter = 0
                        self.previous_attackers[str(obj)] = DAMAGE_REGISTER_FRAMES
                    else:
                        # Initiates the player's dying animation. (Jan 6)
                        self.direction = impact_direction
                        self.velocity = (-1 * self.direction * PLAYER_DEATH_KNOCKBACK, 0)
                        self.animation_frame_counter = 0
                        self.is_dying = True
            # Manages the attacker registry. (Dec 30)
            to_delete = []
            for str_obj, registry_frames in self.previous_attackers.items():
                if registry_frames > 0:
                    self.previous_attackers[str_obj] = registry_frames - 1
                else:
                    to_delete.append(str_obj)
            for str_obj in to_delete:
                self.previous_attackers.pop(str_obj)

    def spawn_viking(self):
        keys = pygame.key.get_pressed()
        if keys[SPAWN_TROOP]:
            if self.spawn_key_released and self.parent.food_resource >= VIKING_SPAWN_COST:
                spawn_pos = None
                if self.parent.is_empty(pos_x=self.pos_x, pos_y=self.pos_y + Y_SPAWN_DISTANCE, stop_distance=VIKING_HORIZONTAL_STOP_DISTANCE):
                    spawn_pos = (self.pos_x, self.pos_y + Y_SPAWN_DISTANCE)
                elif self.parent.is_empty(pos_x=self.pos_x + X_SPAWN_DISTANCE * self.direction, pos_y=self.pos_y, stop_distance=VIKING_HORIZONTAL_STOP_DISTANCE):
                    spawn_pos = (self.pos_x + X_SPAWN_DISTANCE * self.direction, self.pos_y)
                elif self.parent.is_empty(pos_x=self.pos_x - X_SPAWN_DISTANCE * self.direction, pos_y=self.pos_y, stop_distance=VIKING_HORIZONTAL_STOP_DISTANCE):
                    spawn_pos = (self.pos_x - X_SPAWN_DISTANCE * self.direction, self.pos_y)
                elif self.parent.is_empty(pos_x=self.pos_x, pos_y=self.pos_y - Y_SPAWN_DISTANCE, stop_distance=VIKING_HORIZONTAL_STOP_DISTANCE):
                    spawn_pos = (self.pos_x, self.pos_y - Y_SPAWN_DISTANCE)
                if spawn_pos is not None:
                    # Reduces the food resource available to the player. (Jan 10)
                    self.parent.food_resource -= VIKING_SPAWN_COST
                    # Spawns the viking into the stage. (Jan 10)
                    viking = Viking(pos_x=spawn_pos[0], pos_y=spawn_pos[1], direction=self.direction, health=VIKING_MAX_HEALTH)
                    viking.parent = self.parent
                    self.parent.troops.append(viking)
            self.spawn_key_released = False
        else:
            self.spawn_key_released = True

    def work(self):
        if not (self.parent.is_interim or self.parent.is_move_on):
            self.move()
            self.get_hurt()
            self.slash_attack()
            self.spell_attack()
            self.spawn_viking()
        self.compute_sprite()
        self.is_hazardous = self.sprite_ref in PROTAGONIST_HAZARD_SPRITES
