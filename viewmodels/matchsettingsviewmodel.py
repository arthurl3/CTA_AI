import tkinter
import loader
from views import app
from views.gameview import GameView


class MatchSettingsViewModel:
    def __init__(self, matchsettingsview):
        # Attributes
        self.starting_player = tkinter.StringVar(value="Random")
        self.deck_host = None
        self.deck_guest = None
        self.score_to_win = 65
        self.affix1 = "NONE"
        self.affix2 = "NONE"

        # Loading decks
        self.all_decks = loader.load_decks()
        self.deck_names = [deck['name'] for deck in self.all_decks]

    def change_deck_host(self, chosen_deck : str):
        self.deck_host = chosen_deck

    def change_deck_guest(self, chosen_deck : str):
        self.deck_guest = chosen_deck

    def change_affix1(self, chosen_affix :str):
        self.affix1 = chosen_affix

    def change_affix2(self, chosen_affix :str):
        self.affix2 = chosen_affix

    def change_score2win(self, score2win : str):
        self.score_to_win = score2win

    def validate(self):
        # Some verifications before validating settings
        if self.deck_host and self.deck_guest:
            app.show_frame(GameView(app, self))
