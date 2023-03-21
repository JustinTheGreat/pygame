from function_library import *
from constants import *
from math import *


class Zolot:
    def __init__(self, **kwargs):
        self.pos_x = kwargs['pos_x']
        self.pos_y = kwargs['pos_y']
        self.pos_z = 0
        self.velocity = (0, 0)
        self.vertical_speed = 0
        self.animation_frame_counter = 0
        self.idle_sprite = 1
        self.run_sprite = 1
        self.hurt_sprite = 1
        self.death_sprite = 1
        self.attack_sprite = 0
        self.direction = kwargs['direction']
        self.parent = None
        self.target = None
        self.is_spawning = kwargs.get('is_spawning', True)
        self.is_in_motion = False
        self.is_hurt = False
        self.is_attacking = False
        self.is_dying = False
        self.is_dead = False
        self.sprite_ref = ZOLOT_INITIAL_SPRITE
        # These variables manage the zolot's health. (Dec 30)
        self.health = kwargs['health']
        self.health_deduct = 0
        self.report_health = (self.health / ZOLOT_MAX_HEALTH) * 100
        self.bar_clearance = ZOLOT_BAR_CLEARANCE
        # These variables help with hit detection. (Dec 30)
        self.previous_attackers = {}
        self.is_hazardous = False

    def select_target(self):
        if self.target not in self.parent.troops + [self.parent.main_character] or self.target.is_dying:
            if len(self.parent.troops) == 0:
                self.target = self.parent.main_character
            else:
                nearest_target = None
                lowest_distance = inf
                for x in self.parent.troops + [self.parent.main_character]:
                    distance = self.parent.distance_to(base_obj=self, target_obj=x)
                    if distance < lowest_distance and not x.is_dying:
                        lowest_distance = distance
                        nearest_target = x
                self.target = nearest_target

    def move(self):
        # Controls the movement of the Zolot. (Dec 13)
        if self.is_dying:
            if self.pos_z > ZOLOT_DEATH_Z:
                self.vertical_speed += DEFAULT_Z_CORRECTION
                self.pos_z -= self.vertical_speed
            if self.pos_z <= ZOLOT_DEATH_Z:
                self.pos_z = ZOLOT_DEATH_Z
                self.vertical_speed = 0
        elif self.is_hurt:
            if magnitude_of(self.velocity) == 0:
                self.is_hurt = False
            else:
                deceleration = scalar_multiplication(-1 * DEFAULT_KNOCKBACK_DAMPENING / magnitude_of(self.velocity), self.velocity)
                self.velocity = vector_addition(self.velocity, deceleration)
                if magnitude_of(self.velocity) < DEFAULT_KNOCKBACK_DAMPENING:
                    self.velocity = (0, 0)
                    self.is_hurt = False
        else:
            if not (self.target is None or self.is_attacking or self.is_dying):
                if self.parent.is_in_attack_position(base_obj=self, target_obj=self.target, max_x_tolerance=ZOLOT_ATTACK_MAX_X_TOLERANCE):
                    # Decelerates the Zolot. (Dec 13)
                    if magnitude_of(self.velocity) < ZOLOT_DECELERATION:
                        self.velocity = (0, 0)
                    else:
                        self.velocity = vector_addition(self.velocity, scalar_multiplication(-1 * ZOLOT_DECELERATION / magnitude_of(self.velocity), self.velocity))
                    # Makes the zolot attack its target. (Dec 26)
                    if magnitude_of(self.velocity) <= ZOLOT_MAX_ATTACK_SPEED and not self.target.is_hurt and not self.target.is_dying:
                        self.is_attacking = True
                        # Ensures smooth transition between the current sprite and the first attack sprite. (Dec 26)
                        self.animation_frame_counter = 0
                        self.attack_sprite = 0
                else:
                    # Accelerates the Zolot towards the nearest enemy. (Dec 13)
                    unit_vector = self.parent.unit_vector_to(base_obj=self, target_obj=self.target, width_adjustment=True)
                    self.velocity = vector_addition(self.velocity, scalar_multiplication(ZOLOT_ACCELERATION, unit_vector))
                    # Checks if the velocity is over the max speed limit. (Dec 13)
                    if magnitude_of(self.velocity) > ZOLOT_MAX_SPEED:
                        self.velocity = scalar_multiplication(ZOLOT_MAX_SPEED / magnitude_of(self.velocity), self.velocity)
            else:
                # Decelerates the Zolot. (Dec 13)
                if magnitude_of(self.velocity) < ZOLOT_DECELERATION:
                    self.velocity = (0, 0)
                else:
                    self.velocity = vector_addition(self.velocity, scalar_multiplication(-1 * ZOLOT_DECELERATION / magnitude_of(self.velocity), self.velocity))
        # Ensures that the Zolot remains within the stage boundaries. (Dec 29)
        if self.pos_x > self.parent.max_limit - ZOLOT_HORIZONTAL_STOP_DISTANCE:
            self.pos_x = self.parent.max_limit - ZOLOT_HORIZONTAL_STOP_DISTANCE
            if self.is_hurt and self.velocity[0] > 0:
                # Makes the zolot bounce from the boundary wall as a result of knockback. (Dec 29)
                if magnitude_of(self.velocity) >= MIN_BOUNCE_SPEED:
                    self.velocity = (-1 * self.velocity[0], 0)
                    self.direction = 1
                else:
                    self.velocity = (0, 0)
                    self.is_hurt = False
            else:
                self.velocity = (0, self.velocity[1])
        if self.pos_x < self.parent.min_limit + ZOLOT_HORIZONTAL_STOP_DISTANCE:
            self.pos_x = self.parent.min_limit + ZOLOT_HORIZONTAL_STOP_DISTANCE
            if self.is_hurt and self.velocity[0] < 0:
                # Makes the zolot bounce from the boundary wall as a result of knockback. (Dec 29)
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
        # Applies the velocity vector to the zolot's position. (Dec 29)
        self.pos_x += self.velocity[0]
        self.pos_y += self.velocity[1]

    def compute_sprite(self):
        self.animation_frame_counter += 1
        if self.is_dying:
            if self.animation_frame_counter >= ZOLOT_DEATH_FRAMES:
                self.animation_frame_counter = 0
                if self.death_sprite < len(ZOLOT_DEATH_SPRITES):
                    self.death_sprite += 1
                else:
                    self.is_dead = True
            self.sprite_ref = ZOLOT_DEATH_CODE + str(self.death_sprite * self.direction)
        elif self.is_hurt:
            if self.animation_frame_counter >= ZOLOT_HURT_FRAMES:
                self.animation_frame_counter = 0
                if self.hurt_sprite < len(ZOLOT_HURT_SPRITES):
                    self.hurt_sprite += 1
            self.sprite_ref = ZOLOT_HURT_CODE + str(self.hurt_sprite * self.direction)
        elif self.is_attacking:
            if self.animation_frame_counter >= ZOLOT_ATTACK_FRAMES:
                self.attack_sprite += 1
                self.animation_frame_counter = 0
                if self.attack_sprite > len(ZOLOT_ATTACK_SPRITES):
                    self.is_attacking = False
                    self.attack_sprite = 0
                else:
                    self.sprite_ref = ZOLOT_ATTACK_CODE + str(self.direction * self.attack_sprite)
                    # Adjusts the position of the Zolot to accommodate the the composition of the displayed sprite. (Dec 26)
                    self.pos_x += self.direction * ZOLOT_ATTACK_POSITION_CORRECTION.get(self.attack_sprite)
        elif magnitude_of(self.velocity) == 0:
            if self.is_in_motion:
                self.is_in_motion = False
                self.run_sprite = 1
                self.animation_frame_counter = 0
            if self.animation_frame_counter >= ZOLOT_IDLE_FRAMES:
                self.animation_frame_counter = 0
                self.idle_sprite += 1
                if self.idle_sprite > len(ZOLOT_IDLE_SPRITES):
                    self.idle_sprite = 1
            self.sprite_ref = ZOLOT_IDLE_CODE + str(self.idle_sprite * self.direction)
        else:
            if not self.is_in_motion:
                self.is_in_motion = True
                self.idle_sprite = 1
                self.animation_frame_counter = 0
            self.idle_sprite = 1
            if self.animation_frame_counter >= ZOLOT_RUN_FRAMES:
                self.animation_frame_counter = 0
                self.run_sprite += 1
                if self.run_sprite > len(ZOLOT_RUN_SPRITES):
                    self.run_sprite = 1
            self.sprite_ref = ZOLOT_RUN_CODE + str(self.run_sprite * self.direction)

    def compute_direction(self):
        if not (self.target is None or self.is_hurt or self.is_attacking or self.is_dying):
            if self.target.pos_x > self.pos_x:
                self.direction = 1
            else:
                self.direction = -1

    def get_hurt(self):
        if not self.is_dying:
            workplace = self.parent.troops + [self.parent.main_character] + self.parent.fireballs
            for obj in workplace:
                control, impact_direction = self.parent.is_touching(base_obj=self, target_obj=obj, depth_sensitivity=ZOLOT_DEPTH_SENSITIVITY, direction_out=True)
                if control and obj.is_hazardous and obj.direction != impact_direction and str(obj) not in self.previous_attackers.keys():
                    # Reduces the zolot's health. (Dec 30)
                    damage = DAMAGE_DICT[obj.__class__.__name__]
                    self.health -= damage
                    self.is_attacking = False
                    self.health_deduct += damage / ZOLOT_MAX_HEALTH * 100
                    if self.health > 0:
                        # Initiates the zolot's hurt animation. (Dec 30)
                        self.is_hurt = True
                        self.hurt_sprite = 1
                        self.direction = impact_direction
                        self.velocity = (-1 * impact_direction * DEFAULT_KNOCKBACK_SPEED, 0)
                        self.animation_frame_counter = 0
                        self.target = obj
                        self.previous_attackers[str(obj)] = DAMAGE_REGISTER_FRAMES
                    else:
                        # Initiates the zolot's death animation. (Dec 30)
                        self.is_dying = True
                        self.animation_frame_counter = 0
                        self.velocity = (0, 0)
                        # Increases the amount of food resource available to the player. (Jan 17)
                        self.parent.food_resource += ZOLOT_FOOD_GAIN
                        if self.parent.food_resource > MAX_FOOD:
                            self.parent.food_resource = MAX_FOOD
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
            # This will be changed later to spawn the enemy. (Dec 13)
            self.is_spawning = False
        if not self.is_spawning:
            self.select_target()
            if not self.parent.is_interim:
                self.move()
                self.get_hurt()
            self.compute_direction()
            self.compute_sprite()
            self.is_hazardous = self.sprite_ref in ZOLOT_HAZARD_SPRITES
