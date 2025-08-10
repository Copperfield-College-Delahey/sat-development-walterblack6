import pygame

class Button:
    def __init__(self, x, y, width, height, text, font_size=40, color=(255, 255, 255), 
                 hover_color=(200, 200, 200), text_color=(0, 0, 0), hover_text_color=(50, 50, 50)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.hover_text_color = hover_text_color
        self.is_hovered = False
        self.font = pygame.font.SysFont("Arial", font_size)
        
    def draw(self, screen):
        # Draw button background
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect)
        pygame.draw.rect(screen, (100, 100, 100), self.rect, 2)  # Border
        
        # Draw text
        text_color = self.hover_text_color if self.is_hovered else self.text_color
        text_surface = self.font.render(self.text, True, text_color)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False
    
    def update(self, mouse_pos):
        self.is_hovered = self.rect.collidepoint(mouse_pos)
