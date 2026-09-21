import sys

import pygame

from config import WIDTH, HEIGHT, FPS
from screens.menu import MenuScreen
from screens.game import GameScreen
from screens.instructions import InstructionsScreen
from screens.game_over import GameOverScreen


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Sort it right!")

    clock = pygame.time.Clock()

    menu_screen = MenuScreen()
    game_screen = GameScreen()
    instructions_screen = InstructionsScreen()
    game_over_screen = GameOverScreen()

    current_screen = "menu"
    running = True

    while running:
        elapsed = pygame.time.get_ticks() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            if current_screen == "menu":
                result = menu_screen.handle_event(event)

                if result == "game":
                    game_screen.start(screen.get_width(), screen.get_height())
                    current_screen = "game"
                elif result == "instructions":
                    current_screen = "instructions"
                elif result == "exit":
                    running = False

            elif current_screen == "game":
                result = game_screen.handle_event(event)

                if result == "menu":
                    current_screen = "menu"

            elif current_screen == "instructions":
                result = instructions_screen.handle_event(event)

                if result == "menu":
                    current_screen = "menu"

            elif current_screen == "game_over":
                result = game_over_screen.handle_event(event)

                if result == "menu":
                    current_screen = "menu"

        if current_screen == "game":
            result = game_screen.update()

            if result == "game_over":
                game_over_screen.set_result(game_screen.score, game_screen.end_reason)
                current_screen = "game_over"

        if current_screen == "menu":
            menu_screen.draw(screen, elapsed)
        elif current_screen == "game":
            game_screen.draw(screen)
        elif current_screen == "instructions":
            instructions_screen.draw(screen)
        elif current_screen == "game_over":
            game_over_screen.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

