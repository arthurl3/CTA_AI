import os

import customtkinter


class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CARDS_DATA_PATH = BASE_DIR + "\data\cards.json"
    DECKS_DATA_PATH = BASE_DIR + "\data\decks.json"

    #Stockage par tableau des couleurs des éléments (Rappel : 0 = Nature, ..., 6 = Air)
    CARDS_COLORS = ["#29B621", "#E5A360", "#C615FE", "#359EFE", "#F42602", "#FEFD9B", "#A8FFFE"]

    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 600