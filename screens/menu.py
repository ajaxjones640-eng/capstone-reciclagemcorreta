import math

import pygame

from config import (
    WHITE,
    LIME,
    GREEN_DARK,
    TEXT_LIGHT,
    FOOTER,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_SMALL,
    FONT_STAR,
)
from objects.button import Button


class MenuScreen:
    """Tela inicial com o título do jogo e os botões principais."""

    def __init__(self):
        self.sound_enabled = True

        self.play_button = Button(
            (0, 390, 260, 54),
            "▶  Jogar",
            color=LIME,
            text_color=WHITE,
            border_color=LIME
        )

        self.instructions_button = Button(
            (0, 454, 260, 54),
            "ⓘ  Como jogar"
        )

        self.sound_button = Button(
            (0, 518, 260, 54),
            "🔊  Som: ligado"
        )

        self.exit_button = Button(
            (0, 582, 260, 54),
            "×  Sair"
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

    # Desenha o fundo com os círculos decorativos
    def _draw_background(self, surface):
        surface.fill(WHITE)

        pygame.draw.circle(
            surface,
            (237, 252, 237),
            (-20, -20),
            210
        )

        pygame.draw.circle(
            surface,
            (240, 253, 240),
            (
                surface.get_width() + 20,
                surface.get_height() + 20
            ),
            175
        )

        pygame.draw.circle(
            surface,
            (249, 255, 249),
            (
                surface.get_width() // 2,
                surface.get_height() // 2
            ),
            330
        )

    # Desenha a tela completa do menu
    def draw(self, surface, elapsed):
        width = surface.get_width()
        height = surface.get_height()

        self._draw_background(surface)

        center_x = width // 2

        offset = math.sin(elapsed * 3) * 5

        icon_x = center_x
        icon_y = 135 + offset

        pygame.draw.circle(
            surface,
            (224, 248, 224),
            (
                icon_x,
                int(icon_y + 8)
            ),
            45
        )

        pygame.draw.circle(
            surface,
            LIME,
            (
                icon_x,
                int(icon_y)
            ),
            43
        )

        icon_surface = FONT_STAR.render(
            "♻",
            True,
            WHITE
        )

        icon_rect = icon_surface.get_rect(
            center=(
                icon_x,
                int(icon_y)
            )
        )

        surface.blit(
            icon_surface,
            icon_rect
        )

        title = FONT_TITLE.render(
            "Sort it right!",
            True,
            GREEN_DARK
        )

        title_rect = title.get_rect(
            center=(
                center_x,
                215
            )
        )

        surface.blit(
            title,
            title_rect
        )

        subtitle = FONT_SUBTITLE.render(
            "O jogo de reciclagem",
            True,
            TEXT_LIGHT
        )

        subtitle_rect = subtitle.get_rect(
            center=(
                center_x,
                255
            )
        )

        surface.blit(
            subtitle,
            subtitle_rect
        )

        self.play_button.rect.centerx = center_x
        self.instructions_button.rect.centerx = center_x
        self.sound_button.rect.centerx = center_x
        self.exit_button.rect.centerx = center_x

        mouse_pos = pygame.mouse.get_pos()

        self.play_button.update(mouse_pos)
        self.instructions_button.update(mouse_pos)
        self.sound_button.update(mouse_pos)
        self.exit_button.update(mouse_pos)

        self.play_button.draw(surface)
        self.instructions_button.draw(surface)
        self.sound_button.draw(surface)
        self.exit_button.draw(surface)

        footer = FONT_SMALL.render(
            "Use o mouse para jogar",
            True,
            FOOTER
        )

        footer_rect = footer.get_rect(
            center=(
                center_x,
                height - 35
            )
        )

        surface.blit(
            footer,
            footer_rect
        )
