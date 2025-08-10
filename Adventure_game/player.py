import pygame
from map import can_move  # Import can_move from map.py
import os
from inventory import Inventory
from item import Item

def can_move_rect(rect):
    # Check all four corners of the rect
    from map import can_move
    return (
        can_move(rect.left, rect.top) and
        can_move(rect.right - 1, rect.top) and
        can_move(rect.left, rect.bottom - 1) and
        can_move(rect.right - 1, rect.bottom - 1)
    )

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.colour = (0, 0, 255)
        self.speed = 1
        
        # Health system
        self.max_health = 100
        self.health = self.max_health
        
        # Inventory system
        self.inventory = Inventory(max_slots=20)
        
        # Load player sprite using absolute path
        base_path = os.path.dirname(__file__)
        sprite_path = os.path.join(base_path, "assets", "sprites", "player.png")
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def move(self, keys): #player move keys
        new_rect = self.rect.copy()
        if keys[pygame.K_a]:
            new_rect.x -= self.speed
            if can_move_rect(new_rect):
                self.rect.x -= self.speed
        if keys[pygame.K_d]:
            new_rect.x += self.speed
            if can_move_rect(new_rect):
                self.rect.x += self.speed
        if keys[pygame.K_w]:
            new_rect.y -= self.speed
            if can_move_rect(new_rect):
                self.rect.y -= self.speed
        if keys[pygame.K_s]:
            new_rect.y += self.speed
            if can_move_rect(new_rect):
                self.rect.y += self.speed

    def handle_input(self, event):
        # Handle player input including inventory
        # Handle inventory input
        if self.inventory.handle_input(event):
            return True
        
        # Handle inventory toggle
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.inventory.toggle()
                return True
            elif event.key == pygame.K_TAB:
                self.inventory.toggle()
                return True
            elif event.key == pygame.K_RETURN and self.inventory.is_open:
                # Use selected item
                success, message = self.inventory.use_item(self.inventory.selected_slot, self)
                print(message)  # You could display this in a UI
                return True
        
        return False
    
    def add_item(self, item):
        # Add an item to player's inventory
        return self.inventory.add_item(item)
    
    def has_item(self, item_name):
        # Check if player has a specific item
        return self.inventory.has_item(item_name)
    
    def get_item_count(self, item_name):
        # Get count of a specific item
        return self.inventory.get_item_count(item_name)
    
    def take_damage(self, damage):
        # Take damage and return if player is still alive
        self.health = max(0, self.health - damage)
        return self.health > 0
    
    def heal(self, amount):
        # Heal the player
        self.health = min(self.max_health, self.health + amount)
    
    def is_alive(self):
        # Check if player is alive
        return self.health > 0
    
    def draw(self, screen):
        # Draw the sprite image instead of a rectangle
        screen.blit(self.image, self.rect)
        
        # Draw health bar
        self.draw_health_bar(screen)
        
        # Draw inventory if open
        self.inventory.draw(screen)
    
    def draw_health_bar(self, screen):
        # Draw player health bar
        bar_width = 100
        bar_height = 10
        x = self.rect.x - 25
        y = self.rect.y - 20
        
        # Background
        pygame.draw.rect(screen, (100, 0, 0), (x, y, bar_width, bar_height))
        
        # Health bar
        health_width = int((self.health / self.max_health) * bar_width)
        health_color = (0, 255, 0) if self.health > self.max_health * 0.5 else (255, 255, 0) if self.health > self.max_health * 0.25 else (255, 0, 0)
        pygame.draw.rect(screen, health_color, (x, y, health_width, bar_height))
        
        # Border
        pygame.draw.rect(screen, (255, 255, 255), (x, y, bar_width, bar_height), 2)
        
        # Health text
        font = pygame.font.SysFont("Arial", 8)
        health_text = font.render(f"{self.health}/{self.max_health}", True, (255, 255, 255))
        text_x = x + (bar_width - health_text.get_width()) // 2
        text_y = y + (bar_height - health_text.get_height()) // 2
        screen.blit(health_text, (text_x, text_y))
    
    def save_to_dict(self):
        # Convert player to dictionary for saving
        return {
            'x': self.rect.x,
            'y': self.rect.y,
            'health': self.health,
            'max_health': self.max_health,
            'inventory': self.inventory.save_to_dict()
        }
    
    def load_from_dict(self, data):
        # Load player from dictionary
        self.rect.x = data.get('x', self.rect.x)
        self.rect.y = data.get('y', self.rect.y)
        self.health = data.get('health', self.max_health)
        self.max_health = data.get('max_health', self.max_health)
        self.inventory.load_from_dict(data.get('inventory', {}))