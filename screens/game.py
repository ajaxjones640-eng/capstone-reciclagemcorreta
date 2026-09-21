import pygame

from config import (
    WHITE,
    GREEN_DARK,
    GREEN_BG,
    RED,
    DARK,
    YELLOW,
    FONT_PHASE,
    FONT_SCORE,
    FONT_STAR,
    FONT_MESSAGE,
    GAME_DURATION,
)
from objects.button import Button
from objects.bin import create_bins, update_bin_positions, check_bin_collision
from objects.trash import create_trash_items, reset_trash_positions
from utils.helpers import TimedMessage


class GameScreen:
    """Tela de uma fase jogável: arrastar resíduos até os cestos certos."""

    def __init__(self):
        self.back_button = Button((25, 25, 130, 42), "← Menu")

        self.bins = create_bins()
        self.trash_items = create_trash_items()
        self.message = TimedMessage()

        self.score = 0
        self.stars = 3
        self.time_left = GAME_DURATION
        self.start_ticks = 0

        self.dragging_item = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        self.finished = False

    # Reinicia o estado da fase (chamado ao entrar na tela pelo menu)
    def start(self, width, height):
        self.score = 0
        self.stars = 3
        self.time_left = GAME_DURATION
        self.start_ticks = pygame.time.get_ticks()
        self.message = TimedMessage()
        self.dragging_item = None
        self.finished = False

        reset_trash_positions(self.trash_items, width, height)

    # Atualiza o cronômetro da fase
    def _update_timer(self):
        elapsed = (pygame.time.get_ticks() - self.start_ticks) // 1000
        self.time_left = max(0, GAME_DURATION - elapsed)

    # Verifica se todos os resíduos já foram descartados
    def _check_finished(self):
        return all(not item.active for item in self.trash_items)

    # Finaliza o descarte do resíduo, verificando o cesto de destino
    def _drop_item(self, item):
        target_bin = check_bin_collision(item.get_rect(), self.bins)

        if target_bin is None:
            item.reset_position()
            return

        if target_bin.type == item.type:
            item.active = False
            self.score += 100
            self.message.show("Descarte correto!", GREEN_DARK)
        else:
            item.reset_position()
            self.stars = max(0, self.stars - 1)
            self.message.show("Descarte incorreto!", RED)

    # Processa o clique do mouse (início do arrasto ou botão de voltar)
    def _handle_mouse_down(self, event):
        if self.back_button.clicked(event):
            return "menu"

        for item in reversed(self.trash_items):
            if not item.active:
                continue

            rect = item.get_rect()

            if rect.collidepoint(event.pos):
                self.dragging_item = item
                self.drag_offset_x = item.x - event.pos[0]
                self.drag_offset_y = item.y - event.pos[1]
                return None

        return None

    # Processa o movimento do mouse durante o arrasto
    def _handle_mouse_motion(self, event):
        if self.dragging_item is None:
            return

        self.dragging_item.x = event.pos[0] + self.drag_offset_x
        self.dragging_item.y = event.pos[1] + self.drag_offset_y

    # Processa o momento em que o botão do mouse é solto
    def _handle_mouse_up(self):
        if self.dragging_item is not None:
            self._drop_item(self.dragging_item)
            self.dragging_item = None

    # Processa um evento e devolve "menu" se o jogador quiser voltar
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            result = self._handle_mouse_down(event)

            if result == "menu":
                self.dragging_item = None
                return "menu"

        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)

        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_up()

        return None

    # Atualiza o estado da fase a cada quadro
    def update(self):
        self._update_timer()

        if self._check_finished() and not self.finished:
            self.finished = True
            self.message.show("Fase concluída!", GREEN_DARK)

        if self.time_left <= 0 and not self.finished:
            self.finished = True
            self.message.show("Tempo esgotado!", RED)

    # Desenha as estrelas de vida no topo da tela
    def _draw_stars(self, surface):
        for index in range(3):
            x = 40 + index * 42
            y = 75

            color = YELLOW if index < self.stars else (190, 190, 190)

            star = FONT_STAR.render("★", True, color)
            surface.blit(star, (x, y))

    # Desenha o relógio com o tempo restante
    def _draw_timer(self, surface):
        center_x = surface.get_width() - 145
        center_y = 70

        pygame.draw.circle(surface, WHITE, (center_x, center_y), 30)
        pygame.draw.circle(surface, DARK, (center_x, center_y), 30, width=2)

        pygame.draw.line(
            surface,
            DARK,
            (center_x, center_y),
            (center_x, center_y - 16),
            width=3
        )

        pygame.draw.line(
            surface,
            DARK,
            (center_x, center_y),
            (center_x + 11, center_y + 8),
            width=3
        )

        timer_text = FONT_SCORE.render(str(max(0, self.time_left)), True, DARK)
        surface.blit(timer_text, (center_x + 42, center_y - 12))

    # Desenha a tela completa da fase
    def draw(self, surface):
        width = surface.get_width()
        height = surface.get_height()

        surface.fill(GREEN_BG)

        pygame.draw.rect(
            surface,
            (78, 174, 201),
            (0, 0, width, int(height * 0.40))
        )

        self.back_button.update(pygame.mouse.get_pos())
        self.back_button.draw(surface)

        self._draw_stars(surface)

        phase = FONT_PHASE.render("FASE 1", True, DARK)
        phase_rect = phase.get_rect(center=(width - 90, 70))
        surface.blit(phase, phase_rect)

        self._draw_timer(surface)

        update_bin_positions(self.bins, width)

        for bin_data in self.bins:
            bin_data.draw(surface)

        for item in self.trash_items:
            item.draw(surface)

        score_text = FONT_SCORE.render(f"Pontos: {self.score}", True, WHITE)
        surface.blit(score_text, (25, 125))

        self.message.draw(
            surface,
            FONT_MESSAGE,
            center=(width // 2, height - 40)
        )
