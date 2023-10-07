from random import shuffle
import loader
from models.card import Card
from logic.boardgraph import BoardGraph

class GameViewModel:
    def __init__(self, settings, view):

        self.settings = settings
        self.view = view
        self.player = True # True, host to play Else guest

        self.board = [Card(-1, 0, 0) for i in range(16)]
        self.board_graph = BoardGraph()

        self.deck_host = loader.load_deck(settings.deck_host)
        self.deck_guest = loader.load_deck(settings.deck_guest)

        for card in self.deck_guest:
            card.owner = False

        shuffle(self.deck_host)
        shuffle(self.deck_guest)

        # View attributes
        self.selected_card = None

    # When a player click on a card in his hand
    def set_selected(self, card):
        self.selected_card = card

    def get_hand(self):
        return self.deck_host[:6]

    # Logic when a player play a card
    def play_card(self, position):
        if self.player and self.selected_card:  # Si l'hote a selectionné une carte à jouer
            self.board_graph.play_card(self.selected_card, position)
            self.board = self.board_graph.to_board_array()
            self.deck_host.remove(self.selected_card)
            self.player = False
            self.ai_play() #On fait jouer l'IA

    def ai_play(self):
        #Random pour l'instant on joue au premier indice disponible
        for i in range(16):
            if self.board[i].initial_power == -1:
                card = self.deck_guest[0] #ai.play() mais on joue la premiere dispo
                self.board_graph.play_card(card, i)
                self.board = self.board_graph.to_board_array()
                self.deck_guest.remove(card)
                self.player = True
                self.view.update()
                break












