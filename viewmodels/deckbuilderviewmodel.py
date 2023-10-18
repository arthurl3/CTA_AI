import loader
from config import Config
from models.card import Card
from views.widgets.cardwidget import CardWidget

class DeckBuilderViewModel:
    def __init__(self, deckbuilderview):
        # Liste de toutes les cartes du jeu
        self.cards = loader.load_cards()
        self.all_cardviews = []
        # Liste des cartes choisies du deck
        self.selected_cards = []
        self.deck_cardviews = []
        self.view = deckbuilderview
        self.special_ability = "None"
        self.points_counter = 0
        self.field_counter = 0


    def add_card_to_deck(self, card):
        # On ajoute la carte seulement si puissance ≤ DECK_POWER_MAX et n_cards < DECK_N_CARDS_MAX
        if len(self.selected_cards) < 30:
            counter = card.initial_power

            if card.field:
                counter += 300

            if self.points_counter + counter <= 15000:
                self.points_counter += counter
                self.selected_cards.append(card)
                self.view.update()
            else:
                print(f"Points dépassés : {self.points_counter}")
                self.points_counter -= card.initial_power

    def remove_card_from_deck(self, cardview):
        if cardview.card:
            self.selected_cards.remove(cardview.card)
            self.points_counter -= cardview.card.initial_power

            if cardview.card.field:
                self.points_counter -= 300
            self.view.update()


    # Construit un deck avec les cartes choisies puis l'insère le fichier JSON
    def create_deck(self):
        deck_name = self.view.textbox.get("0.0", "end")
        deck_cards = []
        if len(self.selected_cards) == 30:
            for card in self.selected_cards:
                deck_cards.append(card.id)

            loader.insert_deck(deck_cards, deck_name, Config.SPECIAL_POWERS.index(self.special_ability))
            self.selected_cards = []
            self.points_counter = 0
            self.view.reset()
        else:
            print(f"number of cards selected : {len(self.selected_cards)}. Asked 30")


    # add list of all cards into this views
    def draw_cardselector(self):
        self.all_cardviews = [CardWidget(master=self.view.cardselector, card=card) \
                              for card in self.cards]
        x, y = 0, 0
        for cardview in self.all_cardviews:
            cardview.grid(row=y, column=x, padx=1, pady=1)
            cardview.configure(command=lambda c=cardview.card: self.add_card_to_deck(c))
            if (x + 1) % 15 == 0:
                x = 0
                y += 1
            else:
                x += 1


    def change_special_ability(self, sa: str):
        self.special_ability = sa







