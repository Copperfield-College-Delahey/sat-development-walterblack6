import pygame
import os

class Item:
    def __init__(self, name, description, item_type, stackable=False, max_stack=1, image_path=None):
        self.name = name
        self.description = description
        self.item_type = item_type  # "weapon", "armor", "consumable", "key"
        self.stackable = stackable
        self.max_stack = max_stack
        self.quantity = 1
        
        # Load image if provided
        self.image = None
        if image_path:
            try:
                base_path = os.path.dirname(__file__)
                full_path = os.path.join(base_path, "assets", "sprites", image_path)
                if os.path.exists(full_path):
                    self.image = pygame.image.load(full_path).convert_alpha()
                    self.image = pygame.transform.scale(self.image, (32, 32))
            except:
                print(f"Could not load image: {image_path}")
    
    def use(self, player):
        #Use the item on the player
        if self.item_type == "consumable":
            return self.use_consumable(player)
        elif self.item_type == "key":
            return self.use_key(player)
        return False
    
    def use_consumable(self, player):
        #Use a consumable item (health potion, etc.)
        if self.name.lower() == "health potion":
            if hasattr(player, 'health'):
                player.health = min(player.max_health, player.health + 20)
                return True
        return False
    
    def use_key(self, player):
        #Use a key item
        # This would be implemented based on specific doors/chests
        return True
    
    def can_stack_with(self, other_item):
        #Check if this item can stack with another item
        return (self.stackable and 
                other_item.stackable and 
                self.name == other_item.name and 
                self.item_type == other_item.item_type)
    
    def add_to_stack(self, amount=1):
        #Add items to the stack
        if self.stackable:
            self.quantity = min(self.quantity + amount, self.max_stack)
            return True
        return False
    
    def remove_from_stack(self, amount=1):
        #Remove items from the stack
        if self.stackable and self.quantity >= amount:
            self.quantity -= amount
            return True
        return False
    
    def is_empty(self):
        #Check if the stack is empty
        return self.quantity <= 0
    
    def get_display_name(self):
        #Get the display name with quantity if stackable
        if self.stackable and self.quantity > 1:
            return f"{self.name} (x{self.quantity})"
        return self.name
    
    def draw(self, screen, x, y, size=32):
        #Draw the item at the specified position
        if self.image:
            scaled_image = pygame.transform.scale(self.image, (size, size))
            screen.blit(scaled_image, (x, y))
        else:
            # Draw a placeholder rectangle
            pygame.draw.rect(screen, (128, 128, 128), (x, y, size, size))
            pygame.draw.rect(screen, (64, 64, 64), (x, y, size, size), 2)
    
    def __str__(self):
        return self.get_display_name()
    
    def __repr__(self):
        return f"Item('{self.name}', '{self.description}', '{self.item_type}')"


# Predefined items for the game
def create_health_potion():
    return Item("Health Potion", "Restores 20 health points", "consumable", True, 10, "potion.png")

def create_sword():
    return Item("Iron Sword", "A basic iron sword", "weapon", False, 1, "sword.png")

def create_key():
    return Item("Old Key", "An old rusty key", "key", False, 1, "key.png")

def create_armor():
    return Item("Leather Armor", "Basic leather armor", "armor", False, 1, "armor.png")
