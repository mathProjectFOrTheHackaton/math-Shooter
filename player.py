import pygame
from constants import *

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 60
        self.width = 50
        self.height = 50
        self.score = 0
        self.point_counter = 0
        #self.current_level = 1
        self.lives = 3
        
    def draw(self, surface):
        # Draw a simple spaceship
        pygame.draw.polygon(surface, CYAN, [
            (self.x, self.y - 25),
            (self.x - 20, self.y + 15),
            (self.x, self.y + 5),
            (self.x + 20, self.y + 15)
        ])

    def update_level(self, current_level):
        self.current_level = self.score // 100
        if self.score // 100 > self.current_level:
            self.current_level +=1 
        
    def move_to(self, x):
        self.x = max(25, min(SCREEN_WIDTH - 25, x)) 