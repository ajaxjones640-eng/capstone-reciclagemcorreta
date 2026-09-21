import pygame

from config import DARK, WHITE, FONT_BIN, BLUE, RED, GLASS_GREEN, YELLOW

BIN_WIDTH = 190
BIN_HEIGHT = 180
BIN_GAP = 15
BIN_TOP = 110


class Bin:
    """Um cesto de reciclagem de um tipo específico de material."""

    def __init__(self, bin_type, name, color, size=(BIN_WIDTH, BIN_HEIGHT)):
        self.type = bin_type
        self.name = name
        self.color = color
        self.rect = pygame.Rect(0, 0, *size)

    # Desenha o cesto
    def draw(self, surface):
        rect = self.rect

        pygame.draw.rect(
            surface,
            (35, 35, 35),
            rect,
            border_radius=12
        )

        inner = rect.inflate(-4, -4)

        pygame.draw.rect(
            surface,
            self.color,
            inner,
            border_radius=10
        )

        opening = pygame.Rect(
            rect.x + 35,
            rect.y + 15,
            rect.width - 70,
            30
        )

        pygame.draw.rect(
            surface,
            (25, 80, 45),
            opening,
            border_radius=7
        )

        pygame.draw.rect(
            surface,
            DARK,
            opening,
            width=2,
            border_radius=7
        )

        label = FONT_BIN.render(
            self.name,
            True,
            WHITE
        )

        label_rect = label.get_rect(
            center=(
                rect.centerx,
                rect.centery + 25
            )
        )

        surface.blit(
            label,
            label_rect
        )


def create_bins():
    """Cria o conjunto padrão de cestos de uma fase."""

    return [
        Bin("paper", "PAPEL", BLUE),
        Bin("plastic", "PLÁSTICO", RED),
        Bin("glass", "VIDRO", GLASS_GREEN),
        Bin("metal", "METAL", YELLOW),
    ]


def update_bin_positions(bins, surface_width):
    """Centraliza os cestos horizontalmente na tela."""

    total_width = len(bins) * BIN_WIDTH + (len(bins) - 1) * BIN_GAP
    start_x = (surface_width - total_width) // 2

    for index, bin_data in enumerate(bins):
        bin_data.rect.x = start_x + index * (BIN_WIDTH + BIN_GAP)
        bin_data.rect.y = BIN_TOP


def check_bin_collision(item_rect, bins):
    """Retorna o cesto sob o retângulo informado, se houver."""

    for bin_data in bins:
        if item_rect.colliderect(bin_data.rect):
            return bin_data

    return None
