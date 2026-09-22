import pygame

from config import WHITE, FONT_SMALL, BLUE, RED, GLASS_GREEN, YELLOW, BROWN
from utils.helpers import draw_recycle_icon, draw_item_icon, load_sprite

BIN_SIZE = 110
BIN_GAP = 22
BIN_BOTTOM_MARGIN = 56

# (tipo, nome exibido, cor de fallback, ícone de fallback, arquivo de sprite)
# A sprite, quando existe, substitui o desenho vetorial (cor + ícone), que
# fica só como reserva para o tipo sem sprite (vidro).
BIN_DEFINITIONS = [
    ("paper", "Papel", BLUE, "sheets", "assets/images/bins/paper.png"),
    ("plastic", "Plástico", RED, "bottle", "assets/images/bins/plastic.png"),
    ("glass", "Vidro", GLASS_GREEN, "bottle", None),
    ("metal", "Metal", YELLOW, "can", "assets/images/bins/metal.png"),
    ("organic", "Orgânico", BROWN, "leaf", "assets/images/bins/organic.png"),
]

# Cor de cada tipo de lixeira (usada para colorir os resíduos sem sprite própria)
BIN_COLORS = {bin_type: color for bin_type, _, color, _, _ in BIN_DEFINITIONS}


class Bin:
    """Uma lixeira de um tipo específico de material.

    Se houver uma sprite para o tipo, ela é desenhada (mantendo a proporção
    original) ocupando a altura do cesto; sem sprite, cai no desenho vetorial
    antigo (retângulo colorido com ícone).
    """

    def __init__(self, bin_type, name, color, icon, sprite_path, size=BIN_SIZE):
        self.type = bin_type
        self.name = name
        self.color = color
        self.icon = icon
        self.rect = pygame.Rect(0, 0, size, size)
        self.sprite = load_sprite(sprite_path)

    # Desenha a lixeira: sprite (se houver) ou o retângulo vetorial de reserva
    def draw(self, surface):
        if self.sprite is not None:
            self._draw_sprite(surface)
        else:
            self._draw_vector(surface)

        label = FONT_SMALL.render(self.name, True, WHITE)
        label_rect = label.get_rect(center=(self.rect.centerx, self.rect.bottom + 14))
        surface.blit(label, label_rect)

    # Desenha a sprite da lixeira, escalada para a altura do cesto,
    # centralizada na base do slot reservado (a imagem é mais alta que larga)
    def _draw_sprite(self, surface):
        rect = self.rect
        sw, sh = self.sprite.get_size()

        height = int(rect.height * 1.55)
        width = int(sw * (height / sh))

        image = pygame.transform.smoothscale(self.sprite, (width, height))
        image_rect = image.get_rect(midbottom=(rect.centerx, rect.bottom))
        surface.blit(image, image_rect)

    # Desenho vetorial de reserva (usado pelo vidro, que não tem sprite)
    def _draw_vector(self, surface):
        rect = self.rect
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


def create_bins():
    """Cria o conjunto de lixeiras (todas visíveis ao mesmo tempo)."""

    return [
        Bin(bin_type, name, color, icon, sprite_path)
        for bin_type, name, color, icon, sprite_path in BIN_DEFINITIONS
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
