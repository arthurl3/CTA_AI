import os

import customtkinter


class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CARDS_DATA_PATH = BASE_DIR + r"\data\cards.json"
    DECKS_DATA_PATH = BASE_DIR + r"\data\decks.json"
    CROWN_PATH = BASE_DIR + r"\resources\crown-1.png"
    FIELD_PATH = BASE_DIR + r"\resources\field-1.png"
    TRASH_PATH = BASE_DIR + r"\resources\trash-1.png"

    SPECIAL_POWERS = ["INVERSION D'AVANTAGE",  "ACCUMULATION DE PUISSANCE", "BANNIERE DE COMMANDEMENT", "INFLUENCE DE TERRAIN", "RENFORCEMENT AFFINITÉS"]

    #Stockage par tableau des couleurs des éléments (Rappel : 0 = Nature, ..., 6 = Air)
    ARKHOME_COLORS = ["#29B621", "#E5A360", "#A569BD", "#359EFE", "#E74C3C", "#FEFD9B", "#A8FFFE"]
    ARKHOME_COLORS_NAME = ["NATURE", "TERRE", "TENEBRE", "EAU", "FEU", "LUMIERE", "AIR"]

    # Stockage par index dans le json (0 = character, 1=field, ...)
    CARD_TYPES = ["CHARACTER", "FIELD", "EQUIPMENT"]


    WINDOW_WIDTH = 1100
    WINDOW_HEIGHT = 800

    FRAMEID_DECKBUILDER = "frame1"
    FRAMEID_SETTINGS = "frame2"
    FRAMEID_GAME = "frame3"

    app = None