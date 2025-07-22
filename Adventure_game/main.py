import pygame
import sys
from player import Player  # import player class
from map import tile_map, draw_map, get_tile

# Initialize Pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure Quest")

# Set up player
player = Player(375, 275)  # create player instance

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw map
    draw_map(screen, tile_map)

    # Movement
    keys = pygame.key.get_pressed()
    player.move(keys)  # use player's move method

    # Draw player
    player.draw(screen)  # use player's draw method

    # Check tile under player
    tile_under_player = get_tile(player.rect.centerx, player.rect.centery)
    if tile_under_player == 2:  # chest
        print("You found a chest!")
    elif tile_under_player == 3:  # goal
        print("You reached the goal!")

    # Update display
    pygame.display.flip()

# Quit
pygame.quit()
sys.exit()
