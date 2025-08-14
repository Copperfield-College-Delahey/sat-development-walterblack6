import pygame
import random
from typing import Tuple, Optional

class CombatSystem:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.is_player_turn = True
        self.combat_active = True
        self.message = ""
        self.selected_item = None
        # New variables for item menu
        self.show_item_menu = False
        self.selected_item_index = 0
        self.items_per_row = 5
        self.item_slot_size = 50
        self.item_padding = 10
        
        # Victory screen variables
        self.victory_screen = False
        self.victory_timer = 0
        self.VICTORY_DURATION = 180  # 3 seconds at 60 FPS

        # Combat UI dimensions
        self.combat_width = 1200
        self.combat_height = 800
        self.combat_x = (1500 - self.combat_width) // 2
        self.combat_y = (1000 - self.combat_height) // 2
        self.message_y = self.combat_y + 250  # New position for combat messages
    
    def start_combat(self) -> None:
        # Initialize combat state
        self.combat_active = True
        self.is_player_turn = True
        self.message = "Combat started! Select an action!"
    
    def player_attack(self) -> Tuple[int, str]:
        # Basic player attack
        # Check if player has equipped weapon
        base_damage = 15  # Base damage without weapon
        weapon = self.player.get_equipped_weapon()
        
        if weapon:
            base_damage += 10  # Additional damage with equipped weapon
            message = f"You attack with your {weapon.name}!"
        else:
            message = "You attack with your bare hands!"
        
        # Add some randomness
        damage = random.randint(base_damage - 5, base_damage + 5)
        
        self.enemy.take_damage(damage)
        return damage, f"{message} You dealt {damage} damage!"
    
    def enemy_attack(self) -> Tuple[int, str]:
        # Enemy attack turn with armor reduction
        base_damage = random.randint(8, 15)
        
        # Get player's defense from armor
        defense = self.player.get_total_defense()
        
        # Reduce damage by defense (minimum 1 damage)
        damage = max(1, base_damage - defense)
        
        # Get armor name for message if equipped
        armor = self.player.get_equipped_armor()
        if armor:
            message = f"Your {armor.name} absorbs {defense} damage!"
        else:
            message = "You have no armor to protect you!"
        
        self.player.take_damage(damage)
        return damage, f"Enemy attacks! {message} You take {damage} damage!"

    def use_item(self, item_index: int) -> Tuple[bool, str]:
        # Use an item during combat
        success, message = self.player.inventory.use_item(item_index, self.player)
        return success, message
    
    def process_turn(self, action: str, item_index: Optional[int] = None) -> bool:
        # Process a single turn of combat. Returns True if combat should continue.
        if not self.combat_active:
            return False
            
        if action == "enemy" and not self.is_player_turn:
            # Process enemy turn
            damage, msg = self.enemy_attack()
            self.message = f"{self.message}\n{msg}"
            
            # Check if player is defeated
            if not self.player.is_alive():
                self.combat_active = False
                self.message = "Game Over! You were defeated!"
                return False
                
            # Switch back to player's turn
            self.is_player_turn = True
            return True
            
        if self.is_player_turn:
            # Player's turn
            if action == "attack":
                damage, msg = self.player_attack()
                self.message = msg
                # Check if enemy is defeated after player's attack
                if not self.enemy.is_alive():
                    self.combat_active = False
                    self.victory_screen = True
                    self.victory_timer = 0
                    self.message = "Victory! Enemy defeated!"
                    return True  # Keep combat system active for victory screen
                
                # Switch to enemy turn if enemy is still alive
                self.is_player_turn = False
                
            elif action == "item" and item_index is not None:
                success, msg = self.use_item(item_index)
                self.message = msg
                if not success:
                    return True  # Don't end turn if item use failed
                
                # Switch to enemy turn after successful item use
                self.is_player_turn = False
        
        return True
    
    def draw_equipment_info(self, screen: pygame.Surface, x: int, y: int) -> None:
        # Draw currently equipped items
        font = pygame.font.SysFont("Arial", 18)
        
        weapon = self.player.get_equipped_weapon()
        armor = self.player.get_equipped_armor()
        
        # Draw weapon info
        if weapon:
            weapon_text = f"Weapon: {weapon.name}"
        else:
            weapon_text = "Weapon: None"
        weapon_surface = font.render(weapon_text, True, (200, 200, 200))
        screen.blit(weapon_surface, (x, y))
        
        # Draw armor info
        if armor:
            armor_text = f"Armor: {armor.name}"
        else:
            armor_text = "Armor: None"
        armor_surface = font.render(armor_text, True, (200, 200, 200))
        screen.blit(armor_surface, (x, y + 25))

    def draw_combat_ui(self, screen: pygame.Surface) -> None:
        # Draw the combat interface
        # Draw semi-transparent overlay for full window
        overlay = pygame.Surface((1500, 1000))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw combat box - centered and larger
        pygame.draw.rect(screen, (50, 50, 50), 
                        (self.combat_x, self.combat_y, self.combat_width, self.combat_height))
        pygame.draw.rect(screen, (200, 200, 200), 
                        (self.combat_x, self.combat_y, self.combat_width, self.combat_height), 2)
        
        # Draw health bars
        self._draw_health_bar(screen, self.combat_x + 50, self.combat_y + 50, 
                             self.player.health, self.player.max_health, "Player")
        self._draw_health_bar(screen, self.combat_x + 50, self.combat_y + 100, 
                             self.enemy.health, self.enemy.max_health, "Enemy")
        
        # Draw equipment info
        self.draw_equipment_info(screen, self.combat_x + 50, self.combat_y + 150)
        
        # Draw combat message in center area
        font = pygame.font.SysFont("Arial", 28, bold=True)
        messages = self.message.split('\n')
        for i, msg in enumerate(messages):
            msg_surface = font.render(msg, True, (255, 255, 255))
            msg_rect = msg_surface.get_rect(center=(self.combat_x + self.combat_width // 2, 
                                                  self.message_y + i * 40))
            screen.blit(msg_surface, msg_rect)
        
        # Draw item menu or action buttons
        if self.show_item_menu:
            self.draw_item_menu(screen)
        elif self.is_player_turn:
            self._draw_action_buttons(screen)
        
        # Draw victory screen if active
        if self.victory_screen:
            self.draw_victory_screen(screen)
    
    def draw_item_menu(self, screen: pygame.Surface) -> None:
        # Adjust item menu size and position
        menu_width = 800  # Increased from 500
        menu_height = 400  # Increased from 250
        menu_x = (1500 - menu_width) // 2
        menu_y = (1000 - menu_height) // 2
        
        # Draw semi-transparent overlay for item menu
        pygame.draw.rect(screen, (40, 40, 40), (menu_x, menu_y, menu_width, menu_height))
        pygame.draw.rect(screen, (200, 200, 200), (menu_x, menu_y, menu_width, menu_height), 2)
        
        # Draw title
        font = pygame.font.SysFont("Arial", 24, bold=True)
        title = font.render("Select Item to Use", True, (255, 255, 255))
        title_rect = title.get_rect(center=(menu_x + menu_width // 2, menu_y + 25))
        screen.blit(title, title_rect)
        
        # Draw item slots
        items = self.player.inventory.items
        for i, item in enumerate(items):
            row = i // self.items_per_row
            col = i % self.items_per_row
            
            x = menu_x + self.item_padding + col * (self.item_slot_size + self.item_padding)
            y = menu_y + 60 + row * (self.item_slot_size + self.item_padding)
            
            # Draw slot background
            slot_color = (80, 80, 80) if i == self.selected_item_index else (60, 60, 60)
            pygame.draw.rect(screen, slot_color, (x, y, self.item_slot_size, self.item_slot_size))
            pygame.draw.rect(screen, (120, 120, 120), (x, y, self.item_slot_size, self.item_slot_size), 2)
            
            # Draw item
            item.draw(screen, x + 9, y + 9, 32)
            
            # Draw quantity if stackable
            if item.stackable and item.quantity > 1:
                small_font = pygame.font.SysFont("Arial", 12, bold=True)
                quantity_text = small_font.render(str(item.quantity), True, (255, 255, 255))
                screen.blit(quantity_text, (x + self.item_slot_size - 15, y + 5))
        
        # Draw selected item info
        if items and 0 <= self.selected_item_index < len(items):
            item = items[self.selected_item_index]
            font = pygame.font.SysFont("Arial", 16)
            name_text = font.render(item.name, True, (255, 255, 255))
            desc_text = font.render(item.description, True, (200, 200, 200))
            screen.blit(name_text, (menu_x + 10, menu_y + menu_height - 50))
            screen.blit(desc_text, (menu_x + 10, menu_y + menu_height - 30))
        
        # Draw controls hint
        hint_font = pygame.font.SysFont("Arial", 14)
        hint_text = hint_font.render("Arrow keys to select, Enter to use, Esc to cancel", True, (150, 150, 150))
        screen.blit(hint_text, (menu_x + 10, menu_y + menu_height - 20))

    def draw_victory_screen(self, screen: pygame.Surface) -> None:
        # Draw semi-transparent dark overlay for full window
        overlay = pygame.Surface((1500, 1000))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Create a victory box
        victory_width = 800
        victory_height = 500
        victory_x = (1500 - victory_width) // 2
        victory_y = (1000 - victory_height) // 2
        
        # Draw victory box with border
        pygame.draw.rect(screen, (50, 50, 50), (victory_x, victory_y, victory_width, victory_height))
        pygame.draw.rect(screen, (255, 215, 0), (victory_x, victory_y, victory_width, victory_height), 3)
        
        # Draw victory banner
        font = pygame.font.SysFont("Arial", 72, bold=True)
        title = font.render("VICTORY!", True, (255, 215, 0))  # Gold color
        title_rect = title.get_rect(center=(750, victory_y + 80))
        screen.blit(title, title_rect)
        
        # Draw boss defeated message
        font = pygame.font.SysFont("Arial", 36)
        msg = font.render(f"You have defeated the {self.enemy.name}!", True, (255, 255, 255))
        msg_rect = msg.get_rect(center=(750, victory_y + 180))
        screen.blit(msg, msg_rect)
        
        # Draw battle stats
        font = pygame.font.SysFont("Arial", 24)
        stats = [
            f"Your remaining health: {self.player.health}/{self.player.max_health}",
            f"Equipped weapon: {self.player.get_equipped_weapon().name if self.player.get_equipped_weapon() else 'None'}",
            f"Equipped armor: {self.player.get_equipped_armor().name if self.player.get_equipped_armor() else 'None'}"
        ]
        
        for i, stat in enumerate(stats):
            stat_surface = font.render(stat, True, (200, 200, 200))
            stat_rect = stat_surface.get_rect(center=(750, victory_y + 250 + i * 40))
            screen.blit(stat_surface, stat_rect)
        
        # Draw decorative elements
        pygame.draw.line(screen, (255, 215, 0), 
                        (victory_x + 50, victory_y + 140),
                        (victory_x + victory_width - 50, victory_y + 140), 2)
        
        # Draw continue prompt with blinking effect
        if self.victory_timer > 60:  # Start showing after 1 second
            if (self.victory_timer // 30) % 2 == 0:  # Blink every half second
                font = pygame.font.SysFont("Arial", 24)
                prompt = font.render("Press SPACE to continue...", True, (255, 255, 255))
                prompt_rect = prompt.get_rect(center=(750, victory_y + victory_height - 50))
                screen.blit(prompt, prompt_rect)

    def _draw_health_bar(self, screen: pygame.Surface, x: int, y: int, 
                        current: int, maximum: int, label: str) -> None:
        # Draw a health bar with label
        font = pygame.font.SysFont("Arial", 20)
        label_surface = font.render(f"{label}: {current}/{maximum}", True, (255, 255, 255))
        screen.blit(label_surface, (x, y))
        
        bar_width = 200
        bar_height = 20
        health_percent = current / maximum
        
        # Background
        pygame.draw.rect(screen, (100, 0, 0), (x, y + 25, bar_width, bar_height))
        # Health
        pygame.draw.rect(screen, (0, 255, 0), 
                        (x, y + 25, int(bar_width * health_percent), bar_height))
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (x, y + 25, bar_width, bar_height), 2)
    
    def _draw_action_buttons(self, screen: pygame.Surface) -> None:
        # Define button dimensions
        button_width = 200
        button_height = 60
        button_spacing = 50
        
        # Calculate starting position for first button (centered at bottom of combat box)
        total_width = (button_width * 3) + (button_spacing * 2)
        start_x = self.combat_x + (self.combat_width - total_width) // 2
        button_y = self.combat_y + self.combat_height - 100
        
        buttons = [
            ("Attack", (start_x, button_y, button_width, button_height)),
            ("Use Item", (start_x + button_width + button_spacing, button_y, button_width, button_height)),
            ("Run", (start_x + (button_width + button_spacing) * 2, button_y, button_width, button_height))
        ]
        
        for text, rect in buttons:
            # Draw button background with gradient effect
            pygame.draw.rect(screen, (80, 80, 80), rect)
            pygame.draw.rect(screen, (120, 120, 120), rect, 2)
            
            # Draw button text
            font = pygame.font.SysFont("Arial", 24, bold=True)
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(rect[0] + rect[2]//2, rect[1] + rect[3]//2))
            screen.blit(text_surface, text_rect)

class Enemy:
    def __init__(self, name: str, health: int, max_health: int):
        self.name = name
        self.health = health
        self.max_health = max_health
        
    def take_damage(self, amount: int) -> None:
        self.health = max(0, self.health - amount)
        
    def is_alive(self) -> bool:
        return self.health > 0