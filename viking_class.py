from constants import *
from function_library import *
from math import *


class Viking:
    def __init__(self, **kwargs):
        self.pos_x = kwargs['pos_x']
        self.pos_y = kwargs['pos_y']
        self.pos_z = 0
        self.velocity = (0, 0)
        self.is_spawning = kwargs.get('is_spawning', True)
        self.animation_frame_counter = 0
        self.run_sprite = 1
        self.idle_sprite = 1
        self.hurt_sprite = 1
        self.death_sprite = 1
        self.spawn_sprite = 0
        self.attack_sprite = 0
        self.target = None
        self.parent = None
        self.is_in_motion = False
        self.is_attacking = False
        self.is_hurt = False
        self.is_dying = False
        self.is_following_forward = False
        self.is_following_backward = False
        self.direction = kwargs['direction']
        self.sprite_ref = VIKING_INITIAL_SPRITE
        # These variables manage the zolot's health. (Dec 30)
        self.health = kwargs['health']
        self.health_deduct = 0
        self.report_health = (self.health / VIKING_MAX_HEALTH) * 100
        self.bar_clearance = VIKING_BAR_CLEARANCE
        # These variables help with hit detection. (Dec 30)
        self.previous_attackers = {}
        self.is_hazardous = False

    def select_target(self):
        # Selects the nearest enemy as the target if the current target is no longer alive. (Dec 13)
        if self.target not in self.parent.enemies or self.target.is_dying:
            if len(self.parent.enemies) == 0:
                self.target = None
            else:
                nearest_target = None
                nearest_distance = inf
                for x in self.parent.enemies:
                    distance = self.parent.distance_to(base_obj=self, target_obj=x)
                    if distance < nearest_distance and not x.is_dying:
                        nearest_distance = distance
                        nearest_target = x
                self.target = nearest_target

    def move(self):
        if self.is_hurt:
            if magnitude_of(self.velocity) == 0:
                self.is_hurt = False
            else:
                deceleration = scalar_multiplication(-1 * DEFAULT_KNOCKBACK_DAMPENING / magnitude_of(self.velocity), self.velocity)
                self.velocity = vector_addition(self.velocity, deceleration)
                if magnitude_of(self.velocity) < DEFAULT_KNOCKBACK_DAMPENING:
                    self.velocity = (0, 0)
                    self.is_hurt = False
        elif not (self.target is None or self.is_attacking or self.is_dying):
            if self.parent.is_in_attack_position(base_obj=self, target_obj=self.target) or self.is_attacking:
                # Decelerates the viking. (Dec 13)
                if magnitude_of(self.velocity) != 0:
                    if magnitude_of(self.velocity) < VIKING_DECELERATION:
                        self.velocity = (0, 0)
                    else:
                        deceleration = scalar_multiplication(-1 * VIKING_DECELERATION / magnitude_of(self.velocity), self.velocity)
                        self.velocity = vector_addition(self.velocity, deceleration)
                # Makes the viking attack its target. (Dec 17)
                if magnitude_of(self.velocity) <= VIKING_MAX_ATTACK_SPEED and not self.target.is_hurt and not self.target.is_dying:
                    self.is_attacking = True
                    # Ensures smooth transition between the current sprite and the first attack sprite. (Dec 26)
                    self.animation_frame_counter = 0
                    self.attack_sprite = 0
            else:
                # Accelerates the viking towards the selected target. (Dec 13)
                acceleration = scalar_multiplication(VIKING_ACCELERATION, self.parent.unit_vector_to(base_obj=self,
                                                                                                     target_obj=self.target,
                                                                                                     width_adjustment=True))
                self.velocity = vector_addition(self.velocity, acceleration)
                if magnitude_of(self.velocity) > VIKING_MAX_SPEED:
                    self.velocity = scalar_multiplication(VIKING_MAX_SPEED / magnitude_of(self.velocity), self.velocity)
        elif self.target is None and not self.is_dying:
            # Determines whether or not the viking should follow the player. (Jan 15)
            if self.pos_x <= self.parent.main_character.pos_x and self.parent.distance_to(base_obj=self, target_obj=self.parent.main_character) > VIKING_FORWARD_FOLLOW_DISTANCE * VIKING_FOLLOW_SLACK:
                self.is_following_forward = True
                self.is_following_backward = False
            elif self.pos_x > self.parent.main_character.pos_x and self.parent.distance_to(base_obj=self, target_obj=self.parent.main_character) > VIKING_BACKWARD_FOLLOW_DISTANCE * VIKING_FOLLOW_SLACK:
                self.is_following_backward = True
                self.is_following_forward = False
            else:
                if not(self.is_following_forward or self.is_following_backward):
                    self.is_following_forward = False
                    self.is_following_backward = False
            # Accelerates the viking to follow the player if applicable. (Jan 15)
            if self.is_following_forward:
                if self.parent.distance_to(base_obj=self, target_obj=self.parent.main_character) > VIKING_FORWARD_FOLLOW_DISTANCE:
                    acceleration = scalar_multiplication(VIKING_ACCELERATION, self.parent.unit_vector_to(base_obj=self,
                                                                                                         target_obj=self.parent.main_character,
                                                                                                         width_adjustment=True,
                                                                                                         buffer_distance=VIKING_FOLLOW_BUFFER_DISTANCE))
                    self.direction = 1
                    self.velocity = vector_addition(self.velocity, acceleration)
                    if magnitude_of(self.velocity) > VIKING_MAX_SPEED:
                        self.velocity = scalar_multiplication(VIKING_MAX_SPEED / magnitude_of(self.velocity), self.velocity)
                else:
                    self.is_following_forward = False
            elif self.is_following_backward:
                if self.parent.distance_to(base_obj=self, target_obj=self.parent.main_character) > VIKING_BACKWARD_FOLLOW_DISTANCE:
                    acceleration = scalar_multiplication(VIKING_ACCELERATION, self.parent.unit_vector_to(base_obj=self,
                                                                                                         target_obj=self.parent.main_character,
                                                                                                         width_adjustment=True,
                                                                                                         buffer_distance=VIKING_FOLLOW_BUFFER_DISTANCE))
                    self.direction = -1
                    self.velocity = vector_addition(self.velocity, acceleration)
                    if magnitude_of(self.velocity) > VIKING_MAX_SPEED:
                        self.velocity = scalar_multiplication(VIKING_MAX_SPEED / magnitude_of(self.velocity), self.velocity)
                else:
                    self.is_following_backward = False
            else:
                # Decelerates the viking. (Jan 15)
                if magnitude_of(self.velocity) != 0:
                    if magnitude_of(self.velocity) < VIKING_DECELERATION:
                        self.velocity = (0, 0)
                    else:
                        deceleration = scalar_multiplication(-1 * VIKING_DECELERATION / magnitude_of(self.velocity), self.velocity)
                        self.velocity = vector_addition(self.velocity, deceleration)
        else:
            # Decelerates the viking. (Dec 13)
            if magnitude_of(self.velocity) != 0:
                if magnitude_of(self.velocity) < VIKING_DECELERATION:
                    self.velocity = (0, 0)
                else:
                    deceleration = scalar_multiplication(-1 * VIKING_DECELERATION / magnitude_of(self.velocity), self.velocity)
                    self.velocity = vector_addition(self.velocity, deceleration)
        # Ensures that the viking remains within the stage boundaries. (Dec 29)
        if self.pos_x > self.parent.max_limit - VIKING_HORIZONTAL_STOP_DISTANCE:
            self.pos_x = self.parent.max_limit - VIKING_HORIZONTAL_STOP_DISTANCE
            if self.is_hurt and self.velocity[0] > 0:
                # Makes the viking bounce from the boundary wall as a result of knockback. (Dec 29)
                if magnitude_of(self.velocity) >= MIN_BOUNCE_SPEED:
                    self.velocity = (-1 * self.velocity[0], 0)
                    self.direction = 1
                else:
                    self.velocity = (0, 0)
                    self.is_hurt = False
            else:
                self.velocity = (0, self.velocity[1])
        if self.pos_x < self.parent.min_limit + VIKING_HORIZONTAL_STOP_DISTANCE:
            self.pos_x = self.parent.min_limit + VIKING_HORIZONTAL_STOP_DISTANCE
            if self.is_hurt and self.velocity[0] < 0:
                # Makes the viking bounce from the boundary wall as a result of knockback. (Dec 29)
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
        # Applies the viking's velocity to its position. (Dec 29)
        self.pos_x += self.velocity[0]
        self.pos_y += self.velocity[1]

    def compute_sprite(self):
        self.animation_frame_counter += 1
        if self.is_dying:
            if self.animation_frame_counter >= VIKING_DEATH_FRAMES:
                self.animation_frame_counter = 0
                if self.death_sprite < len(VIKING_DEATH_SPRITES):
                    self.death_sprite += 1
                else:
                    # Deletes the viking from memory. (Dec 30)
                    self.parent.troops.remove(self)
            self.sprite_ref = VIKING_DEATH_CODE + str(self.death_sprite * self.direction)
        elif self.is_hurt:
            if self.animation_frame_counter >= VIKING_HURT_FRAMES:
                self.animation_frame_counter = 0
                if self.hurt_sprite < len(VIKING_HURT_SPRITES):
                    self.hurt_sprite += 1
            self.sprite_ref = VIKING_HURT_CODE + str(self.hurt_sprite * self.direction)
        elif self.is_attacking:
            if self.animation_frame_counter >= VIKING_ATTACK_FRAMES:
                self.attack_sprite += 1
                self.animation_frame_counter = 0
                if self.attack_sprite > len(VIKING_ATTACK_SPRITES):
                    self.is_attacking = False
                    self.attack_sprite = 0
                else:
                    self.sprite_ref = VIKING_ATTACK_CODE + str(self.direction * self.attack_sprite)
                    # Adjusts the position of the Viking to accommodate the the composition of the displayed sprite. (Dec 26)
                    self.pos_x += self.direction * VIKING_ATTACK_POSITION_CORRECTION.get(self.attack_sprite)
        elif magnitude_of(self.velocity) == 0:
            if self.is_in_motion:
                self.is_in_motion = False
                self.animation_frame_counter = 0
                self.run_sprite = 1
            if self.animation_frame_counter >= VIKING_IDLE_FRAMES:
                self.animation_frame_counter = 0
                self.idle_sprite += 1
                if self.idle_sprite > len(VIKING_IDLE_SPRITES):
                    self.idle_sprite = 1
            self.sprite_ref = VIKING_IDLE_CODE + str(self.direction * self.idle_sprite)
        else:
            if not self.is_in_motion:
                self.is_in_motion = True
                self.animation_frame_counter = 0
                self.idle_sprite = 1
            if self.animation_frame_counter >= VIKING_RUN_FRAMES:
                self.animation_frame_counter = 0
                self.run_sprite += 1
                if self.run_sprite > len(VIKING_RUN_SPRITES):
                    self.run_sprite = 1
            self.sprite_ref = VIKING_RUN_CODE + str(self.direction * self.run_sprite)

    def compute_direction(self):
        if not (self.target is None or self.is_hurt or self.is_attacking or self.is_dying):
            if self.target.pos_x > self.pos_x:
                self.direction = 1
            else:
                self.direction = -1

    def get_hurt(self):
        if not self.is_dying:
            workplace = self.parent.enemies
            for obj in workplace:
                control, impact_direction = self.parent.is_touching(base_obj=self, target_obj=obj, depth_sensitivity=VIKING_DEPTH_SENSITIVITY, direction_out=True)
                if control and obj.is_hazardous and obj.direction != impact_direction and str(obj) not in self.previous_attackers.keys():
                    # Reduces the viking's health. (Dec 30)
                    damage = DAMAGE_DICT[obj.__class__.__name__]
                    self.health -= damage
                    self.health_deduct += (damage / VIKING_MAX_HEALTH) * 100
                    if self.health > 0:
                        # Initiates the viking's hurt animation. (Dec 30)
                        self.is_hurt = True
                        self.hurt_sprite = 1
                        self.is_attacking = False
                        self.direction = impact_direction
                        self.velocity = (-1 * impact_direction * DEFAULT_KNOCKBACK_SPEED, 0)
                        self.animation_frame_counter = 0
                        self.target = obj
                        self.previous_attackers[str(obj)] = DAMAGE_REGISTER_FRAMES
                    else:
                        # Initiates the viking's death animation. (Dec 30)
                        self.is_dying = True
                        self.direction = impact_direction
                        self.animation_frame_counter = 0
                        self.velocity = (0, 0)
            # Manages the attacker registry. (Dec 30)
            to_delete = []
            for str_obj, registry_frames in self.previous_attackers.items():
                if registry_frames > 0:
                    self.previous_attackers[str_obj] = registry_frames - 1
                else:
                    to_delete.append(str_obj)
            for str_obj in to_delete:
                self.previous_attackers.pop(str_obj)

    def work(self):
        if self.is_spawning:
            # Executes the viking's spawn animation. (Jan 15)
            self.animation_frame_counter += 1
            if self.animation_frame_counter >= VIKING_SPAWN_FRAMES:
                self.animation_frame_counter = 0
                self.spawn_sprite += 1
                if self.spawn_sprite > len(VIKING_SPAWN_SPRITES):
                    self.is_spawning = False
                    self.animation_frame_counter = 0
                else:
                    self.sprite_ref = VIKING_SPAWN_CODE + str(self.spawn_sprite * self.direction)
        if not self.is_spawning:
            self.select_target()
            if not self.parent.is_interim:
                self.move()
                self.get_hurt()
            self.compute_direction()
            self.compute_sprite()
            self.is_hazardous = self.sprite_ref in VIKING_HAZARD_SPRITES
