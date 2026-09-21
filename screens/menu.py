import math

import pygame

from config import (
    BG_DARK,
    ICON_BG_DARK,
    BTN_DARK,
    BTN_DARK_HOVER,
    BTN_DARK_BORDER,
    PRIMARY_GREEN,
    PRIMARY_GREEN_HOVER,
    TEXT_ON_DARK,
    MUTED_ON_DARK,
    WHITE,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_SMALL,
    FONT_STAR,
)
from objects.button import Button
from utils.helpers import draw_recycle_icon


class MenuScreen:
    """Tela inicial com o título do jogo e os botões principais (tema escuro)."""

    def __init__(self):
        self.sound_enabled = True

        self.play_button = Button(
            (0, 390, 260, 54),
            "▶  Jogar",
            color=PRIMARY_GREEN,
            text_color=WHITE,
            border_color=PRIMARY_GREEN,
            hover_color=PRIMARY_GREEN_HOVER,
            hover_border_color=PRIMARY_GREEN_HOVER,
            shadow=False
        )

        self.instructions_button = self._secondary_button((0, 454, 260, 54), "ⓘ  Como jogar")
        self.sound_button = self._secondary_button((0, 518, 260, 54), "🔊  Som: ligado")
        self.exit_button = self._secondary_button((0, 582, 260, 54), "×  Sair")

    # Cria um botão no estilo secundário escuro (fundo quase preto, borda sutil)
    @staticmethod
    def _secondary_button(rect, text):
        return Button(
            rect,
            text,
            color=BTN_DARK,
            text_color=TEXT_ON_DARK,
            border_color=BTN_DARK_BORDER,
            hover_color=BTN_DARK_HOVER,
            hover_border_color=BTN_DARK_BORDER,
            shadow=False
        )

    # Processa um evento e devolve a próxima tela ("game", "instructions",
    # "exit") ou None se o menu deve continuar sendo exibido
    def handle_event(self, event):
        if self.play_button.clicked(event):
            return "game"

        if self.instructions_button.clicked(event):
            return "instructions"

        if self.sound_button.clicked(event):
            self.sound_enabled = not self.sound_enabled

            if self.sound_enabled:
                self.sound_button.text = "🔊  Som: ligado"
            else:
                self.sound_button.text = "🔇  Som: desligado"

        if self.exit_button.clicked(event):
            return "exit"

        return None

    # Desenha a tela completa do menu
    def draw(self, surface, elapsed):
        width = surface.get_width()
        height = surface.get_height()

        surface.fill(BG_DARK)

        center_x = width // 2

        offset = math.sin(elapsed * 3) * 5

        icon_center = (center_x, int(135 + offset))

        pygame.draw.circle(surface, ICON_BG_DARK, icon_center, 43)
        draw_recycle_icon(surface, icon_center, 20, WHITE)

        title = FONT_TITLE.render("Sort it right!", True, TEXT_ON_DARK)
        title_rect = title.get_rect(center=(center_x, 215))
        surface.blit(title, title_rect)

        subtitle = FONT_SUBTITLE.render("O jogo de reciclagem", True, MUTED_ON_DARK)
        subtitle_rect = subtitle.get_rect(center=(center_x, 255))
        surface.blit(subtitle, subtitle_rect)

        self.play_button.rect.centerx = center_x
        self.instructions_button.rect.centerx = center_x
        self.sound_button.rect.centerx = center_x
        self.exit_button.rect.centerx = center_x

        mouse_pos = pygame.mouse.get_pos()

        for button in (
            self.play_button,
            self.instructions_button,
            self.sound_button,
            self.exit_button
        ):
            button.update(mouse_pos)
            button.draw(surface)

        footer = FONT_SMALL.render("Use o mouse para jogar", True, MUTED_ON_DARK)
        footer_rect = footer.get_rect(center=(center_x, height - 35))
        surface.blit(footer, footer_rect)
