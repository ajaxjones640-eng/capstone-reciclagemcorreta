import pygame

from config import (
    WHITE,
    GREEN_DARK,
    TEXT,
    TEXT_LIGHT,
    BLUE,
    RED,
    GLASS_GREEN,
    YELLOW,
    FONT_TITLE,
    FONT_SUBTITLE,
    FONT_ITEM,
)
from objects.button import Button

TOPICS = [
    (BLUE, "PAPEL", "Jornais, folhas, papelão e caixas."),
    (RED, "PLÁSTICO", "Garrafas, embalagens e sacolas."),
    (GLASS_GREEN, "VIDRO", "Potes, garrafas e frascos de vidro."),
    (YELLOW, "METAL", "Latas de alumínio e de aço."),
]


class InstructionsScreen:
    """Tela que explica como jogar."""

    def __init__(self):
        self.back_button = Button((25, 25, 130, 42), "← Menu")

    # Processa um evento e devolve "menu" para voltar, ou None
    def handle_event(self, event):
        if self.back_button.clicked(event):
            return "menu"

        return None

    # Desenha a tela de instruções
    def draw(self, surface):
        width = surface.get_width()

        surface.fill(WHITE)

        self.back_button.update(pygame.mouse.get_pos())
        self.back_button.draw(surface)

        title = FONT_TITLE.render("Como jogar", True, GREEN_DARK)
        title_rect = title.get_rect(center=(width // 2, 110))
        surface.blit(title, title_rect)

        subtitle = FONT_SUBTITLE.render(
            "Arraste cada resíduo até o cesto do material correto",
            True,
            TEXT_LIGHT
        )
        subtitle_rect = subtitle.get_rect(center=(width // 2, 150))
        surface.blit(subtitle, subtitle_rect)

        start_y = 220

        for index, (color, name, description) in enumerate(TOPICS):
            y = start_y + index * 90

            swatch = pygame.Rect(width // 2 - 260, y, 60, 60)
            pygame.draw.rect(surface, color, swatch, border_radius=10)

            name_surface = FONT_ITEM.render(name, True, TEXT)
            surface.blit(name_surface, (width // 2 - 180, y + 5))

            description_surface = FONT_SUBTITLE.render(
                description, True, TEXT_LIGHT
            )
            surface.blit(description_surface, (width // 2 - 180, y + 30))

        footer = FONT_SUBTITLE.render(
            "Você perde uma estrela a cada descarte incorreto. Boa sorte!",
            True,
            TEXT_LIGHT
        )
        footer_rect = footer.get_rect(center=(width // 2, start_y + len(TOPICS) * 90 + 20))
        surface.blit(footer, footer_rect)
