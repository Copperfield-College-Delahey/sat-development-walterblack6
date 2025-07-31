import pygame
from map import can_move  # Import can_move from map.py
import os

def can_move_rect(rect):
    # Check all four corners of the rect
    from map import can_move
    return (
        can_move(rect.left, rect.top) and
        can_move(rect.right - 5, rect.top) and
        can_move(rect.left, rect.bottom - 5) and
        can_move(rect.right - 5, rect.bottom - 5)
    )

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.colour = (0, 0, 255)
        self.speed = 5
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

    def draw(self, screen):
        # Draw the sprite image instead of a rectangle
        screen.blit(self.image, self.rect)