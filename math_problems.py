import pygame
import random
import math
from constants import *

class MathProblem:
    def __init__(self, x, y, level):
        self.level = level
        self.generate_problem()
        self.x = x
        self.y = y
        
        # Adjust speed based on level
        if level == LEVEL_BASIC:
            self.speed = random.uniform(0.02, 0.06)
        elif level == LEVEL_INTERMEDIATE:
            self.speed = random.uniform(0.03, 0.08)
        else:  # LEVEL_ADVANCED
            self.speed = random.uniform(0.04, 0.1)
            
        self.selected = False
        self.correct_option_index = random.randint(0, 2)
        self.options = self.generate_options()
        self.width = 80
        self.height = 80
        self.option_rects = []
        self.update_option_rects()
        self.wrong_answer_clicked = False
        self.wrong_time = 0
        
        # Asteroid visual properties
        self.radius = 40
        self.rotation = random.uniform(0, 360)
        self.rotation_speed = random.uniform(-0.05, 0.05)
        self.points = []
        # Generate irregular asteroid shape
        for i in range(8):
            angle = i * 45 + random.uniform(-10, 10)
            distance = self.radius + random.uniform(-10, 10)
            x_offset = math.cos(math.radians(angle)) * distance
            y_offset = math.sin(math.radians(angle)) * distance
            self.points.append((x_offset, y_offset))
            
        # Explosion animation
        self.exploding = False
        self.explosion_radius = 0
        self.explosion_duration = 500  # in milliseconds
        self.explosion_start_time = 0
        
    def generate_problem(self):
        if self.level == LEVEL_BASIC:
            # Basic: Simple addition and subtraction with small numbers
            operation = random.choice(['+', '-'])
            
            if operation == '+':
                a = random.randint(1, 20)
                b = random.randint(1, 20)
                self.problem = f"{a} + {b}"
                self.answer = a + b
                
            else:  # subtraction
                a = random.randint(5, 20)
                b = random.randint(1, a)  # Ensure positive result
                self.problem = f"{a} - {b}"
                self.answer = a - b
                
        elif self.level == LEVEL_INTERMEDIATE:
            # Intermediate: All operations with medium-sized numbers
            operation = random.choice(['+', '-', '*'])
            
            if operation == '+':
                a = random.randint(10, 50)
                b = random.randint(10, 50)
                self.problem = f"{a} + {b}"
                self.answer = a + b
                
            elif operation == '-':
                a = random.randint(15, 50)
                b = random.randint(5, a)
                self.problem = f"{a} - {b}"
                self.answer = a - b
                
            else:  # multiplication
                a = random.randint(2, 12)
                b = random.randint(2, 12)
                self.problem = f"{a} × {b}"
                self.answer = a * b
                
        else:  # LEVEL_ADVANCED
            # Advanced: All operations including division, larger numbers
            operation = random.choice(['+', '-', '*', '/'])
            
            if operation == '+':
                a = random.randint(20, 99)
                b = random.randint(20, 99)
                self.problem = f"{a} + {b}"
                self.answer = a + b
                
            elif operation == '-':
                a = random.randint(30, 99)
                b = random.randint(10, a)
                self.problem = f"{a} - {b}"
                self.answer = a - b
                
            elif operation == '*':
                a = random.randint(5, 20)
                b = random.randint(5, 12)
                self.problem = f"{a} × {b}"
                self.answer = a * b
                
            else:  # division - ensure it divides evenly
                b = random.randint(2, 12)
                result = random.randint(1, 10)
                a = b * result
                self.problem = f"{a} ÷ {b}"
                self.answer = result
    
    def generate_options(self):
        options = [0, 0, 0]
        options[self.correct_option_index] = self.answer
        
        # Generate wrong answers that are close to the correct one
        for i in range(3):
            if i != self.correct_option_index:
                # Generate a wrong answer within ±10 of the correct answer, but not equal
                wrong_answer = self.answer
                while wrong_answer == self.answer or wrong_answer in options:
                    # Make offset larger for larger answers
                    max_offset = max(5, int(self.answer * 0.2))
                    offset = random.randint(1, max_offset) * random.choice([-1, 1])
                    wrong_answer = max(1, self.answer + offset)  # Ensure positive
                options[i] = wrong_answer
                
        return options
    
    def update_option_rects(self):
        self.option_rects = []
        for i in range(3):
            rect = pygame.Rect(
                self.x - 75 + (i * 60), 
                self.y + 40,
                50, 
                30
            )
            self.option_rects.append(rect)
    
    def update(self, dt):
        self.y += self.speed * dt
        self.update_option_rects()
        
        # Rotate asteroid
        self.rotation += self.rotation_speed * dt
        
        # Update explosion animation
        if self.exploding:
            current_time = pygame.time.get_ticks()
            progress = (current_time - self.explosion_start_time) / self.explosion_duration
            if progress >= 1:
                self.selected = True  # Mark for removal
            else:
                self.explosion_radius = self.radius * progress * 2
    
    def draw(self, surface):
        if self.exploding:
            # Draw explosion
            pygame.draw.circle(surface, ORANGE, (int(self.x), int(self.y)), int(self.explosion_radius))
            pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), int(self.explosion_radius * 0.7))
            return
        
        # Draw asteroid
        points = []
        for x_offset, y_offset in self.points:
            rotated_x = x_offset * math.cos(math.radians(self.rotation)) - y_offset * math.sin(math.radians(self.rotation))
            rotated_y = x_offset * math.sin(math.radians(self.rotation)) + y_offset * math.cos(math.radians(self.rotation))
            points.append((self.x + rotated_x, self.y + rotated_y))
            
        pygame.draw.polygon(surface, (150, 150, 150), points)
        
        # Draw problem text on asteroid
        problem_text = font_small.render(self.problem, True, WHITE)
        surface.blit(problem_text, (self.x - problem_text.get_width() // 2, self.y - problem_text.get_height() // 2))
        
        # Draw options below asteroid
        for i, option in enumerate(self.options):
            color = YELLOW
            if self.wrong_answer_clicked and i != self.correct_option_index:
                color = RED
                
            pygame.draw.rect(surface, color, self.option_rects[i], 0, 5)
            option_text = font_small.render(str(option), True, BLACK)
            text_x = self.option_rects[i].x + (self.option_rects[i].width - option_text.get_width()) // 2
            text_y = self.option_rects[i].y + (self.option_rects[i].height - option_text.get_height()) // 2
            surface.blit(option_text, (text_x, text_y))
        
        # Show "Wrong" text if a wrong answer was clicked
        if self.wrong_answer_clicked:
            wrong_text = font_medium.render("Wrong!", True, RED)
            surface.blit(wrong_text, (self.x - wrong_text.get_width() // 2, self.y - 30))
    
    def start_explosion(self):
        self.exploding = True
        self.explosion_start_time = pygame.time.get_ticks() 