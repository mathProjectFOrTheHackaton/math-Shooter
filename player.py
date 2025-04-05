import pygame
from constants import *

class Player:
    win_sfx = pygame.mixer.Sound("winners_W9Cpenj.mp3")
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 60
        self.width = 50
        self.height = 50
        self.score = 0
        self.point_counter = 0
        self.level = 1  # Initialize player level to 1
        self.lives = 3
        
    def draw(self, surface):
        # Draw a simple spaceship
        pygame.draw.polygon(surface, CYAN, [
            (self.x, self.y - 25),
            (self.x - 20, self.y + 15),
            (self.x, self.y + 5),
            (self.x + 20, self.y + 15)
        ])

    def update_level(self):
        # Calculate level based on score (level increases every 100 points)
        new_level = (self.score // 100) + 1
        
        # Only update if level has increased
        if new_level > self.level:
            self.level = new_level
            self.win_sfx.play()
            return True  # Return True if level increased
        return False  # Return False if level didn't change
        
    def move_to(self, x):
        self.x = max(25, min(SCREEN_WIDTH - 25, x)) 