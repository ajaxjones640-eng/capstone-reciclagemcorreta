import pygame

# Inicialização do pygame (precisa acontecer antes de criar as fontes)
pygame.init()

# Configuração da janela
WIDTH = 1280
HEIGHT = 720
FPS = 60

# Duração de uma fase, em segundos
GAME_DURATION = 60

# Número de vidas do jogador em uma fase (sistema de vidas do protótipo)
LIVES_INICIAIS = 3

# Cores base (usadas nos resíduos, cestos e textos sobre eles)
LIME = (50, 205, 50)
LIME_DARK = (32, 168, 32)
GREEN_DARK = (22, 138, 22)
WHITE = (255, 255, 255)
TEXT = (23, 51, 23)
TEXT_LIGHT = (91, 113, 91)
BORDER = (216, 243, 216)
FOOTER = (145, 167, 145)
BLUE = (45, 125, 190)
RED = (225, 55, 55)
YELLOW = (250, 195, 30)
GLASS_GREEN = (65, 175, 75)
BROWN = (155, 105, 60)
DARK = (35, 35, 35)

# Céu da tela de jogo (fundo por trás da esteira e dos cestos)
SKY_BLUE = (94, 176, 226)

# Tema escuro do menu, das instruções e dos painéis de HUD (do protótipo)
BG_DARK = (18, 19, 15)
PANEL_DARK = (18, 27, 43)
BTN_DARK = (27, 28, 23)
BTN_DARK_HOVER = (40, 42, 34)
BTN_DARK_BORDER = (45, 46, 40)
PRIMARY_GREEN = (152, 199, 85)
PRIMARY_GREEN_HOVER = (166, 213, 100)
TEXT_ON_DARK = (238, 238, 238)
MUTED_ON_DARK = (150, 150, 150)
ICON_BG_DARK = (23, 97, 11)

# Corações do sistema de vidas
HEART_COLOR = (230, 90, 90)
HEART_EMPTY = (90, 90, 90)

# Fontes
FONT_TITLE = pygame.font.SysFont("arial", 42, bold=True)
FONT_SUBTITLE = pygame.font.SysFont("arial", 15)
FONT_BUTTON = pygame.font.SysFont("arial", 15, bold=True)
FONT_BIN = pygame.font.SysFont("arial", 20, bold=True)
FONT_ITEM = pygame.font.SysFont("arial", 17, bold=True)
FONT_SMALL = pygame.font.SysFont("arial", 14, bold=True)
FONT_PHASE = pygame.font.SysFont("arial", 28, bold=True)
FONT_SCORE = pygame.font.SysFont("arial", 20, bold=True)
FONT_STAR = pygame.font.SysFont("arial", 38, bold=True)
FONT_MESSAGE = pygame.font.SysFont("arial", 26, bold=True)
