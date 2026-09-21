import math

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


def draw_heart(surface, center, size, color):
    """Desenha um coração simples (usado pelo sistema de vidas)."""

    cx, cy = center
    radius = max(size // 2, 1)

    pygame.draw.circle(
        surface,
        color,
        (cx - radius // 2, cy - radius // 4),
        radius // 2 or 1
    )

    pygame.draw.circle(
        surface,
        color,
        (cx + radius // 2, cy - radius // 4),
        radius // 2 or 1
    )

    pygame.draw.polygon(
        surface,
        color,
        [
            (cx - radius, cy - radius // 6),
            (cx + radius, cy - radius // 6),
            (cx, cy + radius)
        ]
    )


def draw_recycle_icon(surface, center, radius, color):
    """Desenha um símbolo de reciclagem estilizado (3 lâminas em pinwheel)."""

    cx, cy = center

    for i in range(3):
        angle = math.radians(i * 120)
        points = [
            (0, -radius),
            (-radius * 0.42, -radius * 0.2),
            (radius * 0.42, -radius * 0.2)
        ]

        rotated = []

        for px, py in points:
            rx = px * math.cos(angle) - py * math.sin(angle)
            ry = px * math.sin(angle) + py * math.cos(angle)
            rotated.append((cx + rx, cy + ry))

        pygame.draw.polygon(surface, color, rotated)


def draw_item_icon(surface, kind, center, color, scale=1.0):
    """Desenha o ícone simples de um material: garrafa, lata, folha ou papéis."""

    x, y = center

    def box(dx, dy, width, height):
        return pygame.Rect(
            int(x + dx * scale),
            int(y + dy * scale),
            max(int(width * scale), 1),
            max(int(height * scale), 1)
        )

    if kind == "bottle":
        pygame.draw.rect(surface, color, box(-9, -15, 18, 30), border_radius=5)
        pygame.draw.rect(surface, color, box(-4, -23, 8, 9))

    elif kind == "can":
        pygame.draw.rect(surface, color, box(-11, -15, 22, 30), border_radius=3)

    elif kind == "leaf":
        pygame.draw.ellipse(surface, color, box(-13, -9, 26, 18))

    elif kind == "sheets":
        for i in range(3):
            pygame.draw.rect(
                surface,
                color,
                box(-14, -10 + i * 6, 28, 4),
                border_radius=2
            )

    else:
        pygame.draw.circle(
            surface,
            color,
            (int(x), int(y)),
            max(int(15 * scale), 1)
        )
