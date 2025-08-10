import pygame
import sys
from player import Player  # import player class
from map import tile_map, draw_map, get_tile
from npc import NPC
from button import Button
from item import create_health_potion, create_sword, create_key, create_armor

# Initialize Pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure Quest")
is_fullscreen = False  # Track fullscreen state

paused = False

def draw_textbox(screen, text):
    font = pygame.font.SysFont("Arial", 20)
    pygame.draw.rect(screen, (0, 0, 0), (50, 500, 700, 80))  # Draw textbox background
    rendered = font.render(text, True, (255, 255, 255))      # Render text
    screen.blit(rendered, (60, 530))                         # Draw text in box
    
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    
def draw_paused_menu(screen):
    #draw semi transparent overlay
    overlay = pygame.Surface((800, 600))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    #draw each button
    resume_button.draw(screen)
    save_button.draw(screen)
    inventory_button.draw(screen)
    exit_button.draw(screen)

# Set up player
player = Player(375, 200)  # create player instance

npc1 = NPC(300, 75, "YOUR 5$ DOLLARS WAS PROMISED TO ME 6000 YEARS AGO") # create npc instance

# Create pause menu buttons
resume_button = Button(300, 200, 200, 50, "Resume")
save_button = Button(300, 260, 200, 50, "Save")
inventory_button = Button(300, 320, 200, 50, "Inventory")
exit_button = Button(300, 380, 200, 50, "Exit")

# store message to display
dialogue_message = "" 
message = ""

npc_message_active = False  # track if NPC message is showing
space_was_pressed = False   # track previous space state

# Add some test items to player inventory
player.add_item(create_health_potion())
player.add_item(create_sword())
player.add_item(create_key())

# Game loop
running = True
while running:
    screen.fill((255, 255, 255))  # Clear screen
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                paused = not paused #toggle pause on/off
            elif event.key == pygame.K_F11:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
        
        # Handle player input (including inventory)
        if not paused:
            player.handle_input(event)
        
        # Handle pause menu button events
        if paused:
            if resume_button.handle_event(event):
                paused = False
            elif save_button.handle_event(event):
                # TODO: Implement save functionality
                print("Save button clicked!")
            elif inventory_button.handle_event(event):
                # TODO: Implement inventory functionality
                print("Inventory button clicked!")
            elif exit_button.handle_event(event):
                running = False

    if paused:
        # Update button hover states
        mouse_pos = pygame.mouse.get_pos()
        resume_button.update(mouse_pos)
        save_button.update(mouse_pos)
        inventory_button.update(mouse_pos)
        exit_button.update(mouse_pos)
        
        draw_paused_menu(screen)
        pygame.display.flip()
        continue #skip rest of loop while paused

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
        message = "You found a chest! Press E to open and get a health potion!"
        # Check if player presses E to open chest
        if keys[pygame.K_e]:
            success, msg = player.add_item(create_health_potion())
            if success:
                message = f"Chest opened! {msg}"
            else:
                message = msg
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
