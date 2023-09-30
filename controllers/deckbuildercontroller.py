import loader
from models.deck import Deck
from models.card import Card
import copy

class DeckBuilderController:
    def __init__(self):
        self.deck = []
        self.cardlist = loader.load_cards()

    def create_deck(self):
        print(f"number of cards selected : {len(self.deck)}")
        if len(self.deck) == 30:
            loader.insert_deck(self.deck)


    def add_card_to_deck(self, card):
        self.deck.append({"id": card.id})
