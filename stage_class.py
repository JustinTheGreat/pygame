import pygame
from constants import *
from protagonist_class import Protagonist
from coin_class import Coin
from zolot_class import Zolot
from ogre_class import Ogre
from prop_class import Prop
from function_library import *


class Stage:
    def __init__(self, **kwargs):
        self.is_interim = kwargs.get('is_interim', False)
        self.main_character = kwargs['main_character']
        self.main_character_draw_x = 0    # The stage does not yet know where to draw the main character. (Nov 27)
        self.min_limit = kwargs['min_limit']
        self.max_limit = kwargs['max_limit']
        self.display_surface = kwargs['display_surface']
        self.camera_pos = kwargs['camera_pos']
        self.top_limit = kwargs['top_limit']
        self.bottom_limit = kwargs['bottom_limit']
        # These variables keep track of the objects within the stage. (Nov 28)
        self.props = kwargs['props']
        self.coins = kwargs['coins']
        self.enemies = kwargs['enemies']
        self.troops = kwargs['troops']
        self.fireballs = kwargs['fireballs']
        # These variables keep track of in-game resources. (Nov 24)
        self.food_resource = kwargs['food_resource']
        self.gold_resource = kwargs['gold_resource']
        self.mana_resource = kwargs['mana_resource']
        self.previous_report_food = self.food_resource
        self.previous_report_mana = self.mana_resource
        self.previous_report_health = self.main_character.health
        # This is the root dictionary from which the stage accesses various sprites. (Nov 24)
        self.sprites_dict = kwargs['sprites']
        self.sprites_rect_dict = kwargs['sprites_rect']
        # Keeps track of whether or not the player has lost or won the game. (Jan 19)
        self.is_defeat = False
        self.is_move_on = False

    def is_touching(self, **kwargs):
        base_obj = kwargs['base_obj']
        target_obj = kwargs['target_obj']
        base_dx = self.sprites_rect_dict[base_obj.sprite_ref][0] // 2
        target_dx = self.sprites_rect_dict[target_obj.sprite_ref][0] // 2
        base_x, base_y = base_obj.pos_x, base_obj.pos_y
        target_x, target_y = target_obj.pos_x, target_obj.pos_y
        depth_sensitivity = kwargs['depth_sensitivity']
        min_collision_depth = kwargs.get('min_collision_depth', DEFAULT_COLLISION_DEPTH)
        direction_out = kwargs.get('direction_out', False)
        if abs(base_x - target_x) >= (base_dx + target_dx - min_collision_depth):
            if direction_out:
                return False, None
            return False
        if abs(base_y - target_y) >= depth_sensitivity:
            if direction_out:
                return False, None
            return False
        if direction_out:
            if base_x < target_x:
                return True, 1
            else:
                return True, -1
        return True

    def is_empty(self, **kwargs):
        pos_x = kwargs['pos_x']
        pos_y = kwargs['pos_y']
        stop_distance = kwargs['stop_distance']
        x_tolerance = kwargs.get('x_tolerance', DEFAULT_EMPTY_X_TOLERANCE)
        y_tolerance = kwargs.get('y_tolerance', DEFAULT_EMPTY_Y_TOLERANCE)
        if pos_x - stop_distance < self.min_limit:
            return False
        if pos_x + stop_distance > self.max_limit:
            return False
        if pos_y > self.bottom_limit or pos_y < self.top_limit:
            return False
        for obj in self.troops + self.enemies:
            if pos_x - x_tolerance <= obj.pos_x <= pos_x + x_tolerance and pos_y - y_tolerance <= obj.pos_y <= pos_y + y_tolerance:
                return False
        return True

    @staticmethod
    def distance_to(**kwargs):
        # Computes the Euclidean distance between the inputted objects' Cartesian coordinates. (Dec 15)
        base_obj = kwargs['base_obj']
        target_obj = kwargs['target_obj']
        return sqrt(pow(base_obj.pos_x - target_obj.pos_x, 2) + pow(base_obj.pos_y - target_obj.pos_y, 2))

    def unit_vector_to(self, **kwargs):
        base_x = kwargs['base_obj'].pos_x
        base_y = kwargs['base_obj'].pos_y
        target_x = kwargs['target_obj'].pos_x
        target_y = kwargs['target_obj'].pos_y
        if kwargs.get('width_adjustment', False):
            # Computes the unit vector pointed to the front of the target object. (Dec 15)
            buffer = kwargs.get('buffer_distance', 0)
            base_dx = self.sprites_rect_dict[kwargs['base_obj'].sprite_ref][0] // 2
            target_dx = self.sprites_rect_dict[kwargs['target_obj'].sprite_ref][0] // 2
            # The algorithm by which the x component of the unit vector is determined may be changed in the future. (Dec 15)
            if base_x > target_x:
                result_x = target_x + (base_dx + target_dx + buffer)
                if result_x >= self.max_limit:
                    result_x = target_x - (base_dx + target_dx + buffer)
            else:
                result_x = target_x - (base_dx + target_dx + buffer)
                if result_x <= self.min_limit:
                    result_x = target_x + (base_dx + target_dx + buffer)
            if base_x == result_x and base_y == target_y:
                return 0, 0
            return scalar_multiplication(1 / sqrt(pow(base_x - result_x, 2) + pow(base_y - target_y, 2)), (result_x - base_x, target_y - base_y))
        else:
            # Computes the unit vector directly aimed to the Cartesian coordinates of the target object. (Dec 15)
            if base_x == target_x and base_y == target_y:
                return 0, 0
            return scalar_multiplication(1 / sqrt(pow(base_x - target_x, 2) + pow(base_y - target_y, 2)), (target_x - base_x, target_y - base_y))

    def is_in_attack_position(self, **kwargs):
        # Determines if the base_obj is positioned to attack target_obj. (Dec 15)
        base_x, base_y = kwargs['base_obj'].pos_x, kwargs['base_obj'].pos_y
        target_x, target_y = kwargs['target_obj'].pos_x, kwargs['target_obj'].pos_y
        max_x_tolerance = kwargs.get('max_x_tolerance', DEFAULT_ATTACK_MAX_X_TOLERANCE)
        min_x_tolerance = kwargs.get('min_x_tolerance', DEFAULT_ATTACK_MIN_X_TOLERANCE)
        y_tolerance = kwargs.get('y_tolerance', DEFAULT_ATTACK_Y_TOLERANCE)
        dx = (self.sprites_rect_dict[kwargs['base_obj'].sprite_ref][0] + self.sprites_rect_dict[kwargs['target_obj'].sprite_ref][0]) // 2
        return min_x_tolerance < abs(base_x - target_x) and abs(base_x - target_x) - dx <= max_x_tolerance and abs(base_y - target_y) <= y_tolerance

    def draw(self, obj):
        # Draws non-player objects on the screen. (Dec 30)
        x = round(obj.pos_x)
        y = round(obj.pos_y)
        z = round(obj.pos_z)
        sprite_ref = obj.sprite_ref
        dx = self.sprites_rect_dict[sprite_ref][0]
        draw_pos = None
        if self.camera_pos > x:
            if (self.camera_pos - x - dx) <= (SCREEN_WIDTH // 2):
                draw_pos = ((SCREEN_WIDTH // 2) - (self.camera_pos - x), y)
        else:
            if (x - dx - self.camera_pos) <= (SCREEN_WIDTH // 2):
                draw_pos = ((SCREEN_WIDTH // 2) + (x - self.camera_pos), y)
        if draw_pos is not None:
            s_dx = round(self.sprites_rect_dict[sprite_ref][0] * SHADOW_SCALING_FACTOR)
            try:
                s_dy = round(obj.shadow_depth * SHADOW_SCALING_FACTOR)
            except AttributeError:
                s_dy = round(DEFAULT_SHADOW_DEPTH * SHADOW_SCALING_FACTOR)
            shadow_surface = pygame.Surface((s_dx, s_dy))
            shadow_surface.fill((0, 0, 0))
            shadow_surface.set_colorkey((0, 0, 0))
            pygame.draw.ellipse(shadow_surface, SHADOW_RGBA, (0, 0, s_dx, s_dy))
            shadow_surface.set_alpha(SHADOW_RGBA[-1])
            self.display_surface.blit(shadow_surface, (draw_pos[0] - s_dx // 2, draw_pos[1] - s_dy // 2))
            self.display_surface.blit(self.sprites_dict[sprite_ref], (draw_pos[0] - self.sprites_rect_dict[sprite_ref][0] // 2,
                                                                      draw_pos[1] - self.sprites_rect_dict[sprite_ref][1] - z))
            # Draws the health bar for the object if applicable. (Dec 30)
            try:
                if not obj.is_dying:
                    if obj.health_deduct > NPC_BAR_ANIMATION_SENSITIVITY:
                        obj.report_health -= obj.health_deduct * NPC_BAR_ANIMATION_CONSTANT
                        obj.health_deduct = obj.health_deduct * (1 - NPC_BAR_ANIMATION_CONSTANT)
                    else:
                        obj.report_health -= obj.health_deduct
                        obj.health_deduct = 0
                    report_length = round((NPC_BAR_LENGTH - 2 * NPC_BAR_EDGE_THICKNESS) * obj.report_health / 100)
                    pygame.draw.rect(self.display_surface, NPC_BAR_EDGE_COLOUR, (draw_pos[0] - NPC_BAR_LENGTH // 2,
                                                                                 draw_pos[1] - NPC_BAR_THICKNESS // 2 - obj.bar_clearance - z,
                                                                                 NPC_BAR_LENGTH,
                                                                                 NPC_BAR_THICKNESS))
                    if report_length >= (NPC_BAR_LENGTH - 2 * NPC_BAR_EDGE_THICKNESS) - NPC_BAR_BUFFER_ZONE:
                        pygame.draw.rect(self.display_surface, NPC_BAR_FILL, (draw_pos[0] - (NPC_BAR_LENGTH // 2 - NPC_BAR_EDGE_THICKNESS),
                                                                              draw_pos[1] - (NPC_BAR_THICKNESS // 2 - NPC_BAR_EDGE_THICKNESS) - obj.bar_clearance - z,
                                                                              NPC_BAR_LENGTH - 2 * NPC_BAR_EDGE_THICKNESS,
                                                                              NPC_BAR_THICKNESS - 2 * NPC_BAR_EDGE_THICKNESS))
                    elif report_length <= NPC_BAR_BUFFER_ZONE:
                        pygame.draw.rect(self.display_surface, NPC_BAR_EMPTY_FILL, (draw_pos[0] - (NPC_BAR_LENGTH // 2 - NPC_BAR_EDGE_THICKNESS),
                                                                                    draw_pos[1] - (NPC_BAR_THICKNESS // 2 - NPC_BAR_EDGE_THICKNESS) - obj.bar_clearance - z,
                                                                                    NPC_BAR_LENGTH - 2 * NPC_BAR_EDGE_THICKNESS,
                                                                                    NPC_BAR_THICKNESS - 2 * NPC_BAR_EDGE_THICKNESS))
                    else:
                        pygame.draw.rect(self.display_surface, NPC_BAR_FILL, (draw_pos[0] - (NPC_BAR_LENGTH // 2 - NPC_BAR_EDGE_THICKNESS),
                                                                              draw_pos[1] - (NPC_BAR_THICKNESS // 2 - NPC_BAR_EDGE_THICKNESS) - obj.bar_clearance - z,
                                                                              report_length,
                                                                              NPC_BAR_THICKNESS - 2 * NPC_BAR_EDGE_THICKNESS))
                        pygame.draw.rect(self.display_surface, NPC_BAR_EMPTY_FILL, (draw_pos[0] - (NPC_BAR_LENGTH // 2 - NPC_BAR_EDGE_THICKNESS) + report_length,
                                                                                    draw_pos[1] - (NPC_BAR_THICKNESS // 2 - NPC_BAR_EDGE_THICKNESS) - obj.bar_clearance - z,
                                                                                    (NPC_BAR_LENGTH - 2 * NPC_BAR_EDGE_THICKNESS) - report_length,
                                                                                    NPC_BAR_THICKNESS - 2 * NPC_BAR_EDGE_THICKNESS))
            except AttributeError:
                pass

    def compute_camera_movement(self):
        # This function computes the position of the camera. (Nov 27)
        x = round(self.main_character.pos_x)
        if self.camera_pos > x:
            if (self.camera_pos - x) <= MIN_SLACK:
                draw_x = (SCREEN_WIDTH // 2) - (self.camera_pos - x)
            elif (x - self.min_limit) <= ((SCREEN_WIDTH // 2) - MIN_SLACK):
                self.camera_pos = self.min_limit + (SCREEN_WIDTH // 2)
                draw_x = (SCREEN_WIDTH // 2) - (self.camera_pos - x)
            else:
                self.camera_pos = x + MIN_SLACK
                draw_x = (SCREEN_WIDTH // 2) - MIN_SLACK
        else:
            if (x - self.camera_pos) <= MAX_SLACK:
                draw_x = (SCREEN_WIDTH // 2) + (x - self.camera_pos)
            elif (self.max_limit - x) <= ((SCREEN_WIDTH // 2) - MAX_SLACK):
                self.camera_pos = self.max_limit - (SCREEN_WIDTH // 2)
                draw_x = (SCREEN_WIDTH // 2) + (x - self.camera_pos)
            else:
                self.camera_pos = x - MAX_SLACK
                draw_x = (SCREEN_WIDTH // 2) + MAX_SLACK
        self.main_character_draw_x = draw_x

    def draw_main_character(self):
        draw_pos = (self.main_character_draw_x, round(self.main_character.pos_y))
        z = self.main_character.pos_z
        sprite_ref = self.main_character.sprite_ref
        # Even newer and better drawing module! The best! (Nov 27)
        s_dx = round(self.sprites_rect_dict[sprite_ref][0] * SHADOW_SCALING_FACTOR)
        s_dy = round(DEFAULT_SHADOW_DEPTH * SHADOW_SCALING_FACTOR)
        shadow_surface = pygame.Surface((s_dx, s_dy))
        shadow_surface.fill((0, 0, 0))
        shadow_surface.set_colorkey((0, 0, 0))
        pygame.draw.ellipse(shadow_surface, SHADOW_RGBA, (0, 0, s_dx, s_dy))
        shadow_surface.set_alpha(SHADOW_RGBA[-1])
        self.display_surface.blit(shadow_surface, (draw_pos[0] - s_dx // 2, draw_pos[1] - s_dy // 2))
        self.display_surface.blit(self.sprites_dict[sprite_ref], (draw_pos[0] - self.sprites_rect_dict[sprite_ref][0] // 2,
                                                                  draw_pos[1] - self.sprites_rect_dict[sprite_ref][1] - z))

    def manage_resources(self):
        if self.mana_resource < MAX_MANA:
            self.mana_resource = min(MAX_MANA, self.mana_resource + MANA_REGENERATION)

    def report_resources(self):
        # Draws the HUD on the screen. (Dec 1)
        self.display_surface.blit(self.sprites_dict[HUD_SPRITE_CODE + 'MAIN'], HUD_POS)
        x = HUD_POS[0] + self.sprites_rect_dict[HUD_SPRITE_CODE + 'MAIN'][0]
        y = HUD_POS[1] + HUD_VERTICAL_ADJUSTMENT
        # Computes the special effects for the health bar. (Dec 2)
        if self.previous_report_health - self.main_character.health > HUD_ANIMATION_SENSITIVITY:
            report_health = floor(self.previous_report_health - (self.previous_report_health - self.main_character.health) * HUD_ANIMATION_CONSTANT)
        else:
            report_health = self.main_character.health
        self.previous_report_health = report_health
        # Draws the health bar. (Dec 1)
        pygame.draw.rect(self.display_surface, BAR_EDGE_COLOR, (x, y, HUD_BAR_LENGTH, HUD_BAR_THICKNESS))
        if report_health <= BAR_BUFFER_ZONE:
            pygame.draw.rect(self.display_surface, EMPTY_BAR_COLOR, (x + BAR_EDGE_HORIZONTAL_THICKNESS, y + BAR_EDGE_VERTICAL_THICKNESS,
                                                                     HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS,
                                                                     HUD_BAR_THICKNESS - 2 * BAR_EDGE_VERTICAL_THICKNESS))
        elif report_health >= PLAYER_MAX_HEALTH - BAR_BUFFER_ZONE:
            pygame.draw.rect(self.display_surface, HEALTH_BAR_COLOR, (x + BAR_EDGE_HORIZONTAL_THICKNESS, y + BAR_EDGE_VERTICAL_THICKNESS,
                                                                      HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS,
                                                                      HUD_BAR_THICKNESS - 2 * BAR_EDGE_VERTICAL_THICKNESS))
        else:
            pygame.draw.rect(self.display_surface, HEALTH_BAR_COLOR, (x + BAR_EDGE_HORIZONTAL_THICKNESS, y + BAR_EDGE_VERTICAL_THICKNESS,
                                                                      floor((HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS) * (report_health / PLAYER_MAX_HEALTH)),
                                                                      HUD_BAR_THICKNESS - 2 * BAR_EDGE_VERTICAL_THICKNESS))
            pygame.draw.rect(self.display_surface, EMPTY_BAR_COLOR, (x + BAR_EDGE_HORIZONTAL_THICKNESS + floor((HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS) * (report_health / PLAYER_MAX_HEALTH)),
                                                                     y + BAR_EDGE_VERTICAL_THICKNESS,
                                                                     ceil((HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS) * (1 - report_health / PLAYER_MAX_HEALTH)),
                                                                     HUD_BAR_THICKNESS - 2 * BAR_EDGE_VERTICAL_THICKNESS))
        # Draws the health bar cap. (Dec 1)
        self.display_surface.blit(self.sprites_dict[HUD_SPRITE_CODE + 'HEALTH'], (x + HUD_BAR_LENGTH, y + HUD_CAP_POS_ADJUSTMENT))
        y += HUD_VERTICAL_SEPARATION
        # Computes the animation for the food bar. (Jan 14)
        if abs(self.previous_report_food - self.food_resource) > HUD_ANIMATION_SENSITIVITY:
            report_food = round(self.previous_report_food - (self.previous_report_food - self.food_resource) * HUD_ANIMATION_CONSTANT)
        else:
            report_food = self.food_resource
        self.previous_report_food = report_food
        # Draws the food bar. (Dec 1)
        pygame.draw.rect(self.display_surface, BAR_EDGE_COLOR, (x, y, HUD_BAR_LENGTH, HUD_BAR_THICKNESS))
        if report_food <= BAR_BUFFER_ZONE:
            pygame.draw.rect(self.display_surface, EMPTY_BAR_COLOR, (x + BAR_EDGE_HORIZONTAL_THICKNESS, y + BAR_EDGE_VERTICAL_THICKNESS,
                                                                     HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS,
                                                                     HUD_BAR_THICKNESS - 2 * BAR_EDGE_VERTICAL_THICKNESS))
        elif report_food >= MAX_FOOD - BAR_BUFFER_ZONE:
            pygame.draw.rect(self.display_surface, FOOD_BAR_COLOR, (x + BAR_EDGE_HORIZONTAL_THICKNESS, y + BAR_EDGE_VERTICAL_THICKNESS,
                                                                    HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS,
                                                                    HUD_BAR_THICKNESS - 2 * BAR_EDGE_VERTICAL_THICKNESS))
        else:
            pygame.draw.rect(self.display_surface, FOOD_BAR_COLOR, (x + BAR_EDGE_HORIZONTAL_THICKNESS, y + BAR_EDGE_VERTICAL_THICKNESS,
                                                                    floor((HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS) * (report_food / MAX_FOOD)),
                                                                    HUD_BAR_THICKNESS - 2 * BAR_EDGE_VERTICAL_THICKNESS))
            pygame.draw.rect(self.display_surface, EMPTY_BAR_COLOR, (x + BAR_EDGE_HORIZONTAL_THICKNESS + floor((HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS) * (report_food / MAX_FOOD)),
                                                                     y + BAR_EDGE_VERTICAL_THICKNESS,
                                                                     ceil((HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS) * (1 - report_food / MAX_FOOD)),
                                                                     HUD_BAR_THICKNESS - 2 * BAR_EDGE_VERTICAL_THICKNESS))
        # Draws the food bar cap. (Dec 1)
        self.display_surface.blit(self.sprites_dict[HUD_SPRITE_CODE + 'FOOD'], (x + HUD_BAR_LENGTH, y + HUD_CAP_POS_ADJUSTMENT))
        y += HUD_VERTICAL_SEPARATION
        # Computes the animation for the mana bar. (Jan 14)
        if self.previous_report_mana - self.mana_resource > HUD_ANIMATION_SENSITIVITY:
            report_mana = floor(self.previous_report_mana - (self.previous_report_mana - self.mana_resource) * HUD_ANIMATION_CONSTANT)
        else:
            report_mana = self.mana_resource
        self.previous_report_mana = report_mana
        # Draws the mana bar. (Dec 1)
        pygame.draw.rect(self.display_surface, BAR_EDGE_COLOR, (x, y, HUD_BAR_LENGTH, HUD_BAR_THICKNESS))
        if report_mana <= BAR_BUFFER_ZONE:
            pygame.draw.rect(self.display_surface, EMPTY_BAR_COLOR, (x + BAR_EDGE_HORIZONTAL_THICKNESS, y + BAR_EDGE_VERTICAL_THICKNESS,
                                                                     HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS,
                                                                     HUD_BAR_THICKNESS - 2 * BAR_EDGE_VERTICAL_THICKNESS))
        elif report_mana >= MAX_MANA - BAR_BUFFER_ZONE:
            pygame.draw.rect(self.display_surface, MANA_BAR_COLOR, (x + BAR_EDGE_HORIZONTAL_THICKNESS, y + BAR_EDGE_VERTICAL_THICKNESS,
                                                                    HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS,
                                                                    HUD_BAR_THICKNESS - 2 * BAR_EDGE_VERTICAL_THICKNESS))
        else:
            pygame.draw.rect(self.display_surface, MANA_BAR_COLOR, (x + BAR_EDGE_HORIZONTAL_THICKNESS, y + BAR_EDGE_VERTICAL_THICKNESS,
                                                                    floor((HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS) * (report_mana / MAX_MANA)),
                                                                    HUD_BAR_THICKNESS - 2 * BAR_EDGE_VERTICAL_THICKNESS))
            pygame.draw.rect(self.display_surface, EMPTY_BAR_COLOR, (x + BAR_EDGE_HORIZONTAL_THICKNESS + floor((HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS) * (report_mana / MAX_MANA)),
                                                                     y + BAR_EDGE_VERTICAL_THICKNESS,
                                                                     ceil((HUD_BAR_LENGTH - 2 * BAR_EDGE_HORIZONTAL_THICKNESS) * (1 - report_mana / MAX_MANA)),
                                                                     HUD_BAR_THICKNESS - 2 * BAR_EDGE_VERTICAL_THICKNESS))
        # Draws mana bar cap. (Dec 1)
        self.display_surface.blit(self.sprites_dict[HUD_SPRITE_CODE + 'MANA'], (x + HUD_BAR_LENGTH, y + HUD_CAP_POS_ADJUSTMENT))
        # Draws the gold counter. (Dec 1)
        draw_x, draw_y = GOLD_COUNTER_POSITION[0] - (len(str(self.gold_resource)) - 1) * GOLD_COUNTER_HORIZONTAL_SHIFT, GOLD_COUNTER_POSITION[1]
        self.display_surface.blit(self.sprites_dict[COUNTER_ICONS_CODE + 'GOLD'], (draw_x, draw_y))
        font_obj = pygame.font.SysFont(COUNTER_FONT_TYPE, COUNTER_TEXT_SIZE)
        self.display_surface.blit(font_obj.render(str(self.gold_resource), True, COUNTER_FONT_COLOUR), (draw_x + self.sprites_rect_dict[COUNTER_ICONS_CODE + 'GOLD'][0] + COUNTER_MARGIN,
                                                                                                        draw_y + (COUNTER_HEIGHT - COUNTER_TEXT_SIZE) // 2))

    def draw_background(self):
        # Draws the bits of the background onto the screen in a way that simulates depth. (Nov 27)
        width = self.sprites_rect_dict[BACKGROUND_SPRITE_CODE + "1"][0]
        dy_list = [0]
        x_list = []
        for i in range(0, len(BACKGROUND_SPRITES)):
            dy_list.append(self.sprites_rect_dict[BACKGROUND_SPRITE_CODE + str(i + 1)][1])
            depth_factor = (1 + BACKGROUND_DEPTH_FACTOR * (len(BACKGROUND_SPRITES) - i - 1))
            x_list.append(round(-1 * ((self.camera_pos - SCREEN_WIDTH // 2) % (width * depth_factor)) / depth_factor))
        repeat = ceil(SCREEN_WIDTH / width) + 1
        for i in range(0, repeat):
            for j in range(0, len(BACKGROUND_SPRITES)):
                self.display_surface.blit(self.sprites_dict[BACKGROUND_SPRITE_CODE + str(j + 1)], (x_list[j] + width * i,
                                                                                                   BACKGROUND_VERTICAL_POS + sum(dy_list[:j + 1])))

    def is_over(self):
        for obj in self.enemies:
            if not obj.is_dead:
                return False
        return len(self.coins) == 0

    @staticmethod
    def generate_stage(**kwargs):
        # Generates the a stage using the level information found in constants.py. (Jan 17)
        level = LEVELS[kwargs['level']]
        protagonist = Protagonist(pos_x=level["SPAWN"][0], pos_y=level["SPAWN"][1], direction=1, health=kwargs.get('health', PLAYER_MAX_HEALTH))
        coins = []
        for data in level['COINS']:
            coins.append(Coin(pos_x=data[0], pos_y=data[1]))
        props = []
        for data in level['PROPS']:
            props.append(Prop(pos_x=data[0], pos_y=data[1], type=data[2]))
        enemies = []
        for data in level['ENEMIES']:
            if data[2] == 1:
                enemies.append(Zolot(pos_x=data[0], pos_y=data[1], direction=1, health=ZOLOT_MAX_HEALTH))
            if data[2] == 2:
                enemies.append(Ogre(pos_x=data[0], pos_y=data[1], direction=1, health=OGRE_MAX_HEALTH))
        result_stage = Stage(main_character=protagonist,
                             min_limit=0,
                             max_limit=level["LENGTH"],
                             top_limit=TOP_LIMIT,
                             bottom_limit=BOTTOM_LIMIT,
                             display_surface=kwargs['display_surface'],
                             props=props,
                             coins=coins,
                             enemies=enemies,
                             troops=kwargs.get('troops', []),
                             fireballs=kwargs.get('fireballs', []),
                             camera_pos=level.get('CAMERA_POS', SCREEN_WIDTH // 2),
                             sprites=kwargs['sprites'],
                             sprites_rect=kwargs['sprites_rect'],
                             food_resource=kwargs.get('food_resource', MAX_FOOD),
                             mana_resource=kwargs.get('mana_resource', MAX_MANA),
                             gold_resource=kwargs.get('gold_resource', 0),
                             is_interim=kwargs.get('is_interim', False))
        # Assigns the generated stage object into the parent attributes of its constituents. (Jan 17)
        for obj in coins:
            obj.parent = result_stage
        for obj in enemies:
            obj.parent = result_stage
        for obj in props:
            obj.parent = result_stage
        protagonist.parent = result_stage
        return result_stage

    def work(self):
        self.manage_resources()
        self.main_character.work()
        self.compute_camera_movement()
        self.is_move_on = self.main_character.pos_x > self.max_limit + BLACK_OUT_TOLERANCE
        # Draws the background according to the position of the camera. (Nov 29)
        self.draw_background()
        # Executes the work function of all the objects within the stage. (Dec 13)
        for obj in self.coins + self.props + self.enemies + self.troops + self.fireballs:
            obj.work()
        # The below code draws the characters such that there is a 2.5D effect. (Nov 27)
        workspace = self.coins + self.props + self.enemies + self.troops + [self.main_character] + self.fireballs
        if len(workspace) > 1:
            control = True
            while control:
                control = False
                for i in range(0, len(workspace) - 1):
                    if workspace[i].pos_y > workspace[i + 1].pos_y:
                        control = True
                        stack = workspace[i]
                        workspace[i] = workspace[i + 1]
                        workspace[i + 1] = stack
        for obj in workspace:
            if type(obj) is Protagonist:
                self.draw_main_character()
            else:
                self.draw(obj)
        # Draws the commodity bars as well as counters on the screen. (Nov 29)
        self.report_resources()
