import random

import pygame

from config import WHITE, DARK, FONT_SMALL
from objects.bin import BIN_COLORS
from utils.helpers import draw_item_icon

ITEM_SIZE = 72
POINTS_PER_ITEM = 10

# Distância (em px) abaixo do ponto de nascimento em que um resíduo recém-criado
# ainda é considerado "perto" do topo, para não nascer um em cima do outro
SPAWN_CLEARANCE = 100

# (tipo da lixeira correta, nome exibido, ícone)
TRASH_CATALOG = [
    ("plastic", "Garrafa Pet", "bottle"),
    ("paper", "Jornal", "sheets"),
    ("glass", "Pote de Vidro", "bottle"),
    ("metal", "Lata de Alumínio", "can"),
    ("organic", "Casca de Banana", "leaf"),
]


class TrashItem:
    """Um resíduo que desce pela esteira e precisa ser arrastado até a lixeira certa."""

    def __init__(self, item_type, name, color, icon, speed, center):
        self.type = item_type
        self.name = name
        self.color = color
        self.icon = icon
        self.speed = speed

        self.rect = pygame.Rect(0, 0, ITEM_SIZE, ITEM_SIZE)
        self.rect.center = center

        # Posição vertical em float, para a velocidade não ser truncada
        self._y = float(self.rect.y)

        self._shadow = pygame.Surface((ITEM_SIZE, ITEM_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(
            self._shadow,
            (0, 0, 0, 60),
            self._shadow.get_rect(),
            border_radius=10
        )

    # Faz o resíduo descer um passo pela esteira
    def fall(self):
        self._y += self.speed
        self.rect.y = int(self._y)

    # Move o resíduo (usado no arrasto com o mouse)
    def move_center_to(self, center):
        self.rect.center = center
        self._y = float(self.rect.y)

    # Desenha o resíduo: cartão branco com borda da cor da lixeira correta
    def draw(self, surface):
        rect = self.rect

        surface.blit(self._shadow, (rect.x, rect.y + 4))

        pygame.draw.rect(surface, WHITE, rect, border_radius=10)
        pygame.draw.rect(surface, self.color, rect, width=3, border_radius=10)

        draw_item_icon(
            surface,
            self.icon,
            rect.center,
            self.color,
            scale=rect.width / 52
        )

        name = FONT_SMALL.render(self.name, True, DARK)
        name_rect = name.get_rect(center=(rect.centerx, rect.top - 14))
        surface.blit(name, name_rect)


def _free_spawn_x(active_items, min_x, max_x, y):
    """Escolhe um x de nascimento evitando sobrepor resíduos que acabaram de nascer."""

    if max_x <= min_x:
        return (min_x + max_x) // 2

    for _ in range(12):
        x = random.randint(min_x, max_x)
        free = True

        for item in active_items:
            near_top = item.rect.top < y + SPAWN_CLEARANCE
            too_close = abs(item.rect.centerx - x) < ITEM_SIZE + 12

            if near_top and too_close:
                free = False
                break

        if free:
            return x

    return random.randint(min_x, max_x)


def spawn_trash_item(active_items, min_x, max_x, y, speed):
    """Cria um resíduo aleatório na esteira, entre min_x e max_x, à altura y."""

    item_type, name, icon = random.choice(TRASH_CATALOG)
    color = BIN_COLORS[item_type]
    x = _free_spawn_x(active_items, min_x, max_x, y)

    return TrashItem(item_type, name, color, icon, speed, (x, y))
