from function_library import *
from constants import *
from math import *


class Ogre:
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
        self.sprite_ref = OGRE_INITIAL_SPRITE
        self.health = kwargs['health']
        self.health_deduct = 0
        self.report_health = (self.health / OGRE_MAX_HEALTH) * 100
        self.bar_clearance = OGRE_BAR_CLEARANCE
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
        if self.is_dying:
            if self.pos_z > OGRE_DEATH_Z:
                self.vertical_speed += DEFAULT_Z_CORRECTION
                self.pos_z -= self.vertical_speed
            if self.pos_z <= OGRE_DEATH_Z:
                self.pos_z = OGRE_DEATH_Z
                self.vertical_speed = 0
        elif self.is_hurt:
            if magnitude_of(self.velocity) == 0:
                self.is_hurt = False
            else:
                deceleration = scalar_multiplication(-1 * OGRE_KNOCKBACK_DAMPENING / magnitude_of(self.velocity), self.velocity)
                self.velocity = vector_addition(self.velocity, deceleration)
                if magnitude_of(self.velocity) < OGRE_KNOCKBACK_DAMPENING:
                    self.velocity = (0, 0)
                    self.is_hurt = False
        else:
            if not (self.target is None or self.is_attacking or self.is_dying):
                if self.parent.is_in_attack_position(base_obj=self, target_obj=self.target, max_x_tolerance=OGRE_ATTACK_MAX_X_TOLERANCE):
                    if magnitude_of(self.velocity) < OGRE_DECELERATION:
                        self.velocity = (0, 0)
                    else:
                        self.velocity = vector_addition(self.velocity, scalar_multiplication(-1 * OGRE_DECELERATION / magnitude_of(self.velocity), self.velocity))
                    # Makes the ogre attack its target. (Jan 6)
                    if magnitude_of(self.velocity) <= OGRE_MAX_ATTACK_SPEED and not self.target.is_hurt and not self.target.is_dying:
                        self.is_attacking = True
                        # Ensures smooth transition between the current sprite and the first attack sprite. (Jan 6)
                        self.animation_frame_counter = 0
                        self.attack_sprite = 0
                else:
                    # Accelerates the Ogre towards the nearest enemy. (Jan 6)
                    unit_vector = self.parent.unit_vector_to(base_obj=self, target_obj=self.target, width_adjustment=True)
                    self.velocity = vector_addition(self.velocity, scalar_multiplication(OGRE_ACCELERATION, unit_vector))
                    # Checks if the velocity is over the max speed limit. (Jan 6)
                    if magnitude_of(self.velocity) > OGRE_MAX_SPEED:
                        self.velocity = scalar_multiplication(OGRE_MAX_SPEED / magnitude_of(self.velocity), self.velocity)
            else:
                # Decelerates the Ogre. (Jan 6)
                if magnitude_of(self.velocity) < OGRE_DECELERATION:
                    self.velocity = (0, 0)
                else:
                    self.velocity = vector_addition(self.velocity, scalar_multiplication(-1 * OGRE_DECELERATION / magnitude_of(self.velocity), self.velocity))
        # Ensures that the Ogre remains within the stage boundaries. (Jan 6)
        if self.pos_x > self.parent.max_limit - OGRE_HORIZONTAL_STOP_DISTANCE:
            self.pos_x = self.parent.max_limit - OGRE_HORIZONTAL_STOP_DISTANCE
            if self.is_hurt and self.velocity[0] > 0:
                # Makes the ogre bounce from the boundary wall as a result of knockback. (Jan 6)
                if magnitude_of(self.velocity) >= MIN_BOUNCE_SPEED:
                    self.velocity = (-1 * self.velocity[0], 0)
                    self.direction = 1
                else:
                    self.velocity = (0, 0)
                    self.is_hurt = False
            else:
                self.velocity = (0, self.velocity[1])
        if self.pos_x < self.parent.min_limit + OGRE_HORIZONTAL_STOP_DISTANCE:
            self.pos_x = self.parent.min_limit + OGRE_HORIZONTAL_STOP_DISTANCE
            if self.is_hurt and self.velocity[0] < 0:
                # Makes the ogre bounce from the boundary wall as a result of knockback. (Jan 6)
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
        # Applies the velocity vector to the ogre's position. (Jan 6)
        self.pos_x += self.velocity[0]
        self.pos_y += self.velocity[1]

    def compute_sprite(self):
        self.animation_frame_counter += 1
        if self.is_dying:
            if self.animation_frame_counter >= OGRE_DEATH_FRAMES:
                self.animation_frame_counter = 0
                if self.death_sprite < len(OGRE_DEATH_SPRITES):
                    self.death_sprite += 1
                else:
                    self.is_dead = True
            self.sprite_ref = OGRE_DEATH_CODE + str(self.death_sprite * self.direction)
        elif self.is_hurt:
            if self.animation_frame_counter >= OGRE_HURT_FRAMES:
                self.animation_frame_counter = 0
                if self.hurt_sprite < len(OGRE_HURT_SPRITES):
                    self.hurt_sprite += 1
            self.sprite_ref = OGRE_HURT_CODE + str(self.hurt_sprite * self.direction)
        elif self.is_attacking:
            if self.animation_frame_counter >= OGRE_ATTACK_FRAMES:
                self.attack_sprite += 1
                self.animation_frame_counter = 0
                if self.attack_sprite > len(OGRE_ATTACK_SPRITES):
                    self.is_attacking = False
                    self.attack_sprite = 0
                else:
                    self.sprite_ref = OGRE_ATTACK_CODE + str(self.direction * self.attack_sprite)
                    self.pos_x += self.direction * OGRE_ATTACK_POSITION_CORRECTION.get(self.attack_sprite)
        elif magnitude_of(self.velocity) == 0:
            if self.is_in_motion:
                self.is_in_motion = False
                self.run_sprite = 1
                self.animation_frame_counter = 0
            if self.animation_frame_counter >= OGRE_IDLE_FRAMES:
                self.animation_frame_counter = 0
                self.idle_sprite += 1
                if self.idle_sprite > len(OGRE_IDLE_SPRITES):
                    self.idle_sprite = 1
            self.sprite_ref = OGRE_IDLE_CODE + str(self.idle_sprite * self.direction)
        else:
            if not self.is_in_motion:
                self.is_in_motion = True
                self.idle_sprite = 1
                self.animation_frame_counter = 0
            self.idle_sprite = 1
            if self.animation_frame_counter >= OGRE_RUN_FRAMES:
                self.animation_frame_counter = 0
                self.run_sprite += 1
                if self.run_sprite > len(OGRE_RUN_SPRITES):
                    self.run_sprite = 1
            self.sprite_ref = OGRE_RUN_CODE + str(self.run_sprite * self.direction)

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
                control, impact_direction = self.parent.is_touching(base_obj=self, target_obj=obj, depth_sensitivity=OGRE_DEPTH_SENSITIVITY, direction_out=True)
                if control and obj.is_hazardous and obj.direction != impact_direction and str(obj) not in self.previous_attackers.keys():
                    # Reduces the ogre's health. (Jan 6)
                    damage = DAMAGE_DICT[obj.__class__.__name__]
                    self.health -= damage
                    self.is_attacking = False
                    self.health_deduct += damage / OGRE_MAX_HEALTH * 100
                    if self.health > 0:
                        # Initiates the ogre's hurt animation. (Jan 6)
                        self.is_hurt = True
                        self.hurt_sprite = 1
                        self.direction = impact_direction
                        self.velocity = (-1 * impact_direction * OGRE_KNOCKBACK_SPEED, 0)
                        self.animation_frame_counter = 0
                        self.target = obj
                        self.previous_attackers[str(obj)] = DAMAGE_REGISTER_FRAMES
                    else:
                        # Initiates the ogre's death animation. (Jan 6)
                        self.is_dying = True
                        self.animation_frame_counter = 0
                        self.velocity = (0, 0)
                        # Increases the amount of food resource available to the player. (Jan 17)
                        self.parent.food_resource += OGRE_FOOD_GAIN
                        if self.parent.food_resource > MAX_FOOD:
                            self.parent.food_resource = MAX_FOOD
            # Manages the attacker registry. (Jan 6)
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
            # This will be changed later to spawn the enemy. (Jan 6)
            self.is_spawning = False
        if not self.is_spawning:
            self.select_target()
            if not self.parent.is_interim:
                self.move()
                self.get_hurt()
            self.compute_direction()
            self.compute_sprite()
            self.is_hazardous = self.sprite_ref in OGRE_HAZARD_SPRITES
