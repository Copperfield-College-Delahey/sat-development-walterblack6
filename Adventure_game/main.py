import pygame
import sys
from player import Player  # import player class
from map import tile_map, draw_map, get_tile, is_chest_opened, mark_chest_opened, regenerate_map, validate_player_position, debug_collision
from npc import NPC
from button import Button
from item import create_health_potion, create_sword, create_key, create_armor
from combat import CombatSystem, Enemy

# Initialize Pygame
pygame.init()

# Set up screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Adventure Quest")
is_fullscreen = False  # Track fullscreen state

paused = False
inventory_open = False  # Track inventory state

# Camera system
camera_x = 0
camera_y = 0

def draw_textbox(screen, text):
    font = pygame.font.SysFont("Arial", 20)
    pygame.draw.rect(screen, (0, 0, 0), (50, 500, 700, 80))  # Draw textbox background
    rendered = font.render(text, True, (255, 255, 255))      # Render text
    screen.blit(rendered, (60, 530))                         # Draw text in box
    
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))
    
def update_camera(player_x, player_y):
    # Update camera position to follow the player
    global camera_x, camera_y
    
    # Calculate the center of the screen
    screen_center_x = WIDTH // 2
    screen_center_y = HEIGHT // 2
    
    # Calculate target camera position to center the player
    target_camera_x = player_x - screen_center_x
    target_camera_y = player_y - screen_center_y
    
    # Clamp camera to map boundaries
    map_width = len(tile_map[0]) * 64  # 25 tiles * 64 pixels
    map_height = len(tile_map) * 64    # 25 tiles * 64 pixels
    
    target_camera_x = max(0, min(target_camera_x, map_width - WIDTH))
    target_camera_y = max(0, min(target_camera_y, map_height - HEIGHT))
    
    # Smooth camera movement (optional - can be adjusted for different feel)
    camera_speed = 0.1
    camera_x += (target_camera_x - camera_x) * camera_speed
    camera_y += (target_camera_y - camera_y) * camera_speed



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
player = Player(192, 192)  # create player instance 

npc1 = NPC(320, 320, "Welcome to the Random Dungeon! Explore the maze, find chests, defeat the boss, and reach the final goal! Press Ctrl+R to generate a new map.") # create npc instance

# Create pause menu buttons
resume_button = Button(300, 200, 200, 50, "Resume")
save_button = Button(300, 260, 200, 50, "Save")
inventory_button = Button(300, 320, 200, 50, "Inventory")
exit_button = Button(300, 380, 200, 50, "Exit")

# store message to display
dialogue_message = "" 
message = ""
map_regenerated = False
regeneration_timer = 0

npc_message_active = False  # track if NPC message is showing
space_was_pressed = False   # track previous space state

# Message system variables
chest_message = ""
chest_message_active = False
last_e_state = False

# Add combat system variable
combat_system = None

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
                if inventory_open:
                    inventory_open = False
                    player.inventory.is_open = False  # Close inventory properly
                else:
                    paused = not paused #toggle pause on/off
            elif event.key == pygame.K_F11:
                is_fullscreen = not is_fullscreen
                if is_fullscreen:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
            elif event.key == pygame.K_r and event.mod & pygame.KMOD_CTRL:  # Ctrl+R to regenerate map
                regenerate_map()
                
                # Debug: Test collision at starting position
                print("Testing collision at starting position...")
                debug_collision(64, 64)
                
                # Find a valid starting position
                start_x, start_y = 64, 64
                if not validate_player_position(start_x, start_y):
                    print(f"Starting position ({start_x}, {start_y}) is invalid, searching for valid position...")
                    # Try to find a valid position near the start
                    for dx in range(-64, 128, 64):
                        for dy in range(-64, 128, 64):
                            test_x = start_x + dx
                            test_y = start_y + dy
                            if validate_player_position(test_x, test_y):
                                start_x, start_y = test_x, test_y
                                print(f"Found valid position: ({start_x}, {start_y})")
                                break
                        else:
                            continue
                        break
                else:
                    print(f"Starting position ({start_x}, {start_y}) is valid")
                
                # Reset player position to valid start
                player.rect.x = start_x
                player.rect.y = start_y
                
                # Reset camera position
                camera_x = 0
                camera_y = 0
                
                # Show regeneration message
                map_regenerated = True
                regeneration_timer = 180  # Show for 3 seconds (60 FPS * 3)

        
        # Handle inventory input
        if inventory_open:
            if player.inventory.handle_input(event):
                continue
        
        # Handle player input (including inventory)
        if not paused and not inventory_open:
            player.handle_input(event)
        
        # Handle pause menu button events
        if paused:
            if resume_button.handle_event(event):
                paused = False
            elif save_button.handle_event(event):
                # TODO: Implement save functionality
                print("Save button clicked!")
            elif inventory_button.handle_event(event):
                # Open inventory from pause menu
                inventory_open = True
                player.inventory.is_open = True  # Ensure inventory is marked as open
                paused = False  # Close pause menu when opening inventory
            elif exit_button.handle_event(event):
                running = False

    # Handle inventory state
    if inventory_open:
        # Update inventory input handling
        mouse_pos = pygame.mouse.get_pos()
        
        # Handle item usage with Enter key
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            if 0 <= player.inventory.selected_slot < len(player.inventory.items):
                success, msg = player.inventory.use_item(player.inventory.selected_slot, player)
                if success:
                    message = msg  # Show success message
                    if "Health Potion" in msg:
                        message = f"Used Health Potion. Health restored to {player.health}/{player.max_health}"
        
        # Update camera to follow player
        update_camera(player.rect.centerx, player.rect.centery)
        
        # Draw the game world in background
        draw_map(screen, None, camera_x, camera_y)
        player.draw(screen, camera_x, camera_y)
        npc1.draw(screen, camera_x, camera_y)
        

        
        # Draw inventory on top
        player.inventory.draw(screen)
        
        pygame.display.flip()
        continue

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

    # Update camera to follow player
    update_camera(player.rect.centerx, player.rect.centery)
    
    # Draw map
    draw_map(screen, None, camera_x, camera_y)

    # Movement
    keys = pygame.key.get_pressed()
    
    # Debug: Check if player is in a valid position
    if not validate_player_position(player.rect.centerx, player.rect.centery):
        print(f"Warning: Player at invalid position ({player.rect.centerx}, {player.rect.centery})")
        # Try to move player to a valid position
        for dx in range(-64, 128, 64):
            for dy in range(-64, 128, 64):
                test_x = player.rect.centerx + dx
                test_y = player.rect.centery + dy
                if validate_player_position(test_x, test_y):
                    player.rect.centerx = test_x
                    player.rect.centery = test_y
                    print(f"Moved player to valid position ({test_x}, {test_y})")
                    break
            else:
                continue
            break
    
    player.move(keys)

    # Draw player
    player.draw(screen, camera_x, camera_y)

    # Draw npc
    npc1.draw(screen, camera_x, camera_y)

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
    keys = pygame.key.get_pressed()
    e_pressed = keys[pygame.K_e] and not last_e_state
    
    if tile_under_player == 2:  # Chest
        player_x, player_y = player.rect.centerx // 64, player.rect.centery // 64
        
        if not chest_message_active:
            if is_chest_opened(player_x, player_y):
                chest_message = "This chest has already been opened."
                chest_message_active = True
            else:
                chest_message = "You found a chest! Press E to open it!"
                if e_pressed:
                    # Get a random item from the chest
                    from map import get_random_item
                    item = get_random_item()
                    
                    success, msg = player.add_item(item)
                    if success:
                        chest_message = f"Chest opened! You found {item.name}! ({item.description})"
                        chest_message_active = True
                        mark_chest_opened(player_x, player_y)
                    else:
                        chest_message = f"{msg}"
                        chest_message_active = True
    elif tile_under_player == 5:  # Boss
        if combat_system is None:
            # Initialize combat with a boss enemy
            boss = Enemy("Dungeon Boss", 100, 100)
            combat_system = CombatSystem(player, boss)
            combat_system.start_combat()
        
        # Draw combat UI
        combat_system.draw_combat_ui(screen)
        
        # Handle combat input only if combat is still active
        if combat_system.combat_active:
            mouse_pos = pygame.mouse.get_pos()
            mouse_click = pygame.mouse.get_pressed()[0]
            
            # Only handle input during player's turn
            if combat_system.is_player_turn:
                # Check for button clicks
                if mouse_click:
                    if 100 <= mouse_pos[0] <= 200 and 450 <= mouse_pos[1] <= 490:
                        # Process player's attack turn
                        combat_system.process_turn("attack")
                    elif 220 <= mouse_pos[0] <= 320 and 450 <= mouse_pos[1] <= 490:
                        # Open inventory for item selection
                        inventory_open = True
                    elif 340 <= mouse_pos[0] <= 440 and 450 <= mouse_pos[1] <= 490:
                        # Try to run from combat
                        combat_system = None
                        player.rect.x -= 64  # Move player away from boss
            else:
                # Process enemy turn after a delay
                pygame.time.wait(500)  # Wait 500ms before enemy attacks
                combat_system.process_turn("enemy")
        else:
            # Combat is over, reset combat system
            if not combat_system.enemy.is_alive():
                combat_system = None
    else:
        # Clear chest message when walking off chest
        chest_message = ""
        chest_message_active = False

    # Update last E key state
    last_e_state = keys[pygame.K_e]

    # Modify the message drawing section to use chest_message
    if dialogue_message:
        draw_textbox(screen, dialogue_message)
    elif chest_message:
        draw_textbox(screen, chest_message)
    elif map_regenerated and regeneration_timer > 0:
        draw_textbox(screen, "New map generated! Explore the new dungeon!")
        regeneration_timer -= 1
        if regeneration_timer <= 0:
            map_regenerated = False

    # Update display
    pygame.display.flip()

# Quit
pygame.quit()
sys.exit()
