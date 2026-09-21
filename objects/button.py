import pygame

from config import LIME, LIME_DARK, WHITE, TEXT, BORDER, FONT_BUTTON


class Button:
    """Botão clicável com efeito de hover e sombra."""

    def __init__(
        self,
        rect,
        text,
        color=WHITE,
        text_color=TEXT,
        border_color=BORDER
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.border_color = border_color
        self.hovered = False

    # Atualiza o estado do botão
    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    # Desenha o botão
    def draw(self, surface):
        rect = self.rect.copy()
        color = self.color
        border = self.border_color

        if self.hovered:
            rect.y -= 2

            if self.color == LIME:
                color = LIME_DARK
                border = LIME_DARK
            else:
                color = (244, 255, 244)
                border = LIME

        shadow = rect.copy()
        shadow.y += 4

        pygame.draw.rect(
            surface,
            (235, 248, 235),
            shadow,
            border_radius=12
        )

        pygame.draw.rect(
            surface,
            color,
            rect,
            border_radius=12
        )

        pygame.draw.rect(
            surface,
            border,
            rect,
            width=2,
            border_radius=12
        )

        text_surface = FONT_BUTTON.render(
            self.text,
            True,
            self.text_color
        )

        text_rect = text_surface.get_rect(
            center=rect.center
        )

        surface.blit(
            text_surface,
            text_rect
        )

    # Verifica se o botão foi clicado
    def clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )
