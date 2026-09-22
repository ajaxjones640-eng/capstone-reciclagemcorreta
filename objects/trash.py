import random

import pygame

from config import WHITE, DARK, FONT_SMALL, asset_path
from objects.bin import BIN_COLORS
from utils.helpers import draw_item_icon, load_sprite

ITEM_SIZE = 72
POINTS_PER_ITEM = 10

# Distância (em px) abaixo do ponto de nascimento em que um resíduo recém-criado
# ainda é considerado "perto" do topo, para não nascer um em cima do outro
SPAWN_CLEARANCE = 100

# Efeito visual ao arrastar: o item cresce, se inclina para o lado do
# movimento e "levanta" um pouco da esteira
DRAG_SCALE = 1.18
DRAG_LIFT = 14
DRAG_MAX_TILT = 14
DRAG_TILT_PER_PX = 1.4
TILT_SMOOTHING = 0.35
TILT_DECAY = 0.55

# (tipo da lixeira correta, nome exibido, ícone de reserva, arquivo de sprite)
# Cada tipo pode ter vários resíduos (mais variedade); quando existe sprite,
# ela substitui o cartão colorido + ícone vetorial. Caminho absoluto (via
# asset_path) para funcionar não importa de onde o jogo for executado.
TRASH_CATALOG = [
    # orgânico — os 7 itens da sprite sheet "compost"
    ("organic", "Caixa de Pizza", "leaf", asset_path("images", "trash", "organic_pizza_box.png")),
    ("organic", "Saquinho de Chá", "leaf", asset_path("images", "trash", "organic_tea_bag.png")),
    ("organic", "Abobrinha", "leaf", asset_path("images", "trash", "organic_zucchini.png")),
    ("organic", "Rosquinha", "leaf", asset_path("images", "trash", "organic_donut.png")),
    ("organic", "Cebola", "leaf", asset_path("images", "trash", "organic_onion.png")),
    ("organic", "Casca de Banana", "leaf", asset_path("images", "trash", "organic_banana_peel.png")),
    ("organic", "Casca de Ovo", "leaf", asset_path("images", "trash", "organic_eggshell.png")),
    # demais materiais — um item de cada, escolhido dentro da sprite sheet "recycle"
    ("paper", "Jornal", "sheets", asset_path("images", "trash", "paper_newspaper.png")),
    ("paper", "Saco de Papel", "sheets", asset_path("images", "trash", "paper_paper_bag.png")),
    ("paper", "Copo de Papel", "sheets", asset_path("images", "trash", "paper_paper_cup.png")),
    ("paper", "Caixa de Leite", "sheets", asset_path("images", "trash", "paper_milk_carton.png")),
    ("plastic", "Galão Plástico", "bottle", asset_path("images", "trash", "plastic_jug.png")),
    ("metal", "Lata de Alumínio", "can", asset_path("images", "trash", "metal_can.png")),
]


class TrashItem:
    """Um resíduo que desce pela esteira e precisa ser arrastado até a lixeira certa.

    Ao ser arrastado, o cartão cresce, se inclina na direção do movimento e
    levanta um pouco (efeito de "pegar o objeto"), voltando ao normal assim
    que é solto.
    """

    def __init__(self, item_type, name, color, icon, sprite, speed, center):
        self.type = item_type
        self.name = name
        self.color = color
        self.icon = icon
        self.sprite = sprite
        self.speed = speed
        self.dragging = False

        self.rect = pygame.Rect(0, 0, ITEM_SIZE, ITEM_SIZE)
        self.rect.center = center

        # Posição vertical em float, para a velocidade não ser truncada
        self._y = float(self.rect.y)

        # Inclinação atual e "alvo" (em graus); o alvo decai sozinho quando o
        # mouse para de se mover, fazendo o item se endireitar sozinho
        self._tilt = 0.0
        self._tilt_target = 0.0

        self._card = self._build_card()

    # Monta uma vez o visual do item (fundo, borda e sprite/ícone) numa
    # superfície própria, para poder girar/escalar tudo junto ao arrastar
    def _build_card(self):
        card = pygame.Surface((ITEM_SIZE, ITEM_SIZE), pygame.SRCALPHA)
        card_rect = card.get_rect()

        pygame.draw.rect(card, WHITE, card_rect, border_radius=10)
        pygame.draw.rect(card, self.color, card_rect, width=3, border_radius=10)

        if self.sprite is not None:
            scaled = self._fit_sprite(self.sprite, ITEM_SIZE - 16)
            sprite_rect = scaled.get_rect(center=card_rect.center)
            card.blit(scaled, sprite_rect)
        else:
            draw_item_icon(
                card,
                self.icon,
                card_rect.center,
                self.color,
                scale=card_rect.width / 52
            )

        return card

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

    # Marca o início/fim do arrasto (o fim também zera a inclinação)
    def set_dragging(self, dragging):
        self.dragging = dragging

        if not dragging:
            self._tilt_target = 0.0

    # Move o resíduo (usado no arrasto com o mouse) e atualiza a inclinação
    # alvo de acordo com o quanto ele andou para os lados neste passo
    def move_center_to(self, center):
        dx = center[0] - self.rect.centerx

        target = dx * DRAG_TILT_PER_PX
        self._tilt_target = max(-DRAG_MAX_TILT, min(DRAG_MAX_TILT, target))

        self.rect.center = center
        self._y = float(self.rect.y)

    # Suaviza a inclinação em direção ao alvo e deixa o alvo relaxar de volta
    # a zero (chamado a cada quadro, arrastando ou não)
    def update_visual(self):
        if self._tilt == 0.0 and self._tilt_target == 0.0:
            return

        self._tilt += (self._tilt_target - self._tilt) * TILT_SMOOTHING
        self._tilt_target *= TILT_DECAY

        if abs(self._tilt) < 0.05:
            self._tilt = 0.0

    # Desenha o resíduo: cartão branco com borda da cor da lixeira correta,
    # com a sprite do item (ou, na falta dela, o ícone vetorial de reserva).
    # Enquanto arrastado, o cartão cresce, se inclina e levanta da esteira.
    def draw(self, surface):
        rect = self.rect

        if self.dragging:
            self._draw_dragging(surface)
        else:
            surface.blit(self._shadow_for(rect.width, 4, 60), (rect.x, rect.y + 4))
            surface.blit(self._card, rect.topleft)

        name = FONT_SMALL.render(self.name, True, DARK)
        name_rect = name.get_rect(center=(rect.centerx, rect.top - 14))
        surface.blit(name, name_rect)

    # Desenho especial enquanto o item está sendo arrastado: maior, inclinado
    # e um pouco acima da posição normal, com sombra mais suave por baixo
    def _draw_dragging(self, surface):
        rect = self.rect
        lift_center = (rect.centerx, rect.centery - DRAG_LIFT)

        shadow = self._shadow_for(int(rect.width * DRAG_SCALE), 10, 45)
        shadow_rect = shadow.get_rect(center=(rect.centerx, rect.centery + 6))
        surface.blit(shadow, shadow_rect)

        card = pygame.transform.rotozoom(self._card, -self._tilt, DRAG_SCALE)
        card_rect = card.get_rect(center=lift_center)
        surface.blit(card, card_rect)

    # Sombra simples (retângulo arredondado translúcido) do tamanho pedido;
    # recriada a cada quadro pois o tamanho muda ao arrastar
    @staticmethod
    def _shadow_for(size, radius, alpha):
        shadow = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.rect(
            shadow,
            (0, 0, 0, alpha),
            shadow.get_rect(),
            border_radius=radius
        )
        return shadow


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
