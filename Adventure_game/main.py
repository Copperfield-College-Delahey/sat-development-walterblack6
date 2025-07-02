import pygame
import sys
from player import Player #import player class
from map import load_mpy_map, draw_map# map stuff is test code

# Initialize Pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure Quest")

# Set up player
player = Player(375, 275) #create player instance
map_data = load_mpy_map("data/map1.mpy")

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))  # Clear screen
    draw_map(screen, map_data)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

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
