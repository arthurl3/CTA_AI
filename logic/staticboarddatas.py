from random import shuffle

import loader


class StaticBoardDatas:
    def __init__(self, settings):
        self.score2win = settings.score2win
        self.affix1 = settings.affix1  # No affix by default
        self.affix2 = settings.affix2

        self.deck_p1 = []
        self.deck_p2 = []

        self.special_ability_p1 = None
        self.special_ability_p2 = None

        if settings.host_is_p1:
            self.load_deck(deck_name=settings.deck_host, player=1)
            self.load_deck(deck_name=settings.deck_guest, player=2)
        else:
            self.load_deck(deck_name=settings.deck_guest, player=1)
            self.load_deck(deck_name=settings.deck_host, player=2)

    # DECK LOADING
    def load_deck(self, deck_name, player):
        (deck, sa) = loader.load_deck(deck_name)

        # Le leader reste à l'index 0
        leader = deck[0]
        deck.remove(leader)
        shuffle(deck)

        if player == 1:
            self.deck_p1.append(leader)
            self.deck_p1.extend(deck)
            self.special_ability_p1 = sa
        if player == 2:
            self.deck_p2.append(leader)
            self.deck_p2.extend(deck)
            self.special_ability_p2 = sa

            for card in self.deck_p2:
                card.owned_by_p1 = False

    def remove_card_from_deck(self, id, player):
        if player == 1:
            deck = self.deck_p1
        else:
            deck = self.deck_p2
        for card in deck:
            if card.id == id:
                deck.remove(card)
