import pygame
import sys
import random
import math
from pygame.locals import *

# Initialize pygame blabla
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

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.is_hovered = False
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, 0, 10)
        
        # Border for button
        pygame.draw.rect(surface, WHITE, self.rect, 2, 10)
        
        text_surf = font_medium.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

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
        self.width = 150
        self.height = 100
        self.option_rects = []
        self.update_option_rects()
        self.wrong_answer_clicked = False
        self.wrong_time = 0
        
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

class Menu:
    def __init__(self):
        # Create buttons for difficulty levels
        button_width = 200
        button_height = 60
        center_x = SCREEN_WIDTH // 2
        
        # Calculate positions
        basic_y = SCREEN_HEIGHT // 2 - 80
        intermediate_y = SCREEN_HEIGHT // 2
        advanced_y = SCREEN_HEIGHT // 2 + 80
        start_y = SCREEN_HEIGHT // 2 + 180
        
        # Create buttons
        self.basic_button = Button(center_x - button_width // 2, basic_y, button_width, button_height, "BASIC", BLUE, (100, 100, 255))
        self.intermediate_button = Button(center_x - button_width // 2, intermediate_y, button_width, button_height, "INTERMEDIATE", PURPLE, (180, 100, 255))
        self.advanced_button = Button(center_x - button_width // 2, advanced_y, button_width, button_height, "ADVANCED", RED, (255, 100, 100))
        self.start_button = Button(center_x - button_width // 2, start_y, button_width, button_height, "START GAME", GREEN, (100, 255, 100))
        
        # Default selected level
        self.selected_level = LEVEL_BASIC
        self.basic_button.is_hovered = True
        
    def handle_events(self, events, mouse_pos, mouse_click):
        # Check button hovers
        self.basic_button.check_hover(mouse_pos)
        self.intermediate_button.check_hover(mouse_pos)
        self.advanced_button.check_hover(mouse_pos)
        self.start_button.check_hover(mouse_pos)
        
        # Check button clicks
        if self.basic_button.is_clicked(mouse_pos, mouse_click):
            self.selected_level = LEVEL_BASIC
            return False
            
        if self.intermediate_button.is_clicked(mouse_pos, mouse_click):
            self.selected_level = LEVEL_INTERMEDIATE
            return False
            
        if self.advanced_button.is_clicked(mouse_pos, mouse_click):
            self.selected_level = LEVEL_ADVANCED
            return False
            
        if self.start_button.is_clicked(mouse_pos, mouse_click):
            return True
            
        return False
        
    def draw(self, surface):
        # Draw title
        title_text = font_large.render("MATH SHOOTER", True, WHITE)
        surface.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 100))
        
        # Draw subtitle
        subtitle_text = font_medium.render("Select Difficulty Level", True, WHITE)
        surface.blit(subtitle_text, (SCREEN_WIDTH // 2 - subtitle_text.get_width() // 2, 160))
        
        # Draw level description
        if self.selected_level == LEVEL_BASIC:
            level_text = "Basic: Addition and subtraction with small numbers"
        elif self.selected_level == LEVEL_INTERMEDIATE:
            level_text = "Intermediate: +, -, × with medium-sized numbers"
        else:  # LEVEL_ADVANCED
            level_text = "Advanced: +, -, ×, ÷ with larger numbers"
            
        desc_text = font_small.render(level_text, True, YELLOW)
        surface.blit(desc_text, (SCREEN_WIDTH // 2 - desc_text.get_width() // 2, SCREEN_HEIGHT // 2 + 130))
        
        # Draw buttons
        self.basic_button.draw(surface)
        self.intermediate_button.draw(surface)
        self.advanced_button.draw(surface)
        self.start_button.draw(surface)
        
        # Highlight selected level
        if self.selected_level == LEVEL_BASIC:
            pygame.draw.rect(surface, WHITE, self.basic_button.rect, 4, 10)
        elif self.selected_level == LEVEL_INTERMEDIATE:
            pygame.draw.rect(surface, WHITE, self.intermediate_button.rect, 4, 10)
        else:  # LEVEL_ADVANCED
            pygame.draw.rect(surface, WHITE, self.advanced_button.rect, 4, 10)

class Game:
    def __init__(self):
        self.reset_game()
        self.menu = Menu()
        self.game_state = STATE_MENU
        
    def reset_game(self):
        self.player = Player()
        self.math_problems = []
        self.spawn_timer = 0
        
        # Adjust spawn delay based on level
        self.current_level = LEVEL_BASIC  # Default, will be updated from menu
        self.last_time = pygame.time.get_ticks()
        self.game_over = False
        
    def start_game(self, level):
        self.reset_game()
        self.current_level = level
        
        # Set spawn delay based on level
        if level == LEVEL_BASIC:
            self.spawn_delay = 10000  # 10 seconds
        elif level == LEVEL_INTERMEDIATE:
            self.spawn_delay = 8000   # 8 seconds
        else:  # LEVEL_ADVANCED
            self.spawn_delay = 6000   # 6 seconds
            
        self.game_state = STATE_GAME
        
    def handle_events(self):
        # Handle events common to all game states
        mouse_click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_click = True
                
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # If in game, return to menu
                    if self.game_state == STATE_GAME:
                        self.game_state = STATE_MENU
                    # If in menu, quit game
                    elif self.game_state == STATE_MENU:
                        pygame.quit()
                        sys.exit()
                # Game over - press ENTER to go back to menu
                if (self.game_state == STATE_GAME_OVER or (self.game_state == STATE_GAME and self.game_over)) and event.key == K_RETURN:
                    self.game_state = STATE_MENU
        
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle state-specific events
        if self.game_state == STATE_MENU:
            # Check if Start button was clicked
            if self.menu.handle_events([], mouse_pos, mouse_click):
                self.start_game(self.menu.selected_level)
                
        elif self.game_state == STATE_GAME and not self.game_over:
            # Game state - handle clicking on math problems
            if mouse_click:
                self.handle_game_click(mouse_pos)
    
    def handle_game_click(self, mouse_pos):
        # Check if player clicked on any option
        for problem in self.math_problems:
            if problem.selected or problem.y > SCREEN_HEIGHT:
                continue  # Skip already answered or off-screen problems
                
            for i, rect in enumerate(problem.option_rects):
                if rect.collidepoint(mouse_pos):
                    if i == problem.correct_option_index:
                        problem.selected = True
                        
                        # Award more points for harder levels
                        if self.current_level == LEVEL_BASIC:
                            self.player.score += 10
                        elif self.current_level == LEVEL_INTERMEDIATE:
                            self.player.score += 15
                        else:  # LEVEL_ADVANCED
                            self.player.score += 20
                    else:
                        problem.wrong_answer_clicked = True
                        problem.wrong_time = pygame.time.get_ticks()
                        self.player.lives -= 1
                        if self.player.lives <= 0:
                            self.game_over = True
    
    def update(self):
        if self.game_state != STATE_GAME or self.game_over:
            return
            
        current_time = pygame.time.get_ticks()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # Spawn new math problems
        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_timer = 0
            x = random.randint(100, SCREEN_WIDTH - 100)
            self.math_problems.append(MathProblem(x, -50, self.current_level))
            
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
                        
        # Check if game over, transition to appropriate state
        if self.game_over:
            self.game_state = STATE_GAME_OVER
        
    def draw(self):
        screen.fill(DARK_BLUE)
        
        # Draw background stars
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            size = random.randint(1, 3)
            pygame.draw.circle(screen, WHITE, (x, y), size)
        
        # Draw state-specific elements
        if self.game_state == STATE_MENU:
            self.menu.draw(screen)
            
        elif self.game_state == STATE_GAME or self.game_state == STATE_GAME_OVER:
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
            
            # Draw level indicator
            if self.current_level == LEVEL_BASIC:
                level_text = "BASIC"
                level_color = BLUE
            elif self.current_level == LEVEL_INTERMEDIATE:
                level_text = "INTERMEDIATE"
                level_color = PURPLE
            else:  # LEVEL_ADVANCED
                level_text = "ADVANCED"
                level_color = RED
                
            level_display = font_small.render(f"Level: {level_text}", True, level_color)
            screen.blit(level_display, (SCREEN_WIDTH // 2 - level_display.get_width() // 2, 20))
            
            # Instructions
            instructions = font_small.render("Click on the correct answer!", True, WHITE)
            screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT - 30))
            
            # Game over screen
            if self.game_over:
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
                overlay.fill((0, 0, 0, 180))
                screen.blit(overlay, (0, 0))
                
                game_over_text = font_large.render("Game Over", True, WHITE)
                screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 70))
                
                final_score = font_medium.render(f"Final Score: {self.player.score}", True, WHITE)
                screen.blit(final_score, (SCREEN_WIDTH // 2 - final_score.get_width() // 2, SCREEN_HEIGHT // 2 - 10))
                
                level_result = font_medium.render(f"Level: {level_text}", True, level_color)
                screen.blit(level_result, (SCREEN_WIDTH // 2 - level_result.get_width() // 2, SCREEN_HEIGHT // 2 + 30))
                
                restart_text = font_medium.render("Press ENTER to return to menu", True, WHITE)
                screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 70))
        
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    # Main game loop
    while True:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)

if __name__ == "__main__":
    main() 
