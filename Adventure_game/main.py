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
is_fullscreen = False  # Track fullscreen state

def draw_textbox(screen, text):
    font = pygame.font.SysFont("Arial", 20)
    pygame.draw.rect(screen, (0, 0, 0), (50, 500, 700, 80))  # Draw textbox background
    rendered = font.render(text, True, (255, 255, 255))      # Render text
    screen.blit(rendered, (60, 530))                         # Draw text in box

# Set up player
player = Player(375, 200)  # create player instance

npc1 = NPC(300, 75, "YOUR 5$ DOLLARS WAS PROMISED TO ME 6000 YEARS AGO") # create npc instance

# store message to display
dialogue_message = "" 
message = ""

npc_message_active = False  # track if NPC message is showing
space_was_pressed = False   # track previous space state

paused = False  # Track pause state

def draw_pause_menu(screen):
    font = pygame.font.SysFont("Arial", 40)
    text = font.render("Paused - Press ESC to resume", True, (255, 255, 255))
    rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, (0, 0, 0), rect.inflate(40, 40))
    screen.blit(text, rect)

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))  # Clear screen

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F11:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
            elif event.key == pygame.K_ESCAPE:
                paused = not paused

    if paused:
        draw_pause_menu(screen)
        pygame.display.flip()
        continue  # Skip game updates while paused

    # Draw map
    draw_map(screen, tile_map)

    # Movement
    keys = pygame.key.get_pressed()
    player.move(keys)

    # Draw player
    player.draw(screen)

    # Draw npc
    npc1.draw(screen)

    # Toggle NPC message on space press (not hold)
    if keys[pygame.K_SPACE] and not space_was_pressed:
        if not npc_message_active:
            npc_message = npc1.interact(player.rect)
            if npc_message:
                dialogue_message = npc_message
                npc_message_active = True
        else:
            dialogue_message = ""
            npc_message_active = False
    space_was_pressed = keys[pygame.K_SPACE]

    # Check tile under player and set message
    tile_under_player = get_tile(player.rect.centerx, player.rect.centery)
    if tile_under_player == 2:  # Chest
        message = "You found a chest with a health potion!"
    elif tile_under_player == 3:  # Goal
        message = "You've reached the exit! Well done!"
    else:
        message = ""

    # Draw textbox if there's a message
    if dialogue_message:
        draw_textbox(screen, dialogue_message)
    elif message:
        draw_textbox(screen, message)

    # Update display
    pygame.display.flip()

# Quit
pygame.quit()
sys.exit()
