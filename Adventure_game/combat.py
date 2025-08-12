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
                    self.message = "Victory! Enemy defeated!"
                    return False
                
                # Switch to enemy turn
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
        # Draw semi-transparent overlay
        overlay = pygame.Surface((800, 600))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw combat box
        pygame.draw.rect(screen, (50, 50, 50), (50, 50, 700, 500))
        pygame.draw.rect(screen, (200, 200, 200), (50, 50, 700, 500), 2)
        
        # Draw health bars
        self._draw_health_bar(screen, 100, 100, self.player.health, self.player.max_health, "Player")
        self._draw_health_bar(screen, 100, 150, self.enemy.health, self.enemy.max_health, "Enemy")
        
        # Draw message
        font = pygame.font.SysFont("Arial", 24)
        msg_surface = font.render(self.message, True, (255, 255, 255))
        screen.blit(msg_surface, (100, 400))
        
        # Draw action buttons if it's player's turn
        if self.is_player_turn:
            self._draw_action_buttons(screen)
        
        # Draw equipment info
        self.draw_equipment_info(screen, 100, 200)
    
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
        # Draw combat action buttons
        buttons = [
            ("Attack", (100, 450, 100, 40)),
            ("Use Item", (220, 450, 100, 40)),
            ("Run", (340, 450, 100, 40))
        ]
        
        for text, rect in buttons:
            pygame.draw.rect(screen, (100, 100, 100), rect)
            pygame.draw.rect(screen, (200, 200, 200), rect, 2)
            
            font = pygame.font.SysFont("Arial", 20)
            text_surface = font.render(text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(rect[0] + rect[2]/2, rect[1] + rect[3]/2))
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