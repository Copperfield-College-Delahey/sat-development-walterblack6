import pygame
import os

class NPC:
    def __init__(self, x, y, dialogue):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.dialogue = dialogue
        self.spoken = False
        # Load NPC sprite using absolute path
        base_path = os.path.dirname(__file__)
        sprite_path = os.path.join(base_path, "assets", "sprites", "npc.png")
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

    def interact(self, player_rect):
        if self.rect.colliderect(player_rect):
            self.spoken = True
            return self.dialogue
        return None

    def draw(self, screen):
        screen.blit(self.image, self.rect)
