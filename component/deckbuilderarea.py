import copy
import customtkinter
from component.vuecard import VueCard
from models.card import Card
from controllers.deckbuildercontroller import DeckBuilderController
class DeckbuilderArea(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.controller = DeckBuilderController()
        self.cardview_list = []

        # Divide the frame into 2 equally sized frames
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=4)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(2, weight=1)

        # Deck area zone
        self.deckarea = customtkinter.CTkFrame(self, fg_color="#8c7373")
        self.deckarea.columnconfigure(tuple(range(15)), weight=1)
        self.deckarea.rowconfigure(tuple(range(2)), weight=1)
        self.deckarea_x = 0
        self.deckarea_y = 0
        self.deckarea.configure(height=250)
        self.deckarea.grid(row=0, column=0, sticky="news")

        # Card selection zone
        self.cardselector = customtkinter.CTkFrame(self, fg_color='#ffe6e6')
        self.cardselector.columnconfigure(tuple(range(20)), weight=1)
        self.cardselector.rowconfigure(tuple(range(6)), weight=1)
        self.cardselector.grid(row=1, column=0, sticky="news")
        self.cardselector.configure(height=400)

        # Ok button
        self.bt = customtkinter.CTkButton(self, command=self.bt_onclick, text="Create")
        self.bt.grid(row=2, column=0, sticky="ns", pady=5)

        # Initialization of cardselector area
        self.fill_cardselector_area()

    def add_card_to_deck(self, card):

        # On ajoute la carte seulement si puissance <= DECK_POWER_MAX et n_cards < DECK_N_CARDS_MAX
        if len(self.cardview_list) < 30:
            cardview = VueCard(self.deckarea)
            cardview.initialize_with_model(card)
            cardview.grid(row=self.deckarea_y, column=self.deckarea_x, padx=5, pady=3)

            # Add delete method on view
            cardview.configure(command=lambda: self.remove_card_from_deck(cardview, card))
            self.cardview_list.append(cardview)
            self.controller.add_card_to_deck(card)

            # Increase i and j
            self.deckarea_x += 1
            if self.deckarea_x == 15:
                self.deckarea_x = 0
                self.deckarea_y += 1


    def remove_card_from_deck(self, cardview, card):
        self.cardview_list.remove(cardview)
        self.controller.remove_card(card)
        cardview.destroy()

        # Update of index
        self.deckarea_x -= 1
        if self.deckarea_x == -1:
            self.deckarea_x = 14
            self.deckarea_y -= 1

        self.redraw_deckarea()

    # Redraw the list of cards by changing position when a card is removed
    def redraw_deckarea(self):
        x = 0
        y = 0

        for cardview in self.cardview_list:
            cardview.grid(row=y, column=x, padx=5, pady=3)
            x += 1
            if x == 14:
                x = 0
                y += 1


    def bt_onclick(self):
        self.controller.create_deck()

    # add list of all cards into this view
    def fill_cardselector_area(self):
        card_list = self.controller.cardlist
        i = 0
        j = 0
        for card in card_list:
            cardview = VueCard(self.cardselector)
            cardview.initialize_with_model(card)
            cardview.set_onclick(self.add_card_to_deck)
            cardview.grid(row=i, column=j, padx=1, pady=1)

            j += 1
            if j == 20:
                j = 0
                i += 1

