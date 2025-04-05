import pygame
import math
from constants import *

class Bullet:
    def __init__(self, x, y, target_x, target_y, option_index):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 15
        self.speed = 0.5
        self.option_index = option_index
        
        # Calculate direction vector
        dx = target_x - x
        dy = target_y - y
        distance = math.sqrt(dx * dx + dy * dy)
        self.direction_x = dx / distance if distance > 0 else 0
        self.direction_y = dy / distance if distance > 0 else -1
        
        # Calculate angle for drawing
        self.angle = math.degrees(math.atan2(-self.direction_y, self.direction_x)) - 90
        
    def update(self, dt):
        self.x += self.direction_x * self.speed * dt
        self.y += self.direction_y * self.speed * dt
        
    def draw(self, surface):
        # Draw bullet as a small elongated rectangle
        bullet_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(bullet_surface, CYAN, (0, 0, self.width, self.height))
        
        # Rotate bullet to face direction of travel
        rotated_bullet = pygame.transform.rotate(bullet_surface, self.angle)
        rect = rotated_bullet.get_rect(center=(self.x, self.y))
        surface.blit(rotated_bullet, rect.topleft)
        
    def check_collision(self, problem):
        # Simple circular collision detection with asteroid
        dx = self.x - problem.x
        dy = self.y - problem.y
        distance = math.sqrt(dx * dx + dy * dy)
        return distance < problem.radius 