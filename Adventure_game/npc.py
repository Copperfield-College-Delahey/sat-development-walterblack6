import pygame

class NPC:
    def __init__(self, x, y, dialogue):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.colour = (255, 165, 0)
        self.dialogue = dialogue
        self.spoken = False

    def interact(self, player_rect):
        if self.rect.colliderect(player_rect):
            self.spoken = True
            return self.dialogue
        return None

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, self.rect)
