import pygame
import sys
from player import Player  # import player class
from map import tile_map, draw_map, get_tile
from npc import NPC
# Initialize Pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure Quest")

def draw_textbox(screen, text):
    font = pygame.font.SysFont("Arial", 20)
    pygame.draw.rect(screen, (0, 0, 0), (50, 500, 700, 80)) #draw textbox background
    rendered = font.render(text, True, (255, 255, 255)) #render text
    screen.pygame.Surface.blit(rendered, (60, 530)) #draw text in box

# Set up player
player = Player(375, 275)  # create player instance

npc1 = NPC(300, 200, "SHANE RILE TAN") # create npc instance

dialogue_message = "" # store message to display

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
    
    # Draw npc
    npc1.draw(screen)
    
    #npc interaction
    if keys[pygame.K_SPACE]:
        message = npc1.interact(player.rect)
        if message:
            dialogue_message = message  # Set message to display
            
    
    # Draw textbox if there's a message
    if dialogue_message:
        draw_textbox(screen, dialogue_message)

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
