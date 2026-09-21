<<<<<<< Updated upstream
import streamlit as st

st.set_page_config(
    page_title="Sort it right!",
    page_icon="♻️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------
# CSS
# -------------------------
st.markdown("""
<style>
    /* Fundo geral */
    .stApp {
        background-color: #12130f;
        color: #f2f2f2;
    }

    /* Remove padding padrão */
    .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
        max-width: 100%;
    }

    /* Remove espaço entre elementos */
    div[data-testid="stVerticalBlock"] {
        gap: 0rem;
    }

    /* Coluna central */
    div[data-testid="column"] {
        display: flex;
        flex-direction: column;
        align-items: center;
    }

    /* Ícone */
    .recycle-icon {
        width: 72px;
        height: 72px;
        border-radius: 50%;
        background-color: #17610b;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 130px auto 18px auto;
        font-size: 40px;
        line-height: 1;
    }

    /* Título */
    .title {
        width: 240px;
        font-size: 40px;
        font-weight: 700;
        line-height: 1.1;
        margin: 0 auto 14px auto;
        text-align: center;
        white-space: nowrap;
    }

    /* Subtítulo */
    .subtitle {
        width: 240px;
        color: #c9c9c9;
        font-size: 14px;
        margin: 0 auto 34px auto;
        text-align: center;
    }

    /* Botões */
    div.stButton {
        width: 240px;
        margin: 0 auto;
    }

    div.stButton > button {
        width: 240px;
        height: 54px;
        border-radius: 10px;
        border: 1px solid #2d2e28;
        background-color: #1b1c17;
        color: #eeeeee;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 2px;
        transition: all 0.2s ease;
    }

    div.stButton > button:hover {
        border-color: #5f7838;
        color: white;
        background-color: #22231e;
    }

    /* Botão Jogar */
    div.stButton:first-of-type > button {
        background-color: #98c755;
        color: white;
        border: none;
    }

    div.stButton:first-of-type > button:hover {
        background-color: #a6d564;
        color: white;
    }

    /* Rodapé */
    .footer {
        position: fixed;
        bottom: 55px;
        left: 0;
        width: 100%;
        text-align: center;
        color: #777;
        font-size: 12px;
    }
</style>
""", unsafe_allow_html=True)


# -------------------------
# MENU CENTRAL
# -------------------------
# A coluna central possui exatamente 240px,
# igual à largura dos botões e do conteúdo.
_, col_center, _ = st.columns([1, 240, 1])

with col_center:

    # -------------------------
    # Ícone
    # -------------------------
    st.markdown("""
    <div class="recycle-icon">♻️</div>
    """, unsafe_allow_html=True)

    # -------------------------
    # Título
    # -------------------------
    st.markdown("""
    <div class="title">Sort it right!</div>
    """, unsafe_allow_html=True)

    # -------------------------
    # Subtítulo
    # -------------------------
    st.markdown("""
    <div class="subtitle">O jogo de reciclagem</div>
    """, unsafe_allow_html=True)

    # -------------------------
    # Botão Jogar
    # -------------------------
    if st.button("▶ Jogar", use_container_width=True):
        st.session_state["screen"] = "game"

    # -------------------------
    # Botão Como jogar
    # -------------------------
    if st.button("ⓘ Como jogar", use_container_width=True):
        st.session_state["screen"] = "instructions"

    # -------------------------
    # Botão Som
    # -------------------------
    if st.button("🔊 Som: ligado", use_container_width=True):
        st.session_state["sound"] = not st.session_state.get("sound", True)

    # -------------------------
    # Botão Sair
    # -------------------------
    if st.button("× Sair", use_container_width=True):
        st.session_state["screen"] = "exit"


# -------------------------
# Rodapé
# -------------------------
st.markdown("""
<div class="footer">
    Use as setas para jogar
</div>
""", unsafe_allow_html=True)

# TODO: montar formulários e chamar src.models / src.storage aqui
=======
import sys

import pygame

from config import WIDTH, HEIGHT, FPS
from screens.menu import MenuScreen
from screens.game import GameScreen
from screens.instructions import InstructionsScreen


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Sort it right!")

    clock = pygame.time.Clock()

    menu_screen = MenuScreen()
    game_screen = GameScreen()
    instructions_screen = InstructionsScreen()

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

        if current_screen == "game":
            game_screen.update()

        if current_screen == "menu":
            menu_screen.draw(screen, elapsed)
        elif current_screen == "game":
            game_screen.draw(screen)
        elif current_screen == "instructions":
            instructions_screen.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

>>>>>>> Stashed changes
