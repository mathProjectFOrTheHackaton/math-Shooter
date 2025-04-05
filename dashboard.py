import pygame
import sys
import random
import math
from pygame.locals import *

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

# Create the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Math Shooter")

# Font
font_large = pygame.font.SysFont("Arial", 32)
font_medium = pygame.font.SysFont("Arial", 28)
font_small = pygame.font.SysFont("Arial", 24)

class MathProblem:
    def __init__(self, x, y):
        self.generate_problem()
        self.x = x
        self.y = y
        self.speed = random.uniform(0.02, 0.08)  # Even slower speed
        self.selected = False
        self.correct_option_index = random.randint(0, 2)
        self.options = self.generate_options()
        self.width = 150
        self.height = 100
        self.option_rects = []
        self.update_option_rects()
        self.wrong_answer_clicked = False
        self.wrong_time = 0
        
    def generate_problem(self):
        # Generate basic math problems (addition, subtraction, multiplication)
        operation = random.choice(['+', '-', '*'])
        
        if operation == '+':
            a = random.randint(1, 50)
            b = random.randint(1, 50)
            self.problem = f"{a} + {b}"
            self.answer = a + b
            
        elif operation == '-':
            a = random.randint(10, 50)
            b = random.randint(1, a)  # Ensure positive result
            self.problem = f"{a} - {b}"
            self.answer = a - b
            
        else:  # multiplication
            a = random.randint(1, 12)
            b = random.randint(1, 12)
            self.problem = f"{a} × {b}"
            self.answer = a * b
    
    def generate_options(self):
        options = [0, 0, 0]
        options[self.correct_option_index] = self.answer
        
        # Generate wrong answers that are close to the correct one
        for i in range(3):
            if i != self.correct_option_index:
                # Generate a wrong answer within ±10 of the correct answer, but not equal
                wrong_answer = self.answer
                while wrong_answer == self.answer or wrong_answer in options:
                    offset = random.randint(1, 10) * random.choice([-1, 1])
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
    
    def draw(self, surface):
        # Draw problem
        problem_text = font_medium.render(self.problem, True, WHITE)
        surface.blit(problem_text, (self.x - problem_text.get_width() // 2, self.y))
        
        # Draw options
        for i, option in enumerate(self.options):
            color = YELLOW
            if self.selected:
                color = GREEN if i == self.correct_option_index else RED
            elif self.wrong_answer_clicked and i != self.correct_option_index:
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

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 60
        self.width = 50
        self.height = 50
        self.score = 0
        self.lives = 3
        
    def draw(self, surface):
        # Draw a simple spaceship
        pygame.draw.polygon(surface, CYAN, [
            (self.x, self.y - 25),
            (self.x - 20, self.y + 15),
            (self.x, self.y + 5),
            (self.x + 20, self.y + 15)
        ])

class Game:
    def __init__(self):
        self.player = Player()
        self.math_problems = []
        self.spawn_timer = 0
        self.spawn_delay = 10000  # milliseconds (10 seconds)
        self.last_time = pygame.time.get_ticks()
        self.game_over = False
        
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                # Check if player clicked on any option
                for problem in self.math_problems:
                    if problem.selected or problem.y > SCREEN_HEIGHT:
                        continue  # Skip already answered or off-screen problems
                        
                    for i, rect in enumerate(problem.option_rects):
                        if rect.collidepoint(event.pos):
                            if i == problem.correct_option_index:
                                problem.selected = True
                                self.player.score += 10
                            else:
                                problem.wrong_answer_clicked = True
                                problem.wrong_time = pygame.time.get_ticks()
                                self.player.lives -= 1
                                if self.player.lives <= 0:
                                    self.game_over = True
            
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                if self.game_over and event.key == K_RETURN:
                    self.__init__()  # Reset the game
    
    def update(self):
        current_time = pygame.time.get_ticks()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # Spawn new math problems
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            x = random.randint(100, SCREEN_WIDTH - 100)
            self.math_problems.append(MathProblem(x, -50))
            
        # Update math problems
        for problem in list(self.math_problems):
            problem.update(dt)
            
            # Remove problems that go off-screen or are answered correctly
            if problem.y > SCREEN_HEIGHT or problem.selected:
                self.math_problems.remove(problem)
                
                # If problem goes off-screen without being answered, lose a life
                if not problem.selected and problem.y > SCREEN_HEIGHT:
                    self.player.lives -= 1
                    if self.player.lives <= 0:
                        self.game_over = True
        
    def draw(self):
        screen.fill(DARK_BLUE)
        
        # Draw background stars
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 3)
            pygame.draw.circle(screen, WHITE, (x, y), size)
        
        # Draw math problems
        for problem in self.math_problems:
            problem.draw(screen)
        
        # Draw player
        self.player.draw(screen)
        
        # Draw HUD
        score_text = font_medium.render(f"Score: {self.player.score}", True, WHITE)
        screen.blit(score_text, (20, 20))
        
        lives_text = font_medium.render(f"Lives: {self.player.lives}", True, WHITE)
        screen.blit(lives_text, (SCREEN_WIDTH - lives_text.get_width() - 20, 20))
        
        # Instructions
        instructions = font_small.render("Click on the correct answer!", True, WHITE)
        screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 30))
        
        # Game over screen
        if self.game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            
            game_over_text = font_large.render("Game Over", True, WHITE)
            screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))
            
            final_score = font_medium.render(f"Final Score: {self.player.score}", True, WHITE)
            screen.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2, SCREEN_HEIGHT // 2))
            
            restart_text = font_medium.render("Press ENTER to play again", True, WHITE)
            screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    # Main game loop
    while True:
        game.handle_events()
        if not game.game_over:
            game.update()
        game.draw()
        clock.tick(60)

if __name__ == "__main__":
    main()
        