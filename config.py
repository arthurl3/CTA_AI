import os

import customtkinter


class Config:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    CARDS_DATA_PATH = BASE_DIR + "\data\cards.json"
    DECKS_DATA_PATH = BASE_DIR + "\data\decks.json"
