import copy
from random import shuffle

class Deck:
    def __init__(self, name, cards):
        self.name = name
        self.cards = copy.deepcopy(cards)
        self.index = -1
        shuffle(self.cards)

    def get_next_card(self):
        self.index += 1
        return self.cards[self.index]

    #Used when AI brute forcing
    def cancel_turn(self):
        self.index -= 1




