import pygame
import sys
from game import Game

def main():
    # Initialize pygame
    pygame.init()
    
    # Create clock for controlling frame rate
    clock = pygame.time.Clock()
    
    # Create game instance
    game = Game()
    
    # Main game loop
    while True:
        game.handle_events()
        game.update()
        game.draw()
        clock.tick(60)  # 60 FPS

if __name__ == "__main__":
    main() 