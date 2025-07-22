import pygame
import sys
from player import Player #import player class
from map import tile_map, draw_map
# Initialize Pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure Quest")

# Set up player
player = Player(375, 275) #create player instance

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #draw map
    draw_map(screen, tile_map)
    
    # Movement
    keys = pygame.key.get_pressed()
    player.move(keys) #use players move method

    # Draw player
    player.draw(screen) #use players draw method
    
   

    # Update display
    pygame.display.flip()

# Quit
pygame.quit()
sys.exit()
