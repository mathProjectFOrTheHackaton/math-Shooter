import pygame
from constants import *

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