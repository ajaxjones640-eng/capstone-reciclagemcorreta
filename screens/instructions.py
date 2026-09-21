import pygame

from config import (
    BG_DARK,
    TEXT_ON_DARK,
    MUTED_ON_DARK,
    BLUE,
    RED,
    GLASS_GREEN,
    YELLOW,
    HEART_COLOR,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_ITEM,
)
from objects.button import Button
from utils.helpers import draw_heart

TOPICS = [
    (BLUE, "PAPEL", "Jornais, folhas, papelão e caixas."),
    (RED, "PLÁSTICO", "Garrafas, embalagens e sacolas."),
    (GLASS_GREEN, "VIDRO", "Potes, garrafas e frascos de vidro."),
    (YELLOW, "METAL", "Latas de alumínio e de aço."),
]


class InstructionsScreen:
    """Tela que explica como jogar (tema escuro)."""

    def __init__(self):
        self.back_button = Button(
            (25, 25, 130, 42),
            "← Menu",
            color=(27, 28, 23),
            text_color=TEXT_ON_DARK,
            border_color=(45, 46, 40),
            hover_color=(40, 42, 34),
            shadow=False
        )

    # Processa um evento e devolve "menu" para voltar, ou None
    def handle_event(self, event):
        if self.back_button.clicked(event):
            return "menu"

        return None

    # Desenha a tela de instruções
    def draw(self, surface):
        width = surface.get_width()

        surface.fill(BG_DARK)

        self.back_button.update(pygame.mouse.get_pos())
        self.back_button.draw(surface)

        title = FONT_TITLE.render("Como jogar", True, TEXT_ON_DARK)
        title_rect = title.get_rect(center=(width // 2, 110))
        surface.blit(title, title_rect)

        subtitle = FONT_SUBTITLE.render(
            "Arraste cada resíduo até o cesto do material correto",
            True,
            MUTED_ON_DARK
        )
        subtitle_rect = subtitle.get_rect(center=(width // 2, 150))
        surface.blit(subtitle, subtitle_rect)

        start_y = 220

        for index, (color, name, description) in enumerate(TOPICS):
            y = start_y + index * 90

            swatch = pygame.Rect(width // 2 - 260, y, 60, 60)
            pygame.draw.rect(surface, color, swatch, border_radius=10)

            name_surface = FONT_ITEM.render(name, True, TEXT_ON_DARK)
            surface.blit(name_surface, (width // 2 - 180, y + 5))

            description_surface = FONT_SUBTITLE.render(
                description, True, MUTED_ON_DARK
            )
            surface.blit(description_surface, (width // 2 - 180, y + 30))

        hearts_y = start_y + len(TOPICS) * 90 + 20

        footer = FONT_SUBTITLE.render(
            "Você tem 3 vidas: cada descarte incorreto tira um coração.",
            True,
            MUTED_ON_DARK
        )
        footer_rect = footer.get_rect(center=(width // 2, hearts_y))
        surface.blit(footer, footer_rect)

        for i in range(3):
            heart_x = width // 2 - 30 + i * 32
            draw_heart(surface, (heart_x, hearts_y + 40), 18, HEART_COLOR)

        footer2 = FONT_SUBTITLE.render(
            "O jogo acaba quando as vidas ou o tempo se esgotam. Boa sorte!",
            True,
            MUTED_ON_DARK
        )
        footer2_rect = footer2.get_rect(center=(width // 2, hearts_y + 66))
        surface.blit(footer2, footer2_rect)
