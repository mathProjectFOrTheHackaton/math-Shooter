import pygame
import random
import sys
from pygame.locals import *
from constants import *
from player import Player
from math_problems import MathProblem
from projectiles import Bullet
from ui import Menu

class Game:
    #point_counter = 0 #to count the points and know what level the player is on
    def __init__(self):
        self.reset_game()
        self.menu = Menu()
        self.game_state = STATE_MENU
        
    def reset_game(self):
        self.player = Player()
        self.math_problems = []
        self.bullets = []
        self.spawn_timer = 0
        self.player_level = 1  # Player progression level (separate from difficulty)
        
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
        
        # Move player with mouse in game state
        if self.game_state == STATE_GAME and not self.game_over:
            self.player.move_to(mouse_pos[0])
        
        # Handle state-specific events
        if self.game_state == STATE_MENU:
            # Check if Start button was clicked
            if self.menu.handle_events([], mouse_pos, mouse_click):
                self.start_game(self.menu.selected_level)
                
        elif self.game_state == STATE_GAME and not self.game_over:
            # Game state - handle clicking on math problem options
            if mouse_click:
                self.handle_game_click(mouse_pos)
    
    def handle_game_click(self, mouse_pos):
        # Check if player clicked on any option
        for problem in self.math_problems:
            if problem.exploding or problem.selected or problem.y > SCREEN_HEIGHT:
                continue  # Skip already answered, exploding, or off-screen problems
                
            for i, rect in enumerate(problem.option_rects):
                if rect.collidepoint(mouse_pos):
                    # Create a bullet
                    self.bullets.append(Bullet(self.player.x, self.player.y - 25, problem.x, problem.y, i))
                    break
    
    def update(self):
        if self.game_state != STATE_GAME or self.game_over:
            return
            
        current_time = pygame.time.get_ticks()
        dt = current_time - self.last_time
        self.last_time = current_time
        
        # Update player level based on score
        if self.player.score // 100 > self.player_level:
            self.current_level +=1 
        
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
        
        # Update bullets
        for bullet in list(self.bullets):
            bullet.update(dt)
            
            # Check if bullet is off-screen
            if bullet.y < 0 or bullet.y > SCREEN_HEIGHT or bullet.x < 0 or bullet.x > SCREEN_WIDTH:
                self.bullets.remove(bullet)
                continue
                
            # Check bullet collisions with problems
            for problem in list(self.math_problems):
                if problem.exploding or problem.selected:
                    continue
                    
                if bullet.check_collision(problem):
                    # Check if correct option
                    if bullet.option_index == problem.correct_option_index:
                        problem.start_explosion()
                        
                        # Award more points for harder levels
                        if self.current_level == LEVEL_BASIC:
                            self.player.score += 10 #counter to track score
                         
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
                

                    # Remove bullet
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    break
                        
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
            # Draw math problems (asteroids)
            for problem in self.math_problems:
                problem.draw(screen)
            
            # Draw bullets
            for bullet in self.bullets:
                bullet.draw(screen)
            
            # Draw player
            self.player.draw(screen)
            
            # Draw HUD
            score_text = font_medium.render(f"Score: {self.player.score}", True, WHITE)
            screen.blit(score_text, (20, 20))

            # Display player progression level
            player_level_text = font_medium.render(f"Player Level: {self.player_level}", True, GREEN)
            screen.blit(player_level_text, (20, 50))
            
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
            instructions = font_small.render("Click on an option to shoot the asteroid!", True, WHITE)
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