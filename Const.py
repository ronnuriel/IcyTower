import pygame

GAME_FPS = 150
WIDTH, HEIGHT = 800, 600
JUMPING_HEIGHT = 20
MAX_ACCELERATION = 10
VEL_X = 3  # Setting the moving speed.
VEL_Y = JUMPING_HEIGHT  # Setting the jumping height.

# Walls settings:
WALLS_Y = -128
WALL_WIDTH = 128
WALLS_ROLLING_SPEED = 2
RIGHT_WALL_BOUND = WIDTH - WALL_WIDTH
LEFT_WALL_BOUND = WALL_WIDTH

GAMEPLAY_SOUND_LENGTH = 31  # 31 seconds.
SHELVES_COUNT = 500  # Number of shelves in the game.
MAX_SHELF_NUMBER = 0

# Constants:
LEVEL_UP = 30
# Colors:
GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
INSTRUCTIONS_BACKGROUNDCOLOR = (150, 195, 213, 255)

pygame.init()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))


# Images:
BODY_IMAGE = pygame.image.load("Assets/icyMan.png")
BACKGROUND = pygame.image.load("Assets/background2.jpg")
BRICK_IMAGE = pygame.image.load("Assets/brick_block.png")
SHELF_BRICK_IMAGE = pygame.image.load("Assets/shelf_brick.png")
SHELF_BRICK_IMAGE2 = pygame.image.load("Assets/ice.png")
SHELF_BRICK_IMAGE3 = pygame.image.load("Assets/fire.png.webp")
MAINMENU_BACKGROUND = pygame.transform.scale(pygame.image.load("Assets/IcyTowerBackground.gif"), (WIDTH, HEIGHT))
CENTER_X = (WIDTH - MAINMENU_BACKGROUND.get_width()) // 2
CENTER_Y = (HEIGHT - MAINMENU_BACKGROUND.get_height()) // 2
GAME_OVER_BACKGROUND = pygame.transform.scale(pygame.image.load("Assets/game_over.png"), (WIDTH, HEIGHT))
GAME_OVER_BACKGROUND.set_colorkey(BLACK)
instruction_images = [
    pygame.transform.scale(pygame.image.load(r"Assets/game_instructions_goal.png"), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load(r"Assets/game_instructions_howTo.png"), (WIDTH, HEIGHT))

]