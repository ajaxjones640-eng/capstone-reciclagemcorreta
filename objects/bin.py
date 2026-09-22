import math

import pygame

from config import WHITE, FONT_SMALL, BLUE, RED, YELLOW, BROWN, asset_path
from utils.helpers import draw_recycle_icon, draw_item_icon, load_sprite

BIN_SIZE = 110
BIN_GAP = 22
BIN_BOTTOM_MARGIN = 56

# Quanto a lixeira "respira" (cresce/encolhe) e o quanto o brilho ao redor
# dela pulsa enquanto um resíduo está sendo arrastado por cima
HIGHLIGHT_SCALE = 1.1
GLOW_LAYERS = 4
GLOW_BASE = 16
GLOW_PULSE = 10

# (tipo, nome exibido, cor de fallback, ícone de fallback, arquivo de sprite)
# A sprite, quando existe, substitui o desenho vetorial (cor + ícone); hoje
# todos os tipos têm sprite, então o desenho vetorial fica só como reserva
# caso algum arquivo falte. Caminho absoluto (via asset_path) para funcionar
# não importa de onde o jogo for executado.
BIN_DEFINITIONS = [
    ("paper", "Papel", BLUE, "sheets", asset_path("images", "bins", "paper.png")),
    ("plastic", "Plástico", RED, "bottle", asset_path("images", "bins", "plastic.png")),
    ("metal", "Metal", YELLOW, "can", asset_path("images", "bins", "metal.png")),
    ("organic", "Orgânico", BROWN, "leaf", asset_path("images", "bins", "organic.png")),
]

# Cor de cada tipo de lixeira (usada para colorir os resíduos sem sprite própria)
BIN_COLORS = {bin_type: color for bin_type, _, color, _, _ in BIN_DEFINITIONS}


class Bin:
    """Uma lixeira de um tipo específico de material.

    Se houver uma sprite para o tipo, ela é desenhada (mantendo a proporção
    original) ocupando a altura do cesto; sem sprite, cai no desenho vetorial
    antigo (retângulo colorido com ícone). Quando um resíduo está sendo
    arrastado por cima dela, a lixeira brilha e cresce um pouco, indicando
    que é ali que ele vai cair se for solto.
    """

    def __init__(self, bin_type, name, color, icon, sprite_path, size=BIN_SIZE):
        self.type = bin_type
        self.name = name
        self.color = color
        self.icon = icon
        self.rect = pygame.Rect(0, 0, size, size)
        self.sprite = load_sprite(sprite_path)

    # Desenha a lixeira: sprite (se houver) ou o retângulo vetorial de
    # reserva, com o brilho por trás quando ela é o alvo do arrasto atual
    def draw(self, surface, highlighted=False):
        if highlighted:
            self._draw_glow(surface)

        scale = HIGHLIGHT_SCALE if highlighted else 1.0

        if self.sprite is not None:
            self._draw_sprite(surface, scale)
        else:
            self._draw_vector(surface, scale)

        label = FONT_SMALL.render(self.name, True, WHITE)
        label_rect = label.get_rect(center=(self.rect.centerx, self.rect.bottom + 14))
        surface.blit(label, label_rect)

    # Brilho pulsante atrás da lixeira, na cor dela, enquanto é o alvo do arrasto
    def _draw_glow(self, surface):
        rect = self.rect
        pulse = (math.sin(pygame.time.get_ticks() / 220) + 1) / 2
        extra = GLOW_BASE + pulse * GLOW_PULSE

        base_radius = rect.width * 0.7
        size = int((base_radius + extra) * 2)

        glow = pygame.Surface((size, size), pygame.SRCALPHA)
        center = (size // 2, size // 2)

        for i in range(GLOW_LAYERS, 0, -1):
            radius = int((base_radius + extra) * (i / GLOW_LAYERS))
            alpha = int(65 * (1 - i / GLOW_LAYERS) + 25)
            pygame.draw.circle(glow, (*self.color, alpha), center, radius)

        glow_rect = glow.get_rect(center=rect.center)
        surface.blit(glow, glow_rect)

    # Desenha a sprite da lixeira, escalada para a altura do cesto,
    # centralizada na base do slot reservado (a imagem é mais alta que larga)
    def _draw_sprite(self, surface, scale=1.0):
        rect = self.rect
        sw, sh = self.sprite.get_size()

        height = int(rect.height * 1.55 * scale)
        width = int(sw * (height / sh))

        image = pygame.transform.smoothscale(self.sprite, (width, height))
        image_rect = image.get_rect(midbottom=(rect.centerx, rect.bottom))
        surface.blit(image, image_rect)

    # Desenho vetorial de reserva (usado quando falta a sprite de algum tipo)
    def _draw_vector(self, surface, scale=1.0):
        rect = self.rect.inflate(
            int(self.rect.width * (scale - 1)),
            int(self.rect.height * (scale - 1))
        )
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
