import pygame

from config import WHITE, FONT_SMALL, BLUE, RED, GLASS_GREEN, YELLOW, BROWN
from utils.helpers import draw_recycle_icon, draw_item_icon

BIN_SIZE = 110
BIN_GAP = 22
BIN_BOTTOM_MARGIN = 56

# (tipo, nome exibido, cor, ícone do material)
BIN_DEFINITIONS = [
    ("paper", "Papel", BLUE, "sheets"),
    ("plastic", "Plástico", RED, "bottle"),
    ("glass", "Vidro", GLASS_GREEN, "bottle"),
    ("metal", "Metal", YELLOW, "can"),
    ("organic", "Orgânico", BROWN, "leaf"),
]

# Cor de cada tipo de cesto (usada também para colorir os resíduos)
BIN_COLORS = {bin_type: color for bin_type, _, color, _ in BIN_DEFINITIONS}


class Bin:
    """Uma lixeira de um tipo específico de material."""

    def __init__(self, bin_type, name, color, icon, size=BIN_SIZE):
        self.type = bin_type
        self.name = name
        self.color = color
        self.icon = icon
        self.rect = pygame.Rect(0, 0, size, size)

    # Desenha a lixeira, a seta colorida acima dela e o nome abaixo
    def draw(self, surface):
        rect = self.rect

        # Tudo foi desenhado originalmente para uma lixeira de 78 px
        k = rect.width / 78

        arrow_half = int(10 * k)
        arrow_points = [
            (rect.centerx - arrow_half, rect.top - int(26 * k)),
            (rect.centerx + arrow_half, rect.top - int(26 * k)),
            (rect.centerx, rect.top - int(10 * k)),
        ]

        pygame.draw.polygon(surface, self.color, arrow_points)

        pygame.draw.rect(surface, self.color, rect, border_radius=8)

        border_color = tuple(max(c - 30, 0) for c in self.color)
        pygame.draw.rect(surface, border_color, rect, width=3, border_radius=8)

        draw_recycle_icon(
            surface,
            (rect.centerx, rect.top + int(22 * k)),
            int(14 * k),
            WHITE
        )

        draw_item_icon(
            surface,
            self.icon,
            (rect.centerx, rect.bottom - int(20 * k)),
            WHITE,
            scale=0.7 * k
        )

        label = FONT_SMALL.render(self.name, True, WHITE)
        label_rect = label.get_rect(center=(rect.centerx, rect.bottom + 14))
        surface.blit(label, label_rect)


def create_bins():
    """Cria o conjunto de lixeiras (todas visíveis ao mesmo tempo)."""

    return [
        Bin(bin_type, name, color, icon)
        for bin_type, name, color, icon in BIN_DEFINITIONS
    ]


def update_bin_positions(bins, surface_width, surface_height):
    """Centraliza as lixeiras na parte de baixo da tela."""

    total_width = len(bins) * BIN_SIZE + (len(bins) - 1) * BIN_GAP
    start_x = (surface_width - total_width) // 2
    top = surface_height - BIN_SIZE - BIN_BOTTOM_MARGIN

    for index, bin_data in enumerate(bins):
        bin_data.rect.x = start_x + index * (BIN_SIZE + BIN_GAP)
        bin_data.rect.y = top


def check_bin_collision(item_rect, bins):
    """Retorna a lixeira sob o retângulo informado, se houver."""

    for bin_data in bins:
        if item_rect.colliderect(bin_data.rect):
            return bin_data

    return None
