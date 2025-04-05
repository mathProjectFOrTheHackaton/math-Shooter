import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
CYAN = (0, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 40)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math Shooter")

# Font
font_large = pygame.font.SysFont("Arial", 40, bold=True)
font_medium = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 24)

# Game states
STATE_MENU = 0
STATE_GAME = 1
STATE_GAME_OVER = 2

# Difficulty levels
LEVEL_BASIC = 0
LEVEL_INTERMEDIATE = 1
LEVEL_ADVANCED = 2 