import pygame


class TimedMessage:
    """Mensagem temporária exibida na tela por um curto período."""

    def __init__(self, duration_ms=1400):
        self.duration_ms = duration_ms
        self.text = ""
        self.color = (255, 255, 255)
        self.shown_at = 0

    # Define e reinicia a mensagem
    def show(self, text, color):
        self.text = text
        self.color = color
        self.shown_at = pygame.time.get_ticks()

    # Indica se a mensagem ainda deve aparecer na tela
    def is_visible(self):
        if not self.text:
            return False

        return pygame.time.get_ticks() - self.shown_at < self.duration_ms

    # Desenha a mensagem centralizada, se ainda estiver visível
    def draw(self, surface, font, center):
        if not self.is_visible():
            return

        message_surface = font.render(self.text, True, self.color)
        message_rect = message_surface.get_rect(center=center)
        surface.blit(message_surface, message_rect)


def clamp(value, minimum, maximum):
    """Limita um valor a um intervalo [minimum, maximum]."""

    return max(minimum, min(maximum, value))
