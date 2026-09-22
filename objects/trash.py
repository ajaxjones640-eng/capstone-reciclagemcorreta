import random

import pygame

from config import WHITE, DARK, FONT_SMALL
from objects.bin import BIN_COLORS
from utils.helpers import draw_item_icon, load_sprite

ITEM_SIZE = 72
POINTS_PER_ITEM = 10

# Distância (em px) abaixo do ponto de nascimento em que um resíduo recém-criado
# ainda é considerado "perto" do topo, para não nascer um em cima do outro
SPAWN_CLEARANCE = 100

# (tipo da lixeira correta, nome exibido, ícone de reserva, arquivo de sprite)
# Cada tipo pode ter vários resíduos (mais variedade); quando existe sprite,
# ela substitui o cartão colorido + ícone vetorial.
TRASH_CATALOG = [
    # orgânico — os 7 itens da sprite sheet "compost"
    ("organic", "Caixa de Pizza", "leaf", "assets/images/trash/organic_pizza_box.png"),
    ("organic", "Saquinho de Chá", "leaf", "assets/images/trash/organic_tea_bag.png"),
    ("organic", "Abobrinha", "leaf", "assets/images/trash/organic_zucchini.png"),
    ("organic", "Rosquinha", "leaf", "assets/images/trash/organic_donut.png"),
    ("organic", "Cebola", "leaf", "assets/images/trash/organic_onion.png"),
    ("organic", "Casca de Banana", "leaf", "assets/images/trash/organic_banana_peel.png"),
    ("organic", "Casca de Ovo", "leaf", "assets/images/trash/organic_eggshell.png"),
    # demais materiais — um item de cada, escolhido dentro da sprite sheet "recycle"
    ("glass", "Garrafa de Vidro", "bottle", "assets/images/trash/glass_bottle.png"),
    ("paper", "Jornal", "sheets", "assets/images/trash/paper_newspaper.png"),
    ("paper", "Saco de Papel", "sheets", "assets/images/trash/paper_paper_bag.png"),
    ("paper", "Copo de Papel", "sheets", "assets/images/trash/paper_paper_cup.png"),
    ("paper", "Caixa de Leite", "sheets", "assets/images/trash/paper_milk_carton.png"),
    ("plastic", "Galão Plástico", "bottle", "assets/images/trash/plastic_jug.png"),
    ("metal", "Lata de Alumínio", "can", "assets/images/trash/metal_can.png"),
]


class TrashItem:
    """Um resíduo que desce pela esteira e precisa ser arrastado até a lixeira certa."""

    def __init__(self, item_type, name, color, icon, sprite, speed, center):
        self.type = item_type
        self.name = name
        self.color = color
        self.icon = icon
        self.sprite = sprite
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

        self._scaled_sprite = None

        if self.sprite is not None:
            self._scaled_sprite = self._fit_sprite(self.sprite, ITEM_SIZE - 16)

    # Redimensiona a sprite mantendo a proporção, para caber dentro do cartão
    @staticmethod
    def _fit_sprite(sprite, max_side):
        sw, sh = sprite.get_size()
        scale = min(max_side / sw, max_side / sh)

        size = (max(1, int(sw * scale)), max(1, int(sh * scale)))

        return pygame.transform.smoothscale(sprite, size)

    # Faz o resíduo descer um passo pela esteira
    def fall(self):
        self._y += self.speed
        self.rect.y = int(self._y)

    # Move o resíduo (usado no arrasto com o mouse)
    def move_center_to(self, center):
        self.rect.center = center
        self._y = float(self.rect.y)

    # Desenha o resíduo: cartão branco com borda da cor da lixeira correta,
    # com a sprite do item (ou, na falta dela, o ícone vetorial de reserva)
    def draw(self, surface):
        rect = self.rect

        surface.blit(self._shadow, (rect.x, rect.y + 4))

        pygame.draw.rect(surface, WHITE, rect, border_radius=10)
        pygame.draw.rect(surface, self.color, rect, width=3, border_radius=10)

        if self._scaled_sprite is not None:
            sprite_rect = self._scaled_sprite.get_rect(center=rect.center)
            surface.blit(self._scaled_sprite, sprite_rect)
        else:
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

    item_type, name, icon, sprite_path = random.choice(TRASH_CATALOG)
    color = BIN_COLORS[item_type]
    sprite = load_sprite(sprite_path)
    x = _free_spawn_x(active_items, min_x, max_x, y)

    return TrashItem(item_type, name, color, icon, sprite, speed, (x, y))
