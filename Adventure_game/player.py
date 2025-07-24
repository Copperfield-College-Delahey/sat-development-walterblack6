import pygame
from map import can_move  # Import can_move from map.py
import os

class Player:
    def __init__(self, x, y,):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.colour = (0, 0, 255)
        self.speed = 1
        # load player sprite
          sprite_path = os.path.join("assets", "sprite", "player.png")
        self.image = pygame.image.load(sprite_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
    def move(self, keys): #player move keys
        if keys[pygame.K_a] and can_move(self.rect.x - self.speed, self.rect.y):
            self.rect.x -= self.speed
        if keys[pygame.K_d] and can_move(self.rect.x + self.speed, self.rect.y):
            self.rect.x += self.speed
        if keys[pygame.K_w] and can_move(self.rect.x, self.rect.y - self.speed):
            self.rect.y -= self.speed
        if keys[pygame.K_s] and can_move(self.rect.x, self.rect.y + self.speed):
            self.rect.y += self.speed
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)