import os

import customtkinter


class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CARDS_DATA_PATH = BASE_DIR + "\data\cards.json"
    DECKS_DATA_PATH = BASE_DIR + "\data\decks.json"

    #Stockage par tableau des couleurs des éléments (Rappel : 0 = Nature, ..., 6 = Air)
    ARKHOME_COLORS = ["#29B621", "#E5A360", "#C615FE", "#359EFE", "#F42602", "#FEFD9B", "#A8FFFE"]
    ARKHOME_COLORS_NAME = ["NATURE", "TERRE", "TENEBRE", "EAU", "FEU", "LUMIERE", "AIR"]

    WINDOW_WIDTH = 1100
    WINDOW_HEIGHT = 800

    FRAMEID_DECKBUILDER = "frame1"
    FRAMEID_SETTINGS = "frame2"
    FRAMEID_GAME = "frame3"

    app = None