from models.hand import Hand

class Player:
    def __init__(self, deck):
        self.deck = deck
        self.hand = Hand(deck)


    def get_hand(self):
        return self.hand


