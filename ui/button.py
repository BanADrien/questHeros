import pygame

class Button:
    def __init__(self, text, pos, size):
        self.rect = pygame.Rect(pos, size)
        self.text = text

    def draw(self, screen, font):
        pygame.draw.rect(screen, (200, 200, 200), self.rect)
        txt = font.render(self.text, True, (0, 0, 0))
        screen.blit(txt, (self.rect.x + 10, self.rect.y + 10))

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN 
            and self.rect.collidepoint(event.pos)
        )
