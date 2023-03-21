from pygame.locals import *

# Video Constants (Updated: Jan 20)
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 333
FPS = 20
GAME_TITLE = "The Best Game of All Time!"
MAX_SLACK = 150
MIN_SLACK = 150

# Player Speed Constants (Updated: Dec 9)
PLAYER_MAX_SPEED = 6.5
PLAYER_ACCELERATION = 0.8
PLAYER_DECELERATION = 1.2
PLAYER_MIN_SPELL_SPEED = 3.0
PLAYER_SPELL_N = 3
PLAYER_SPELL_A = 750
PLAYER_SPELL_B = 30
PLAYER_SPELL_C = -3.5
PLAYER_DEATH_KNOCKBACK = 5.5

# Viking Speed Constants (Created: Jan 17)
VIKING_MAX_SPEED = 3
VIKING_ACCELERATION = 0.8
VIKING_DECELERATION = 1.2
VIKING_MAX_ATTACK_SPEED = 2

# Zolot Speed Constants (Created: Jan 17)
ZOLOT_MAX_SPEED = 3
ZOLOT_ACCELERATION = 0.8
ZOLOT_DECELERATION = 1.2
ZOLOT_MAX_ATTACK_SPEED = 2

# Fireball Speed Constants (Created: Jan 17)
FIREBALL_MAX_SPEED = 7.5
FIREBALL_INITIAL_SPEED = 3.5
FIREBALL_ACCELERATION = 0.8

# Ogre Speed Constants (Created: Jan 17)
OGRE_MAX_SPEED = 1.5
OGRE_ACCELERATION = 0.3
OGRE_DECELERATION = 1.6
OGRE_MAX_ATTACK_SPEED = 1

# Sound Constants (Created: Jan 15)
BACKGROUND_SONG = "Music\\Game Main Music.mp3"
VICTORY_SONG = "Music\\Victory Music.wav"
DEFEAT_SONG = "Music\\Defeat Sound Effect.wav"
MUSIC_VOLUME = 0.7

# Direction Constants (Created: Nov 20)
RIGHT = (1, 0)
LEFT = (-1, 0)
UP = (0, -1)
DOWN = (0, 1)

# Key Mapping Constants (Updated: Jan 12)
GO_RIGHT = K_RIGHT
GO_LEFT = K_LEFT
GO_UP = K_UP
GO_DOWN = K_DOWN
SLASH_ATTACK = K_a
SPELL_ATTACK = K_s
SPAWN_TROOP = K_x

# These constants outline the directories at which the sprites for the main character are stored. (Nov 24)
PROTAGONIST_RUN_SPRITES = {1: "Sprites\\Main Character\\Run\\Run (1).png",
                           2: "Sprites\\Main Character\\Run\\Run (2).png",
                           3: "Sprites\\Main Character\\Run\\Run (3).png",
                           4: "Sprites\\Main Character\\Run\\Run (4).png",
                           5: "Sprites\\Main Character\\Run\\Run (5).png",
                           6: "Sprites\\Main Character\\Run\\Run (6).png",
                           7: "Sprites\\Main Character\\Run\\Run (7).png",
                           8: "Sprites\\Main Character\\Run\\Run (8).png",
                           9: "Sprites\\Main Character\\Run\\Run (9).png",
                           10: "Sprites\\Main Character\\Run\\Run (10).png"}

PROTAGONIST_IDLE_SPRITES = {1: "Sprites\\Main Character\\Idle\\Idle (1).png",
                            2: "Sprites\\Main Character\\Idle\\Idle (2).png",
                            3: "Sprites\\Main Character\\Idle\\Idle (3).png",
                            4: "Sprites\\Main Character\\Idle\\Idle (4).png",
                            5: "Sprites\\Main Character\\Idle\\Idle (5).png",
                            6: "Sprites\\Main Character\\Idle\\Idle (6).png",
                            7: "Sprites\\Main Character\\Idle\\Idle (7).png",
                            8: "Sprites\\Main Character\\Idle\\Idle (8).png",
                            9: "Sprites\\Main Character\\Idle\\Idle (9).png",
                            10: "Sprites\\Main Character\\Idle\\Idle (10).png"}

PROTAGONIST_ATTACK_SPRITES = {1: "Sprites\\Main Character\\Attack\\Attack (1).png",
                              2: "Sprites\\Main Character\\Attack\\Attack (2).png",
                              3: "Sprites\\Main Character\\Attack\\Attack (3).png",
                              4: "Sprites\\Main Character\\Attack\\Attack (4).png",
                              5: "Sprites\\Main Character\\Attack\\Attack (5).png",
                              6: "Sprites\\Main Character\\Attack\\Attack (6).png",
                              7: "Sprites\\Main Character\\Attack\\Attack (7).png",
                              8: "Sprites\\Main Character\\Attack\\Attack (8).png",
                              9: "Sprites\\Main Character\\Attack\\Attack (9).png",
                              10: "Sprites\\Main Character\\Attack\\Attack (10).png", }

PROTAGONIST_SPELL_SPRITES = {1: "Sprites\\Main Character\\Jump Attack\\JumpAttack (1).png",
                             2: "Sprites\\Main Character\\Jump Attack\\JumpAttack (2).png",
                             3: "Sprites\\Main Character\\Jump Attack\\JumpAttack (3).png",
                             4: "Sprites\\Main Character\\Jump Attack\\JumpAttack (4).png",
                             5: "Sprites\\Main Character\\Jump Attack\\JumpAttack (5).png",
                             6: "Sprites\\Main Character\\Jump Attack\\JumpAttack (6).png",
                             7: "Sprites\\Main Character\\Jump Attack\\JumpAttack (7).png",
                             8: "Sprites\\Main Character\\Jump Attack\\JumpAttack (8).png",
                             9: "Sprites\\Main Character\\Jump Attack\\JumpAttack (9).png",
                             10: "Sprites\\Main Character\\Jump Attack\\JumpAttack (10).png"}

PROTAGONIST_HURT_SPRITES = {1: "Sprites\\Main Character\\Hurt\\Hurt (1).png",
                            2: "Sprites\\Main Character\\Hurt\\Hurt (2).png"}

PROTAGONIST_DEATH_SPRITES = {1: "Sprites\\Main Character\\Dead\\Dead (1).png",
                             2: "Sprites\\Main Character\\Dead\\Dead (2).png",
                             3: "Sprites\\Main Character\\Dead\\Dead (3).png",
                             4: "Sprites\\Main Character\\Dead\\Dead (4).png",
                             5: "Sprites\\Main Character\\Dead\\Dead (5).png",
                             6: "Sprites\\Main Character\\Dead\\Dead (6).png",
                             7: "Sprites\\Main Character\\Dead\\Dead (7).png",
                             8: "Sprites\\Main Character\\Dead\\Dead (8).png"}

# These constants outline the directories at which the sprites for Zolot enemies are stored. (Dec 11)
ZOLOT_IDLE_SPRITES = {1: "Sprites\\Enemies\\Zolot\\Idle\\Zolot Idle 1.png",
                      2: "Sprites\\Enemies\\Zolot\\Idle\\Zolot Idle 2.png",
                      3: "Sprites\\Enemies\\Zolot\\Idle\\Zolot Idle 3.png",
                      4: "Sprites\\Enemies\\Zolot\\Idle\\Zolot Idle 4.png",
                      5: "Sprites\\Enemies\\Zolot\\Idle\\Zolot Idle 5.png",
                      6: "Sprites\\Enemies\\Zolot\\Idle\\Zolot Idle 6.png"}

ZOLOT_RUN_SPRITES = {1: "Sprites\\Enemies\\Zolot\\Run\\Zolot Run 1.png",
                     2: "Sprites\\Enemies\\Zolot\\Run\\Zolot Run 2.png",
                     3: "Sprites\\Enemies\\Zolot\\Run\\Zolot Run 3.png",
                     4: "Sprites\\Enemies\\Zolot\\Run\\Zolot Run 4.png",
                     5: "Sprites\\Enemies\\Zolot\\Run\\Zolot Run 5.png",
                     6: "Sprites\\Enemies\\Zolot\\Run\\Zolot Run 6.png"}

ZOLOT_HURT_SPRITES = {1: "Sprites\\Enemies\\Zolot\\Hurt\\Zolot Hurt 1.png",
                      2: "Sprites\\Enemies\\Zolot\\Hurt\\Zolot Hurt 2.png",
                      3: "Sprites\\Enemies\\Zolot\\Hurt\\Zolot Hurt 3.png",
                      4: "Sprites\\Enemies\\Zolot\\Hurt\\Zolot Hurt 4.png",
                      5: "Sprites\\Enemies\\Zolot\\Hurt\\Zolot Hurt 5.png",
                      6: "Sprites\\Enemies\\Zolot\\Hurt\\Zolot Hurt 6.png"}

ZOLOT_ATTACK_SPRITES = {1: "Sprites\\Enemies\\Zolot\\Attack\\Zolot Attack 1.png",
                        2: "Sprites\\Enemies\\Zolot\\Attack\\Zolot Attack 2.png",
                        3: "Sprites\\Enemies\\Zolot\\Attack\\Zolot Attack 3.png",
                        4: "Sprites\\Enemies\\Zolot\\Attack\\Zolot Attack 4.png",
                        5: "Sprites\\Enemies\\Zolot\\Attack\\Zolot attack 5.png",
                        6: "Sprites\\Enemies\\Zolot\\Attack\\Zolot attack 6.png"}

ZOLOT_DEATH_SPRITES = {1: "Sprites\\Enemies\\Zolot\\Die\\Zolot Die 1.png",
                       2: "Sprites\\Enemies\\Zolot\\Die\\Zolot Die 2.png",
                       3: "Sprites\\Enemies\\Zolot\\Die\\Zolot Die 3.png",
                       4: "Sprites\\Enemies\\Zolot\\Die\\Zolot Die 4.png",
                       5: "Sprites\\Enemies\\Zolot\\Die\\Zolot Die 5.png",
                       6: "Sprites\\Enemies\\Zolot\\Die\\Zolot Die 6.png"}

# These constants outline the directories at which the sprites for the Viking units are stored. (Dec 13)
VIKING_RUN_SPRITES = {1: "Sprites\\Troops\\Viking\\Run\\run1.png",
                      2: "Sprites\\Troops\\Viking\\Run\\run2.png",
                      3: "Sprites\\Troops\\Viking\\Run\\run3.png",
                      4: "Sprites\\Troops\\Viking\\Run\\run4.png",
                      5: "Sprites\\Troops\\Viking\\Run\\run5.png",
                      6: "Sprites\\Troops\\Viking\\Run\\run6.png",
                      7: "Sprites\\Troops\\Viking\\Run\\run7.png",
                      8: "Sprites\\Troops\\Viking\\Run\\run8.png"}

VIKING_IDLE_SPRITES = {1: "Sprites\\Troops\\Viking\\Idle\\idle2.png",
                       2: "Sprites\\Troops\\Viking\\Idle\\idle3.png",
                       3: "Sprites\\Troops\\Viking\\Idle\\idle4.png",
                       4: "Sprites\\Troops\\Viking\\Idle\\idle5.png",
                       5: "Sprites\\Troops\\Viking\\Idle\\idle6.png",
                       6: "Sprites\\Troops\\Viking\\Idle\\idle1.png"}

VIKING_ATTACK_SPRITES = {1: "Sprites\\Troops\\Viking\\Attack\\attack0.png",
                         2: "Sprites\\Troops\\Viking\\Attack\\attack1.png",
                         3: "Sprites\\Troops\\Viking\\Attack\\attack2.png",
                         4: "Sprites\\Troops\\Viking\\Attack\\attack3.png",
                         5: "Sprites\\Troops\\Viking\\Attack\\attack0.png"}

VIKING_HURT_SPRITES = {1: "Sprites\\Troops\\Viking\\Hurt\\hurt1.png",
                       2: "Sprites\\Troops\\Viking\\Hurt\\hurt2.png",
                       3: "Sprites\\Troops\\Viking\\Hurt\\hurt3.png",
                       4: "Sprites\\Troops\\Viking\\Hurt\\hurt4.png"}

VIKING_DEATH_SPRITES = {1: "Sprites\\Troops\\Viking\\Death\\death1.png",
                        2: "Sprites\\Troops\\Viking\\Death\\death2.png",
                        3: "Sprites\\Troops\\Viking\\Death\\death3.png",
                        4: "Sprites\\Troops\\Viking\\Death\\death4.png",
                        5: "Sprites\\Troops\\Viking\\Death\\death5.png",
                        6: "Sprites\\Troops\\Viking\\Death\\death6.png",
                        7: "Sprites\\Troops\\Viking\\Death\\death7.png",
                        8: "Sprites\\Troops\\Viking\\Death\\death8.png",
                        9: "Sprites\\Troops\\Viking\\Death\\death9.png",
                        10: "Sprites\\Troops\\Viking\\Death\\death10.png"}

VIKING_SPAWN_SPRITES = {1: "Sprites\\Troops\\Viking\\Spawn\\Spawn 1.png",
                        2: "Sprites\\Troops\\Viking\\Spawn\\Spawn 2.png",
                        3: "Sprites\\Troops\\Viking\\Spawn\\Spawn 3.png",
                        4: "Sprites\\Troops\\Viking\\Spawn\\Spawn 4.png",
                        5: "Sprites\\Troops\\Viking\\Spawn\\Spawn 5.png",
                        6: "Sprites\\Troops\\Viking\\Spawn\\Spawn 6.png",
                        7: "Sprites\\Troops\\Viking\\Spawn\\Spawn 7.png",
                        8: "Sprites\\Troops\\Viking\\Spawn\\Spawn 8.png"}

# These constants outline the directories at which the sprites for Ogre enemies are stored. (Jan 6)
OGRE_IDLE_SPRITES = {1: "Sprites\\Enemies\\Ogre\\Idle\\idle1.png",
                     2: "Sprites\\Enemies\\Ogre\\Idle\\idle2.png",
                     3: "Sprites\\Enemies\\Ogre\\Idle\\idle3.png",
                     4: "Sprites\\Enemies\\Ogre\\Idle\\idle4.png",
                     5: "Sprites\\Enemies\\Ogre\\Idle\\idle5.png",
                     6: "Sprites\\Enemies\\Ogre\\Idle\\idle6.png"}

OGRE_RUN_SPRITES = {1: "Sprites\\Enemies\\Ogre\\Run\\run1.png",
                    2: "Sprites\\Enemies\\Ogre\\Run\\run2.png",
                    3: "Sprites\\Enemies\\Ogre\\Run\\run3.png",
                    4: "Sprites\\Enemies\\Ogre\\Run\\run4.png",
                    5: "Sprites\\Enemies\\Ogre\\Run\\run5.png",
                    6: "Sprites\\Enemies\\Ogre\\Run\\run6.png"}

OGRE_HURT_SPRITES = {1: "Sprites\\Enemies\\Ogre\\Hurt\\hurt1.png",
                     2: "Sprites\\Enemies\\Ogre\\Hurt\\hurt2.png",
                     3: "Sprites\\Enemies\\Ogre\\Hurt\\hurt3.png",
                     4: "Sprites\\Enemies\\Ogre\\Hurt\\hurt4.png",
                     5: "Sprites\\Enemies\\Ogre\\Hurt\\hurt5.png",
                     6: "Sprites\\Enemies\\Ogre\\Hurt\\hurt6.png"}

OGRE_ATTACK_SPRITES = {1: "Sprites\\Enemies\\Ogre\\Attack\\attack1.png",
                       2: "Sprites\\Enemies\\Ogre\\Attack\\attack2.png",
                       3: "Sprites\\Enemies\\Ogre\\Attack\\attack3.png",
                       4: "Sprites\\Enemies\\Ogre\\Attack\\attack4.png",
                       5: "Sprites\\Enemies\\Ogre\\Attack\\attack5.png",
                       6: "Sprites\\Enemies\\Ogre\\Attack\\attack6.png"}

OGRE_DEATH_SPRITES = {1: "Sprites\\Enemies\\Ogre\\Die\\die1.png",
                      2: "Sprites\\Enemies\\Ogre\\Die\\die2.png",
                      3: "Sprites\\Enemies\\Ogre\\Die\\die3.png",
                      4: "Sprites\\Enemies\\Ogre\\Die\\die4.png",
                      5: "Sprites\\Enemies\\Ogre\\Die\\die5.png",
                      6: "Sprites\\Enemies\\Ogre\\Die\\die6.png"}

# Game Boundaries Constants (Updated: Jan 20)
PLAYER_HORIZONTAL_STOP_DISTANCE = 48
VIKING_HORIZONTAL_STOP_DISTANCE = 16
ZOLOT_HORIZONTAL_STOP_DISTANCE = 16
OGRE_HORIZONTAL_STOP_DISTANCE = 28
FIREBALL_STOP_DISTANCE = 10
BACKGROUND_VERTICAL_POS = 0
TOP_LIMIT = 245
BOTTOM_LIMIT = 324
BACKGROUND_DEPTH_FACTOR = 3.0
MIN_BOUNCE_SPEED = 3.5
BLACK_OUT_TOLERANCE = 100

# Sprite Rect Constants (Updated: Jan 17)
COIN_HEIGHT = 8
X_SPAWN_DISTANCE = 62
Y_SPAWN_DISTANCE = 20
DEFAULT_EMPTY_X_TOLERANCE = 15
DEFAULT_EMPTY_Y_TOLERANCE = 12
DEFAULT_ATTACK_MAX_X_TOLERANCE = 5
DEFAULT_ATTACK_MIN_X_TOLERANCE = 28
DEFAULT_ATTACK_Y_TOLERANCE = 5
ZOLOT_ATTACK_MAX_X_TOLERANCE = -2
OGRE_ATTACK_MAX_X_TOLERANCE = -1
PROTAGONIST_SPELL_EXECUTE_X = 50
PROTAGONIST_SPELL_EXECUTE_Y = 0
PROTAGONIST_SPELL_EXECUTE_Z = 16
VIKING_FORWARD_FOLLOW_DISTANCE = 170
VIKING_BACKWARD_FOLLOW_DISTANCE = 225
VIKING_FOLLOW_SLACK = 1.5
VIKING_FOLLOW_BUFFER_DISTANCE = 15

# Z-Correction Constants (Created: Jan 17)
ZOLOT_DEATH_Z = -2.0
FIREBALL_Z_CORRECTION = -2
DEFAULT_Z_CORRECTION = 0.3
PROTAGONIST_DEATH_Z = -9.0
OGRE_DEATH_Z = -3.8

# These constants are how certain groups of sprites are referred to by the objects. (Nov 24)
PROTAGONIST_RUN_CODE = "A"
PROTAGONIST_IDLE_CODE = "B"
COUNTER_ICONS_CODE = "C"
COIN_SPRITES_CODE = "D"
PROTAGONIST_ATTACK_CODE = "E"
BACKGROUND_SPRITE_CODE = "F"
PROP_SPRITE_CODE = "G"
HUD_SPRITE_CODE = "H"
PROTAGONIST_SPELL_CODE = "I"
ZOLOT_IDLE_CODE = "J"
ZOLOT_RUN_CODE = "K"
VIKING_IDLE_CODE = "L"
VIKING_RUN_CODE = "M"
VIKING_ATTACK_CODE = "N"
ZOLOT_HURT_CODE = "O"
VIKING_HURT_CODE = "P"
ZOLOT_ATTACK_CODE = "Q"
PROTAGONIST_HURT_CODE = "R"
ZOLOT_DEATH_CODE = "S"
VIKING_DEATH_CODE = "T"
OGRE_IDLE_CODE = "U"
OGRE_RUN_CODE = "V"
OGRE_ATTACK_CODE = "W"
OGRE_HURT_CODE = "X"
OGRE_DEATH_CODE = "Y"
PROTAGONIST_DEATH_CODE = "Z"
FIREBALL_AIRBORNE_CODE = "AA"
FIREBALL_IMPACT_CODE = "AB"
VIKING_SPAWN_CODE = "AC"
FIREBALL_SPAWN_CODE = "AD"

# Constants for the frame rate of the animations. (Nov 22)
PROTAGONIST_RUN_FRAMES = 2
PROTAGONIST_IDLE_FRAMES = 3
PROTAGONIST_SLASH_ATTACK_FRAMES = 1
PROTAGONIST_SPELL_ATTACK_FRAMES = 1
PROTAGONIST_HURT_FRAMES = 4
COIN_ANIMATION_FRAMES = 5
PROTAGONIST_DEATH_FRAMES = 2
VIKING_RUN_FRAMES = 3
VIKING_IDLE_FRAMES = 5
VIKING_ATTACK_FRAMES = 3
VIKING_SPAWN_FRAMES = 2
VIKING_HURT_FRAMES = 2
VIKING_DEATH_FRAMES = 4
ZOLOT_IDLE_FRAMES = 3
ZOLOT_RUN_FRAMES = 3
ZOLOT_HURT_FRAMES = 2
ZOLOT_ATTACK_FRAMES = 2
ZOLOT_DEATH_FRAMES = 3
FIREBALL_MOVE_FRAMES = 2
FIREBALL_IMPLODE_FRAMES = 2
FIREBALL_SPAWN_FRAMES = 1
OGRE_IDLE_FRAMES = 3
OGRE_RUN_FRAMES = 3
OGRE_HURT_FRAMES = 2
OGRE_ATTACK_FRAMES = 2
OGRE_DEATH_FRAMES = 3

# Sprite Size Constants (Updated: Nov 23)
PLAYER_SCALING_FACTOR = 0.2
COIN_SCALING_FACTOR = 0.8
BACKGROUND_SCALING_FACTOR = 0.4
PROP_SCALING_FACTOR = 2.3
ZOLOT_SCALING_FACTOR = 0.3
OGRE_SCALING_FACTOR = 0.5
VIKING_SCALING_FACTOR = 1
FIREBALL_SCALING_FACTOR = 1

# This constant outlines the directories for the animation for the coin objects. (Nov 26)
COIN_SPRITES = {1: "Sprites\\Coins\\Coin 1.png",
                2: "Sprites\\Coins\\Coin 2.png",
                3: "Sprites\\Coins\\Coin 3.png",
                4: "Sprites\\Coins\\Coin 4.png"}

# These constants outlines the directories for the fireball objects. (Jan 10)
FIREBALL_AIRBORNE_SPRITES = {1: "Sprites\\Main Character\\Spells\\Firewave\\Firewave 1.png",
                             2: "Sprites\\Main Character\\Spells\\Firewave\\Firewave 2.png",
                             3: "Sprites\\Main Character\\Spells\\Firewave\\Firewave 3.png"}

FIREBALL_IMPACT_SPRITES = {1: "Sprites\\Main Character\\Spells\\Firewave\\Firewave 4.png",
                           2: "Sprites\\Main Character\\Spells\\Firewave\\Firewave 5.png",
                           3: "Sprites\\Main Character\\Spells\\Firewave\\Firewave 6.png",
                           4: "Sprites\\Main Character\\Spells\\Firewave\\Firewave 7.png",
                           5: "Sprites\\Main Character\\Spells\\Firewave\\Firewave 8.png",
                           6: "Sprites\\Main Character\\Spells\\Firewave\\Firewave 9.png"}

FIREBALL_SPAWN_SPRITES = {1: "Sprites\\Main Character\\Spells\\Firewave\\fire_spawn0.png",
                          2: "Sprites\\Main Character\\Spells\\Firewave\\fire_spawn1.png",
                          3: "Sprites\\Main Character\\Spells\\Firewave\\fire_spawn2.png",
                          4: "Sprites\\Main Character\\Spells\\Firewave\\fire_spawn3.png",
                          5: "Sprites\\Main Character\\Spells\\Firewave\\fire_spawn4.png"}

# Hazard Sprites Constants (Created: Jan 13)
OGRE_HAZARD_SPRITES = ["W3", "W-3"]
VIKING_HAZARD_SPRITES = ["N3", "N-3"]
ZOLOT_HAZARD_SPRITES = ["Q4", "Q-4"]
PROTAGONIST_HAZARD_SPRITES = ["E6", "E-6"]
PROTAGONIST_SPELL_EXECUTE_SPRITE = 4

# Lighting and Shadows Constants (Updated: Nov 29)
DEFAULT_SHADOW_DEPTH = 10
SHADOW_RGBA = (50, 50, 50, 100)
SHADOW_SCALING_FACTOR = 1.1

# Collision Detection Constants (Updated: Jan 20)
COIN_DEPTH_SENSITIVITY = 5
ZOLOT_DEPTH_SENSITIVITY = 6
VIKING_DEPTH_SENSITIVITY = 6
OGRE_DEPTH_SENSITIVITY = 6
PLAYER_DEPTH_SENSITIVITY = 7
FIREBALL_DEPTH_SENSITIVITY = 6
DEFAULT_KNOCKBACK_SPEED = 10
OGRE_KNOCKBACK_SPEED = 6
OGRE_KNOCKBACK_DAMPENING = 0.6
DEFAULT_KNOCKBACK_DAMPENING = 1
DEFAULT_AIR_KNOCKBACK_DAMPENING = 0.6
DEFAULT_COLLISION_DEPTH = 5
DAMAGE_REGISTER_FRAMES = 5

# This constant outlines the directories for the background tile-set. (Nov 29)
BACKGROUND_SPRITES = {1: "Sprites\\Background Images\\Sky.png",
                      2: "Sprites\\Background Images\\Nature Background.png",
                      3: "Sprites\\Background Images\\Nature Foreground.png"}

# This constant outlines the directories at which prop sprites are stored. (Nov 29)
PROP_SPRITES = {1: "Sprites\\Props\\Tree 1.png",
                2: "Sprites\\Props\\Tree 2.png"}

# This constant outlines the directories at which the HUD sprites are stored. (Dec 1)
HUD_SPRITES = {'MAIN': "Sprites\\HUD Bars\\HUD Main.png",
               'HEALTH': "Sprites\\HUD Bars\\Health Bar End.png",
               'FOOD': "Sprites\\HUD Bars\\Food Bar End.png",
               'MANA': "Sprites\\HUD Bars\\Mana Bar End.png"}

# HUD Constants (Updated: Jan 17)
HUD_POS = (7, 7)
HUD_SCALING_FACTOR = 1
HUD_VERTICAL_ADJUSTMENT = 4
HUD_VERTICAL_SEPARATION = 20
HUD_CAP_POS_ADJUSTMENT = -2
HUD_BAR_LENGTH = 125
HUD_BAR_THICKNESS = 15
HEALTH_BAR_COLOR = (99, 219, 105)
FOOD_BAR_COLOR = (196, 55, 55)
MANA_BAR_COLOR = (55, 126, 196)
EMPTY_BAR_COLOR = (160, 160, 160)
BAR_EDGE_HORIZONTAL_THICKNESS = 1
BAR_EDGE_VERTICAL_THICKNESS = 2
BAR_EDGE_COLOR = (25, 25, 25)
BAR_BUFFER_ZONE = 1
COUNTER_HEIGHT = 23
COUNTER_FONT_TYPE = "consolas"
COUNTER_TEXT_SIZE = 21
GOLD_COUNTER_POSITION = (530, 10)
GOLD_COUNTER_HORIZONTAL_SHIFT = 10
COUNTER_FONT_COLOUR = (0, 0, 0)
COUNTER_MARGIN = 7
GOLD_COUNTER_ICON = "Sprites\\UI\\gold_icon.png"
HUD_ANIMATION_SENSITIVITY = 1
HUD_ANIMATION_CONSTANT = 0.3

# Resource Management Constants (Updated: Jan 17)
PLAYER_MAX_HEALTH = 100
MAX_FOOD = 100
MAX_MANA = 100
VIKING_SPAWN_COST = 35
FIREBALL_COST = 20
MANA_REGENERATION = 0.1
ZOLOT_FOOD_GAIN = 10
OGRE_FOOD_GAIN = 22

# NPC HP Constants (Created: Dec 30)
ZOLOT_MAX_HEALTH = 15
VIKING_MAX_HEALTH = 23
OGRE_MAX_HEALTH = 40
NPC_BAR_LENGTH = 50
NPC_BAR_THICKNESS = 10
NPC_BAR_EDGE_THICKNESS = 2
NPC_BAR_EDGE_COLOUR = (25, 25, 25)
NPC_BAR_FILL = (99, 219, 105)
NPC_BAR_EMPTY_FILL = (160, 160, 160)
NPC_BAR_ANIMATION_CONSTANT = 0.3
NPC_BAR_ANIMATION_SENSITIVITY = 1
NPC_BAR_BUFFER_ZONE = 1
ZOLOT_BAR_CLEARANCE = 70
VIKING_BAR_CLEARANCE = 60
OGRE_BAR_CLEARANCE = 112

# Position Correction Constants (Created: Dec 26)
ZOLOT_ATTACK_POSITION_CORRECTION = {1: 0,
                                    2: -5,
                                    3: -5,
                                    4: 16,
                                    5: -3,
                                    6: -3}

VIKING_ATTACK_POSITION_CORRECTION = {1: 0,
                                     2: 0,
                                     3: 30,
                                     4: 0,
                                     5: -30}

OGRE_ATTACK_POSITION_CORRECTION = {1: 0,
                                   2: 2,
                                   3: 9,
                                   4: -9,
                                   5: -2,
                                   6: 0}

# Initial Sprite Constants (Updated: Jan 20)
PLAYER_INITIAL_SPRITE = "B1"
VIKING_INITIAL_SPRITE = "AC1"
ZOLOT_INITIAL_SPRITE = "J1"
OGRE_INITIAL_SPRITE = "U1"
FIREBALL_INITIAL_SPRITE = "AD1"
COIN_INITIAL_SPRITE = "D1"

# Game Over Screen Constants (Created: Dec 29)
GAME_OVER_SCREEN_WIDTH = 200
GAME_OVER_SCREEN_HEIGHT = 130
GAME_OVER_SCREEN_BORDER_COLOR = (25, 25, 25)
GAME_OVER_SCREEN_UNSUCCESSFUL_FILL_COLOR = (200, 50, 50)
GAME_OVER_SCREEN_SUCCESSFUL_FILL_COLOR = (19, 143, 0)
GAME_OVER_SCREEN_BORDER_WIDTH = 3
GAME_OVER_SCREEN_FONT_TYPE = 'consolas'
GAME_OVER_SCREEN_FONT_SIZE = 26
GAME_OVER_SCREEN_FONT_COLOR = (10, 10, 10)
GAME_OVER_UNSUCCESSFUL_MESSAGE = "YOU LOSE"
GAME_OVER_SUCCESSFUL_MESSAGE = "YOU WIN"
GAME_OVER_SCREEN_ANIMATION_FRAMES = 2
GAME_OVER_SCREEN_DISPLAY_MIN_SIZE = 0.2
GAME_OVER_SCREEN_DISPLAY_SIZE_INC = 0.1

# Black Out Constants (Created: Jan 20)
BLACK_OUT_ANIMATION_CONSTANT = 0.035
BLACK_OUT_DELAY = 10
BLACK_OUT_COLOR = (10, 10, 10)

# This constant outlines the damage dealt by various entities in the game. (Dec 29)
DAMAGE_DICT = {'Protagonist': 7,
               'Zolot': 5,
               'Viking': 5,
               'Ogre': 11,
               'Fireball': 10}

# Level Design Constants (Updated: Jan 28)
LEVELS = [{"SPAWN": (160, 300),
           "LENGTH": 1500,
           "PROPS": [(110, 241, 1), (750, 327, 1), (1390, 241, 2)],
           "COINS": [(375, 300), (425, 300), (475, 300), (1030, 280), (1080, 280), (1130, 280)],
           "ENEMIES": []},
          {"LENGTH": 1000,
           "PROPS": [(250, 241, 1), (850, 327, 2)],
           "COINS": [(400, 285), (450, 285), (350, 285)],
           "ENEMIES": [(800, 320, 1), (850, 250, 1), (900, 310, 1)],
           "SPAWN": (160, 300)},
          {"LENGTH": 1300,
           "PROPS": [(200, 241, 2), (1100, 241, 1)],
           "COINS": [],
           "ENEMIES": [(400, 300, 1), (450, 320, 1), (850, 320, 1), (900, 300, 1)],
           "SPAWN": (650, 260),
           "CAMERA_POS": 650},
          {"LENGTH": 1200,
           "PROPS": [(840, 241, 1)],
           "COINS": [(950, 314), (1000, 304), (1050, 297), (1100, 290), (1050, 283), (1000, 276), (950, 269)],
           "ENEMIES": [(150, 284, 1), (230, 312, 2), (750, 250, 1), (850, 300, 1)],
           "SPAWN": (400, 260)},
          {"LENGTH": 1600,
           "PROPS": [(750, 241, 1), (1500, 327, 2)],
           "COINS": [(1100, 284), (1150, 274), (1150, 294), (1200, 274), (1200, 294), (1250, 284)],
           "ENEMIES": [(200, 260, 1), (250, 300, 1), (550, 250, 1), (600, 300, 1), (1000, 260, 2), (1100, 320, 2)],
           "SPAWN": (400, 280),
           "CAMERA_POS": 350},
          {"SPAWN": (200, 285),
           "LENGTH": 1200,
           "PROPS": [(510, 241, 1)],
           "COINS": [],
           "ENEMIES": [(75, 285, 1), (325, 285, 1), (900, 275, 2), (1000, 270, 2), (1100, 310, 2)]},
          {"LENGTH": 1100,
           "PROPS": [(100, 241, 1), (1000, 241, 2)],
           "COINS": [(400, 300), (450, 290), (500, 280), (700, 300), (750, 290), (800, 280)],
           "ENEMIES": [],
           "SPAWN": (235, 290)},
          {"SPAWN": (1000, 280),
           "CAMERA_POS": 1000,
           "LENGTH": 2000,
           "PROPS": [(500, 241, 1), (1500, 327, 2)],
           "COINS": [],
           "ENEMIES": [(875, 280, 1), (1125, 280, 1), (100, 300, 2), (200, 260, 2), (1900, 300, 2), (1800, 260, 2)]},
          {"SPAWN": (160, 300),
           "LENGTH": 2100,
           "PROPS": [(100, 241, 2), (720, 241, 1), (1650, 327, 2)],
           "COINS": [(1900, 284), (1950, 284), (2000, 284)],
           "ENEMIES": [(400, 310, 1), (475, 290, 1), (1300, 253, 2), (1400, 270, 2), (1500, 290, 2), (1600, 270, 2), (1700, 310, 2)]},
          {"SPAWN": (850, 284),
           "CAMERA_POS": 850,
           "LENGTH": 1700,
           "ENEMIES": [(200, 251, 2), (200, 317, 2), (300, 284, 1), (400, 251, 2), (400, 317, 2), (1300, 251, 2), (1300, 317, 2), (1400, 284, 1), (1500, 251, 2), (1500, 317, 2)],
           "COINS": [(700, 270), (750, 260), (945, 310), (995, 300), (700, 300), (750, 310), (945, 260), (995, 270)],
           "PROPS": [(200, 241, 1), (1500, 241, 2)]},
          {"LENGTH": 1150,
           "SPAWN": (160, 300),
           "ENEMIES": [],
           "COINS": [],
           "PROPS": [(500, 241, 2), (1000, 327, 1)]}]
