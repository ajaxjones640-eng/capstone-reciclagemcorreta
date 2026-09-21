import pygame

from config import LIME, LIME_DARK, WHITE, TEXT, BORDER, FONT_BUTTON


class Button:
    """Botão clicável com efeito de hover e sombra.

    As cores de hover e de sombra podem ser customizadas (usado pelo tema
    escuro do protótipo); se não forem informadas, caem no comportamento
    padrão do tema claro original.
    """

    def __init__(
        self,
        rect,
        text,
        color=WHITE,
        text_color=TEXT,
        border_color=BORDER,
        hover_color=None,
        hover_border_color=None,
        shadow_color=(235, 248, 235),
        shadow=True
    ):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.color = color
        self.text_color = text_color
        self.border_color = border_color
        self.shadow_color = shadow_color
        self.shadow = shadow
        self.hovered = False

        if hover_color is not None:
            self.hover_color = hover_color
            self.hover_border_color = (
                hover_border_color
                if hover_border_color is not None
                else hover_color
            )
        else:
            # Comportamento padrão do tema claro original
            if color == LIME:
                self.hover_color = LIME_DARK
                self.hover_border_color = LIME_DARK
            else:
                self.hover_color = (244, 255, 244)
                self.hover_border_color = LIME

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
            color = self.hover_color
            border = self.hover_border_color

        if self.shadow:
            shadow = rect.copy()
            shadow.y += 4

            pygame.draw.rect(
                surface,
                self.shadow_color,
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
