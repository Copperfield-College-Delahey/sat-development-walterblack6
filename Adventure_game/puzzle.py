import pygame
import random

class MathPuzzle:
    def __init__(self):
        self.num1 = random.randint(1, 10)
        self.num2 = random.randint(1, 10)
        self.operator = random.choice(['+', '-', '*'])
        self.user_answer = ""
        self.active = True

        if self.operator == '+':
            self.correct_answer = self.num1 + self.num2
        elif self.operator == '-':
            self.correct_answer = self.num1 - self.num2
        else:
            self.correct_answer = self.num1 * self.num2
        
        self.question = f"What is {self.num1} {self.operator} {self.num2}?"

    def handle_input(self, event):
        if not self.active:
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.user_answer = self.user_answer[:-1]
            elif event.unicode.isdigit() or (event.unicode == '-' and not self.user_answer):
                self.user_answer += event.unicode

    def check_answer(self):
        if not self.user_answer:
            return False
        return int(self.user_answer) == self.correct_answer

    def draw(self, screen):
        if not self.active:
            return

        # Create a semi-transparent overlay
        overlay = pygame.Surface((1500, 1000))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        # Puzzle box
        box_width, box_height = 500, 300
        box_x = (1500 - box_width) // 2
        box_y = (1000 - box_height) // 2
        pygame.draw.rect(screen, (30, 30, 30), (box_x, box_y, box_width, box_height))
        pygame.draw.rect(screen, (100, 100, 100), (box_x, box_y, box_width, box_height), 3)

        # Question text
        font = pygame.font.SysFont("Arial", 36)
        question_text = font.render(self.question, True, (255, 255, 255))
        text_rect = question_text.get_rect(center=(box_x + box_width // 2, box_y + 80))
        screen.blit(question_text, text_rect)

        # Answer input box
        input_box_width, input_box_height = 200, 50
        input_box_x = (1500 - input_box_width) // 2
        input_box_y = box_y + 150
        pygame.draw.rect(screen, (80, 80, 80), (input_box_x, input_box_y, input_box_width, input_box_height))
        pygame.draw.rect(screen, (150, 150, 150), (input_box_x, input_box_y, input_box_width, input_box_height), 2)

        # User answer text
        answer_text = font.render(self.user_answer, True, (255, 255, 255))
        answer_rect = answer_text.get_rect(center=(input_box_x + input_box_width // 2, input_box_y + input_box_height // 2))
        screen.blit(answer_text, answer_rect)

        # Instructions
        font_small = pygame.font.SysFont("Arial", 18)
        instructions = font_small.render("Type your answer and press Enter", True, (180, 180, 180))
        inst_rect = instructions.get_rect(center=(box_x + box_width // 2, box_y + box_height - 30))
        screen.blit(instructions, inst_rect)
