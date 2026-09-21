import pygame

from config import DARK, WHITE, FONT_ITEM, BLUE, RED, GLASS_GREEN, YELLOW, BROWN


class TrashItem:
    """Um resíduo que o jogador precisa arrastar até o cesto certo."""

    def __init__(self, item_type, name, color, shape, size):
        self.type = item_type
        self.name = name
        self.color = color
        self.shape = shape
        self.size = size
        self.start = (0, 0)
        self.x = 0
        self.y = 0
        self.active = True

    # Cria o retângulo de colisão do resíduo
    def get_rect(self):
        width, height = self.size

        return pygame.Rect(
            int(self.x - width / 2),
            int(self.y - height / 2),
            width,
            height
        )

    # Move o resíduo de volta para a posição inicial
    def reset_position(self):
        self.x, self.y = self.start

    # Desenha o resíduo
    def draw(self, surface):
        if not self.active:
            return

        rect = self.get_rect()
        color = self.color

        if self.shape == "circle":
            radius = min(rect.width, rect.height) // 2

            pygame.draw.circle(
                surface,
                color,
                rect.center,
                radius
            )

            pygame.draw.circle(
                surface,
                DARK,
                rect.center,
                radius,
                width=2
            )

        elif self.shape == "bottle":
            body = rect.copy()

            pygame.draw.rect(
                surface,
                color,
                body,
                border_radius=12
            )

            pygame.draw.rect(
                surface,
                DARK,
                body,
                width=2,
                border_radius=12
            )

            neck = pygame.Rect(
                rect.centerx - 12,
                rect.top - 15,
                24,
                20
            )

            pygame.draw.rect(
                surface,
                color,
                neck,
                border_radius=5
            )

            pygame.draw.rect(
                surface,
                DARK,
                neck,
                width=2,
                border_radius=5
            )

        else:
            pygame.draw.rect(
                surface,
                color,
                rect,
                border_radius=8
            )

            pygame.draw.rect(
                surface,
                DARK,
                rect,
                width=2,
                border_radius=8
            )

        text = FONT_ITEM.render(
            self.name,
            True,
            WHITE
        )

        text_rect = text.get_rect(
            center=rect.center
        )

        surface.blit(
            text,
            text_rect
        )


def create_trash_items():
    """Cria o conjunto padrão de resíduos de uma fase."""

    return [
        TrashItem("paper", "PAPEL", BLUE, "rectangle", (125, 70)),
        TrashItem("plastic", "GARRAFA", RED, "bottle", (80, 125)),
        TrashItem("glass", "VIDRO", GLASS_GREEN, "circle", (95, 95)),
        TrashItem("metal", "LATA", YELLOW, "rectangle", (130, 75)),
        TrashItem("paper", "PAPELÃO", BROWN, "rectangle", (145, 75)),
    ]


def reset_trash_positions(items, width, height):
    """Posiciona os resíduos na base da tela, no início da fase."""

    positions = [
        (width * 0.22, height * 0.72),
        (width * 0.38, height * 0.78),
        (width * 0.53, height * 0.70),
        (width * 0.68, height * 0.78),
        (width * 0.82, height * 0.70)
    ]

    for item, position in zip(items, positions):
        item.start = position
        item.x = position[0]
        item.y = position[1]
        item.active = True
