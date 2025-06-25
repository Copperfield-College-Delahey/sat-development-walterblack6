import pygame

class Player:
    def __init__(self, x, y,):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.colour = (0, 0, 255)
        self.speed = 1
    
    def move(self, keys):
        if keys[pygame.K_a]:
            self.rect.x -= self.speed
        if keys[pygame.K_d]:
            self.rect.x += self.speed
        if keys[pygame.K_w]:
            self.rect.y -= self.speed
        if keys[pygame.K_s]:
            self.rect.y += self.speed
        
    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)   