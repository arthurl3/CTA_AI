class Hand:
    def __init__(self, deck):
        self.deck = deck
        self.cards = []
        #Initialize the hand by drawing 5 cards
        for i in range(5):
            self.draw()

    def play_card(self, card):
        self.cards.remove(card)

    def draw(self):
       self.cards.append(self.deck.get_next_card())