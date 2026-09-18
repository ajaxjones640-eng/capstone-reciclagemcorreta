import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path


# --------------------------------
# Configuração do Streamlit
# --------------------------------

st.set_page_config(
    page_title="Sort it right!",
    page_icon="♻️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# --------------------------------
# Remove elementos visuais do
# Streamlit
# --------------------------------

st.markdown("""
<style>

    /* Remove margem/padding da aplicação Streamlit */

    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stApp"] {
        margin: 0 !important;
        padding: 0 !important;
        width: 100% !important;
        height: 100% !important;
        overflow: hidden !important;
    }


    /* Remove header */

    header {
        visibility: hidden;
        height: 0 !important;
    }


    /* Remove menu */

    #MainMenu {
        visibility: hidden;
    }


    /* Remove footer */

    footer {
        visibility: hidden;
    }


    /* Container principal */

    [data-testid="stMainBlockContainer"] {
        padding: 0 !important;
        margin: 0 !important;
        max-width: none !important;
    }


    /* Remove espaço dos blocos */

    [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }


</style>
""", unsafe_allow_html=True)


# --------------------------------
# Carrega o HTML
# --------------------------------

html_path = Path(__file__).parent / "index.html"

html = html_path.read_text(encoding="utf-8")


# --------------------------------
# Renderiza a aplicação HTML
# --------------------------------

components.html(
    html,
    height=1000,
    scrolling=False
)
