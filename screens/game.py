import random

import pygame

from config import (
    WIDTH,
    HEIGHT,
    WHITE,
    SKY_BLUE,
    PANEL_DARK,
    HEART_COLOR,
    HEART_EMPTY,
    PRIMARY_GREEN,
    TEXT_ON_DARK,
    MUTED_ON_DARK,
    BTN_DARK,
    BTN_DARK_HOVER,
    BTN_DARK_BORDER,
    FONT_SUBTITLE,
    FONT_SCORE,
    FONT_SMALL,
    FONT_MESSAGE,
    LIVES_INICIAIS,
)
from objects.button import Button
from objects.bin import create_bins, update_bin_positions, check_bin_collision
from objects.trash import spawn_trash_item, ITEM_SIZE, POINTS_PER_ITEM
from utils.helpers import TimedMessage, clamp, draw_heart, draw_recycle_icon

# Esteira no topo da tela, de onde os resíduos nascem
BELT_Y = 190
BELT_HEIGHT = 60
BELT_COLOR = (35, 40, 54)
BELT_ROLLER = (70, 78, 96)

# Quantos resíduos podem estar na tela ao mesmo tempo e de quanto em quanto
# tempo (em quadros) um novo nasce
MAX_ITEMS = 3
SPAWN_MIN_FRAMES = 70
SPAWN_MAX_FRAMES = 130

# Velocidade de queda (px por quadro): aumenta com a pontuação até o limite
BASE_SPEED = 3.2
MAX_SPEED = 7.5
SPEED_PER_POINT = 0.03

MESSAGE_DURATION_MS = 750


class GameScreen:
    """Tela do jogo: a esteira traz vários resíduos ao mesmo tempo em direção
    às lixeiras. O jogador arrasta cada um até a lixeira certa antes que ele
    "caia" sozinho lá embaixo. Errar a lixeira ou deixar o resíduo cair tira
    uma vida (são 3); o jogo termina quando as vidas acabam.

    Mecânica vinda do protótipo "capstone-reciclagemcorreta", adaptada ao
    formato de tela da estrutura (start / handle_event / update / draw).
    """

    def __init__(self):
        self.back_button = Button(
            (25, 25, 130, 42),
            "← Menu",
            color=BTN_DARK,
            text_color=TEXT_ON_DARK,
            border_color=BTN_DARK_BORDER,
            hover_color=BTN_DARK_HOVER,
            shadow=False
        )

        self.width = WIDTH
        self.height = HEIGHT

        self.bins = create_bins()
        update_bin_positions(self.bins, self.width, self.height)

        self.items = []
        self.message = TimedMessage(MESSAGE_DURATION_MS)

        self.score = 0
        self.lives = LIVES_INICIAIS
        self.spawn_timer = 1

        self.dragging_item = None
        self.drag_offset = (0, 0)

        self.finished = False
        self.end_reason = ""

    # Reinicia o estado da partida (chamado ao entrar na tela pelo menu)
    def start(self, width, height):
        self.width = width
        self.height = height
        update_bin_positions(self.bins, width, height)

        self.items = []
        self.message = TimedMessage(MESSAGE_DURATION_MS)

        self.score = 0
        self.lives = LIVES_INICIAIS

        # O primeiro resíduo nasce quase de imediato
        self.spawn_timer = 1

        self.dragging_item = None
        self.finished = False
        self.end_reason = ""

    # Velocidade de queda dos resíduos que nascerem agora
    def _current_speed(self):
        return min(BASE_SPEED + self.score * SPEED_PER_POINT, MAX_SPEED)

    # Faixa horizontal em que um resíduo pode nascer (acima das lixeiras)
    def _spawn_range(self):
        half = ITEM_SIZE // 2

        return (
            self.bins[0].rect.left + half,
            self.bins[-1].rect.right - half
        )

    # Altura a partir da qual o resíduo "cai" sozinho dentro da lixeira
    def _fall_line(self):
        return self.bins[0].rect.top

    # Lixeira sob o item sendo arrastado agora, se houver (usada para saber
    # qual delas destacar/brilhar)
    def _hovered_bin(self):
        if self.dragging_item is None:
            return None

        return check_bin_collision(self.dragging_item.rect, self.bins)

    # Resolve o descarte: acerto soma pontos, erro tira uma vida.
    # Solto fora de uma lixeira, o resíduo simplesmente continua descendo.
    def _drop_item(self, item):
        target_bin = check_bin_collision(item.rect, self.bins)

        if target_bin is None:
            return

        self.items.remove(item)

        if target_bin.type == item.type:
            self.score += POINTS_PER_ITEM
            self.message.show(f"+{POINTS_PER_ITEM} correto!", PRIMARY_GREEN)
        else:
            self.lives = max(0, self.lives - 1)
            self.message.show("Lixeira errada!", HEART_COLOR)

    # Processa o clique do mouse (início do arrasto ou botão de voltar)
    def _handle_mouse_down(self, event):
        if self.back_button.clicked(event):
            return "menu"

        # Pega o resíduo mais "de cima" (desenhado por último) sob o cursor
        for item in reversed(self.items):
            if item.rect.collidepoint(event.pos):
                self.dragging_item = item
                item.set_dragging(True)
                self.drag_offset = (
                    item.rect.centerx - event.pos[0],
                    item.rect.centery - event.pos[1]
                )
                break

        return None

    # Processa o movimento do mouse durante o arrasto
    def _handle_mouse_motion(self, event):
        if self.dragging_item is None:
            return

        self.dragging_item.move_center_to((
            event.pos[0] + self.drag_offset[0],
            event.pos[1] + self.drag_offset[1]
        ))

    # Processa o momento em que o botão do mouse é solto
    def _handle_mouse_up(self):
        if self.dragging_item is None:
            return

        item = self.dragging_item
        self.dragging_item = None
        item.set_dragging(False)

        self._drop_item(item)

    # Cancela o arrasto em andamento (usado ao sair da tela pelo menu/ESC),
    # devolvendo o item ao tamanho e ângulo normais
    def _cancel_drag(self):
        if self.dragging_item is not None:
            self.dragging_item.set_dragging(False)
            self.dragging_item = None

    # Processa um evento e devolve "menu" se o jogador quiser voltar
    def handle_event(self, event):
        if self.finished:
            return None

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._cancel_drag()
            return "menu"

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            result = self._handle_mouse_down(event)

            if result == "menu":
                self._cancel_drag()
                return "menu"

        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self._handle_mouse_up()

        return None

    # Atualiza o estado da partida a cada quadro.
    # Devolve "game_over" quando as vidas acabam.
    def update(self):
        if self.finished:
            return None

        fall_line = self._fall_line()
        half = ITEM_SIZE // 2

        # Avança os resíduos que estão descendo sozinhos pela esteira
        for item in self.items[:]:
            # A inclinação/tamanho do item ao ser arrastado relaxam a cada
            # quadro, então precisam ser atualizados mesmo sem ele se mexer
            item.update_visual()

            if item is self.dragging_item:
                continue

            # Mantém o resíduo dentro da tela se a janela for redimensionada
            item.rect.centerx = clamp(item.rect.centerx, half, self.width - half)

            item.fall()

            if item.rect.top >= fall_line:
                self.items.remove(item)
                self.lives = max(0, self.lives - 1)
                self.message.show("Caiu na lixeira sem separar!", HEART_COLOR)

        # Controla o surgimento de novos resíduos (vários ao mesmo tempo)
        self.spawn_timer -= 1

        if self.spawn_timer <= 0 and len(self.items) < MAX_ITEMS:
            min_x, max_x = self._spawn_range()

            self.items.append(
                spawn_trash_item(
                    self.items,
                    min_x,
                    max_x,
                    BELT_Y + BELT_HEIGHT // 2,
                    self._current_speed()
                )
            )

            self.spawn_timer = random.randint(SPAWN_MIN_FRAMES, SPAWN_MAX_FRAMES)

        if self.lives <= 0:
            self.finished = True
            self._cancel_drag()
            self.end_reason = "Suas vidas acabaram!"
            return "game_over"

        return None

    # Desenha a esteira, com rolos igualmente espaçados
    def _draw_belt(self, surface):
        belt = pygame.Rect(0, BELT_Y, surface.get_width(), BELT_HEIGHT)
        pygame.draw.rect(surface, BELT_COLOR, belt)

        for x in range(24, surface.get_width(), 48):
            pygame.draw.circle(
                surface,
                BELT_ROLLER,
                (x, BELT_Y + BELT_HEIGHT // 2),
                7
            )

    # Desenha o painel de pontos (canto superior esquerdo)
    def _draw_score_panel(self, surface):
        panel = pygame.Rect(16, 16, 170, 56)

        pygame.draw.rect(surface, PANEL_DARK, panel, border_radius=10)
        pygame.draw.rect(surface, (90, 210, 110), panel, width=2, border_radius=10)

        draw_recycle_icon(surface, (panel.left + 26, panel.centery), 16, (90, 210, 110))

        label = FONT_SMALL.render("PONTOS", True, MUTED_ON_DARK)
        surface.blit(label, (panel.left + 50, panel.top + 8))

        value = FONT_SCORE.render(str(self.score), True, TEXT_ON_DARK)
        surface.blit(value, (panel.left + 50, panel.top + 24))

    # Desenha o painel de vidas (canto superior direito)
    def _draw_lives_panel(self, surface):
        width = surface.get_width()
        panel = pygame.Rect(width - 16 - 150, 16, 150, 56)

        pygame.draw.rect(surface, PANEL_DARK, panel, border_radius=10)

        label = FONT_SMALL.render("VIDAS", True, MUTED_ON_DARK)
        surface.blit(label, label.get_rect(midtop=(panel.centerx, panel.top + 8)))

        start_x = panel.centerx - (LIVES_INICIAIS - 1) * 14

        for i in range(LIVES_INICIAIS):
            color = HEART_COLOR if i < self.lives else HEART_EMPTY
            draw_heart(surface, (start_x + i * 28, panel.top + 38), 18, color)

    # Desenha o aviso de acerto/erro sobre um fundo escuro, no meio da queda
    def _draw_feedback(self, surface):
        if not self.message.is_visible():
            return

        text_width, text_height = FONT_MESSAGE.size(self.message.text)

        pill = pygame.Rect(0, 0, text_width + 40, text_height + 20)
        pill.center = (
            surface.get_width() // 2,
            (BELT_Y + BELT_HEIGHT + self._fall_line()) // 2
        )

        pygame.draw.rect(surface, PANEL_DARK, pill, border_radius=10)
        self.message.draw(surface, FONT_MESSAGE, pill.center)

    # Desenha a tela completa do jogo
    def draw(self, surface):
        width = surface.get_width()
        height = surface.get_height()

        # A janela é redimensionável: reposiciona as lixeiras a cada quadro
        self.width = width
        self.height = height
        update_bin_positions(self.bins, width, height)

        surface.fill(SKY_BLUE)

        self._draw_belt(surface)

        hint = FONT_SUBTITLE.render(
            "Arraste cada lixo até a lixeira certa antes que ele caia",
            True,
            WHITE
        )
        surface.blit(hint, hint.get_rect(center=(width // 2, BELT_Y - 22)))

        hovered_bin = self._hovered_bin()

        for bin_data in self.bins:
            bin_data.draw(surface, highlighted=(bin_data is hovered_bin))

        for item in self.items:
            item.draw(surface)

        self._draw_score_panel(surface)
        self._draw_lives_panel(surface)

        self.back_button.rect.bottomleft = (25, height - 25)
        self.back_button.update(pygame.mouse.get_pos())
        self.back_button.draw(surface)

        self._draw_feedback(surface)
