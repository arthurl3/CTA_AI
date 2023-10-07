import loader
from models.card import Card
from views.widgets.cardwidget import CardWidget

class DeckBuilderViewModel:
    def __init__(self, deckbuilderview):

        self.view = deckbuilderview
        # Liste des cartes choisies du deck
        self.selected_cardviews = []


        # Liste de toutes les cartes du jeu
        self.cards = loader.load_cards()
        self.all_cardviews = []

        # Coordonnées des cartes de la zone de deck
        self.deckarea_x = 0
        self.deckarea_y = 0

    def add_card_to_deck(self, card):
        # On ajoute la carte seulement si puissance ≤ DECK_POWER_MAX et n_cards < DECK_N_CARDS_MAX
        if len(self.selected_cardviews) < 30:
            cardview = CardWidget(master=self.view.deckarea, card_viewmodel=card.card_viewmodel)
            cardview.grid(row=self.deckarea_y, column=self.deckarea_x, padx=4, pady=4, sticky="nw")
            # Add delete method when clicked
            cardview.configure(command=lambda: self.remove_card_from_deck(cardview))

            self.selected_cardviews.append(cardview)

            # Increase i and j
            self.deckarea_x += 1
            if self.deckarea_x == 15:
                self.deckarea_x = 0
                self.deckarea_y += 1

    def remove_card_from_deck(self, cardview):
        self.selected_cardviews.remove(cardview)
        cardview.destroy()

        # Update of index
        self.deckarea_x -= 1
        if self.deckarea_x == -1:
            self.deckarea_x = 14
            self.deckarea_y -= 1
        self.redraw_deck_frame()


    # Construit un deck avec les cartes choisies puis l'insère le fichier JSON
    def create_deck(self):
        selected_cards = []
        if len(self.selected_cardviews) == 30:
            for cardview in self.selected_cardviews:
                selected_cards.append(cardview.card_viewmodel.id)
            loader.insert_deck(selected_cards)
        else:
            print(f"number of cards selected : {len(self.selected_cardviews)}. Asked 30")


    # Redraw the list of cards by changing position when a card is removed
    def redraw_deck_frame(self):
        x, y = 0, 0
        for cardview in self.selected_cardviews:
            cardview.grid(row=y, column=x, padx=1, pady=1)
            if (x + 1) % 15 == 0:
                x = 0
                y += 1
            else:
                x += 1

    # add list of all cards into this views
    def draw_cardselector(self):
        self.all_cardviews = [CardWidget(master=self.view.cardselector, card=card) \
                              for card in self.cards]
        x, y = 0, 0
        for cardview in self.all_cardviews:
            cardview.grid(row=y, column=x, padx=1, pady=1)
            cardview.configure(command=lambda c=cardview: self.add_card_to_deck(c))
            if (x + 1) % 15 == 0:
                x = 0
                y += 1
            else:
                x += 1



