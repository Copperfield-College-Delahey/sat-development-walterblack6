import pygame
from item import Item

class Inventory:
    def __init__(self, max_slots=20):
        self.max_slots = max_slots
        self.items = []
        self.selected_slot = 0
        self.is_open = False
        
        # UI settings
        self.slot_size = 50
        self.slots_per_row = 5
        self.padding = 10
        self.inventory_x = 50
        self.inventory_y = 100
        
    def add_item(self, item):
        #Add an item to the inventory
        if len(self.items) >= self.max_slots:
            return False, "Inventory is full!"
        
        # Check if we can stack with existing items
        for existing_item in self.items:
            if existing_item.can_stack_with(item):
                if existing_item.add_to_stack(item.quantity):
                    return True, f"Added {item.quantity} {item.name} to stack"
                else:
                    return False, f"Cannot add more {item.name} - stack is full"
        
        # If we can't stack, add as new item
        self.items.append(item)
        return True, f"Added {item.name} to inventory"
    
    def remove_item(self, slot_index, amount=1):
        #Remove an item from a specific slot
        if 0 <= slot_index < len(self.items):
            item = self.items[slot_index]
            if item.stackable:
                if item.remove_from_stack(amount):
                    if item.is_empty():
                        self.items.pop(slot_index)
                    return True, f"Removed {amount} {item.name}"
                else:
                    return False, f"Not enough {item.name} to remove"
            else:
                self.items.pop(slot_index)
                return True, f"Removed {item.name}"
        return False, "Invalid slot"
    
    def use_item(self, slot_index, player):
        #Use an item from a specific slot
        if 0 <= slot_index < len(self.items):
            item = self.items[slot_index]
            if item.use(player):
                # Remove the item if it's consumed
                if item.item_type == "consumable":
                    self.remove_item(slot_index, 1)
                return True, f"Used {item.name}"
            else:
                return False, f"Cannot use {item.name}"
        return False, "Invalid slot"
    
    def get_item(self, slot_index):
        #Get item at specific slot
        if 0 <= slot_index < len(self.items):
            return self.items[slot_index]
        return None
    
    def has_item(self, item_name):
        #Check if inventory has a specific item
        for item in self.items:
            if item.name.lower() == item_name.lower():
                return True
        return False
    
    def get_item_count(self, item_name):
        #Get total count of a specific item
        total = 0
        for item in self.items:
            if item.name.lower() == item_name.lower():
                total += item.quantity
        return total
    
    def sort_by_type(self):
        #Sort items by type
        type_order = ["weapon", "armor", "consumable", "key"]
        self.items.sort(key=lambda x: (type_order.index(x.item_type) if x.item_type in type_order else len(type_order), x.name))
    
    def sort_by_name(self):
        #Sort items alphabetically by name
        self.items.sort(key=lambda x: x.name.lower())
    

    
    def clear(self):
        #Clear all items from inventory
        self.items.clear()
    

    
    def toggle(self):
        #Toggle inventory open/closed state
        self.is_open = not self.is_open
    
    def handle_input(self, event):
        #Handle input for inventory navigation
        if not self.is_open:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                self.toggle()
                return True
            elif event.key == pygame.K_TAB:
                self.toggle()
                return True
            elif event.key == pygame.K_LEFT:
                self.selected_slot = max(0, self.selected_slot - 1)
                return True
            elif event.key == pygame.K_RIGHT:
                self.selected_slot = min(len(self.items) - 1, self.selected_slot + 1)
                return True
            elif event.key == pygame.K_UP:
                self.selected_slot = max(0, self.selected_slot - self.slots_per_row)
                return True
            elif event.key == pygame.K_DOWN:
                self.selected_slot = min(len(self.items) - 1, self.selected_slot + self.slots_per_row)
                return True
            elif event.key == pygame.K_RETURN:
                # Use selected item
                return True
        
        return False
    
    def draw(self, screen):
        #Draw the inventory interface
        if not self.is_open:
            return
        
        # Draw background
        inventory_width = self.slots_per_row * self.slot_size + (self.slots_per_row + 1) * self.padding
        inventory_height = ((self.max_slots - 1) // self.slots_per_row + 1) * self.slot_size + ((self.max_slots - 1) // self.slots_per_row + 2) * self.padding + 100
        
        # Semi-transparent background
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Inventory background
        pygame.draw.rect(screen, (50, 50, 50), (self.inventory_x, self.inventory_y, inventory_width, inventory_height))
        pygame.draw.rect(screen, (100, 100, 100), (self.inventory_x, self.inventory_y, inventory_width, inventory_height), 3)
        
        # Draw title
        font = pygame.font.SysFont("Arial", 24, bold=True)
        title = font.render("INVENTORY", True, (255, 255, 255))
        title_rect = title.get_rect(center=(self.inventory_x + inventory_width // 2, self.inventory_y + 20))
        screen.blit(title, title_rect)
        
        # Draw slots
        for i in range(self.max_slots):
            row = i // self.slots_per_row
            col = i % self.slots_per_row
            
            x = self.inventory_x + self.padding + col * (self.slot_size + self.padding)
            y = self.inventory_y + 50 + row * (self.slot_size + self.padding)
            
            # Draw slot background
            slot_color = (80, 80, 80) if i == self.selected_slot else (60, 60, 60)
            pygame.draw.rect(screen, slot_color, (x, y, self.slot_size, self.slot_size))
            pygame.draw.rect(screen, (120, 120, 120), (x, y, self.slot_size, self.slot_size), 2)
            
            # Draw item if exists
            if i < len(self.items):
                item = self.items[i]
                item.draw(screen, x + 9, y + 9, self.slot_size - 18)
                
                # Draw quantity if stackable
                if item.stackable and item.quantity > 1:
                    font = pygame.font.SysFont("Arial", 12, bold=True)
                    quantity_text = font.render(str(item.quantity), True, (255, 255, 255))
                    screen.blit(quantity_text, (x + self.slot_size - 15, y + 5))
        
        # Draw item info
        if 0 <= self.selected_slot < len(self.items):
            selected_item = self.items[self.selected_slot]
            self.draw_item_info(screen, selected_item, self.inventory_x, self.inventory_y + inventory_height + 10)
        
        # Draw controls
        self.draw_controls(screen, self.inventory_x, self.inventory_y + inventory_height + 80)
    
    def draw_item_info(self, screen, item, x, y):
        #Draw detailed information about the selected item
        font = pygame.font.SysFont("Arial", 16)
        title_font = pygame.font.SysFont("Arial", 18, bold=True)
        
        # Item name
        name_text = title_font.render(item.name, True, (255, 255, 255))
        screen.blit(name_text, (x, y))
        
        # Item description
        desc_text = font.render(item.description, True, (200, 200, 200))
        screen.blit(desc_text, (x, y + 25))
        
        # Item type
        type_text = font.render(f"Type: {item.item_type.title()}", True, (180, 180, 180))
        screen.blit(type_text, (x, y + 45))
    
    def draw_controls(self, screen, x, y):
        #Draw control instructions
        font = pygame.font.SysFont("Arial", 14)
        controls = [
            "Controls: Arrow Keys - Navigate | Enter - Use Item | I/Tab - Close",
            f"Items: {len(self.items)}/{self.max_slots}"
        ]
        
        for i, control in enumerate(controls):
            text = font.render(control, True, (150, 150, 150))
            screen.blit(text, (x, y + i * 20))
    
    def save_to_dict(self):
        #Convert inventory to dictionary for saving
        return {
            'max_slots': self.max_slots,
            'items': [
                {
                    'name': item.name,
                    'description': item.description,
                    'item_type': item.item_type,
                    'stackable': item.stackable,
                    'max_stack': item.max_stack,
                    'quantity': item.quantity
                }
                for item in self.items
            ]
        }
    
    def load_from_dict(self, data):
        #Load inventory from dictionary
        self.max_slots = data.get('max_slots', 20)
        self.items = []
        
        for item_data in data.get('items', []):
            item = Item(
                name=item_data['name'],
                description=item_data['description'],
                item_type=item_data['item_type'],
                stackable=item_data['stackable'],
                max_stack=item_data['max_stack']
            )
            item.quantity = item_data['quantity']
            self.items.append(item)
