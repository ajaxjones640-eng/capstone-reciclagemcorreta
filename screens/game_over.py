import pygame

from config import (
    BG_DARK,
    TEXT_ON_DARK,
    MUTED_ON_DARK,
    PRIMARY_GREEN,
    PRIMARY_GREEN_HOVER,
    WHITE,
    FONT_TITLE,
    FONT_SCORE,
    FONT_SUBTITLE,
)
from objects.button import Button


class GameOverScreen:
    """Tela exibida quando uma fase termina (vidas ou tempo esgotados,
    ou todos os resíduos descartados corretamente)."""

    def __init__(self):
        self.score = 0
        self.reason = ""

        self.menu_button = Button(
            (0, 0, 240, 54),
            "Voltar ao menu",
            color=PRIMARY_GREEN,
            text_color=WHITE,
            border_color=PRIMARY_GREEN,
            hover_color=PRIMARY_GREEN_HOVER,
            hover_border_color=PRIMARY_GREEN_HOVER,
            shadow=False
        )

    # Define o resultado da fase que acabou de terminar
    def set_result(self, score, reason):
        self.score = score
        self.reason = reason

    # Processa um evento e devolve "menu" para voltar, ou None
    def handle_event(self, event):
        if self.menu_button.clicked(event):
            return "menu"

        return None

    # Desenha a tela de fim de jogo
    def draw(self, surface):
        width = surface.get_width()
        height = surface.get_height()
        center_x = width // 2

        surface.fill(BG_DARK)

        title = FONT_TITLE.render("Fim de jogo!", True, TEXT_ON_DARK)
        title_rect = title.get_rect(center=(center_x, height // 2 - 100))
        surface.blit(title, title_rect)

        reason = FONT_SUBTITLE.render(self.reason, True, MUTED_ON_DARK)
        reason_rect = reason.get_rect(center=(center_x, height // 2 - 55))
        surface.blit(reason, reason_rect)

        score_label = FONT_SUBTITLE.render("Pontuação final", True, MUTED_ON_DARK)
        score_label_rect = score_label.get_rect(center=(center_x, height // 2 - 5))
        surface.blit(score_label, score_label_rect)

        score_value = FONT_SCORE.render(str(self.score), True, TEXT_ON_DARK)
        score_value_rect = score_value.get_rect(center=(center_x, height // 2 + 25))
        surface.blit(score_value, score_value_rect)

        self.menu_button.rect.center = (center_x, height // 2 + 100)
        self.menu_button.update(pygame.mouse.get_pos())
        self.menu_button.draw(surface)
