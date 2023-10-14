import customtkinter

from config import Config
from viewmodels.deckbuilderviewmodel import DeckBuilderViewModel
from views.widgets.cardwidget import CardWidget


class DeckbuilderView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.deckbuilder_viewmodel = DeckBuilderViewModel(self)


        # DECK NAME
        self.deckname_area = customtkinter.CTkFrame(self)
        self.deckname_label = customtkinter.CTkLabel(self.deckname_area, text="NAME : ")
        self.textbox = customtkinter.CTkTextbox(self.deckname_area, width=150, height=25)
        self.deckname_label.grid(row=0, column=0)
        self.textbox.grid(row=0, column=1)
        self.deckname_area.grid(row=0, column=0)

        # SPECIAL ABILITY
        self.sa_mode_optionmenu = customtkinter.CTkOptionMenu(self,
                                                                       values=Config.SPECIAL_POWERS,
                                                                       command=self.deckbuilder_viewmodel.change_special_ability)
        self.sa_mode_optionmenu.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="n")
        self.sa_mode_optionmenu.set("NONE")

        # COUNTER
        self.counter_label = customtkinter.CTkLabel(self.deckname_area, text=f"POINTS : {self.deckbuilder_viewmodel.points_counter}")
        self.counter_label.grid(row=2, column=0)

        # Deck area zone
        self.deckarea = customtkinter.CTkFrame(self, fg_color="#5B5EA6")
        self.deckarea.columnconfigure(tuple(range(15)), weight=1)
        self.deckarea.rowconfigure(tuple(range(2)), weight=1)
        self.deckarea.grid(row=3, column=0, sticky="nsew", pady=(5,5), padx=(0,0),ipadx=1, ipady=2)


        # Card selection zone
        self.cardselector = customtkinter.CTkFrame(self, fg_color='#9B2335')
        self.cardselector.columnconfigure(tuple(range(15)), weight=1)
        self.cardselector.rowconfigure(tuple(range(4)), weight=1)
        self.cardselector.grid(row=4, column=0, sticky="news")


        # Ok button
        self.bt = customtkinter.CTkButton(self, command=self.deckbuilder_viewmodel.create_deck, text="Create")
        self.bt.grid(row=5, column=0, pady=2)

        # Divide the frame into 2 equally sized frames
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=4)
        self.grid_rowconfigure(4, weight=5)
        self.grid_rowconfigure(5, weight=1)

        self.deck_cardviews = []

        for y in range(2):
            for x in range(15):
                cw = None
                if y == 0 and x == 0:
                    cw = CardWidget(master=self.deckarea, leader=True)
                else:
                    cw = CardWidget(master=self.deckarea)
                self.deck_cardviews.append(cw)
                # Add delete method when clicked
                cw.configure(command=lambda cardview=cw: self.deckbuilder_viewmodel.remove_card_from_deck(cardview))
                cw.grid(row=y, column=x)


        self.deckbuilder_viewmodel.draw_cardselector()




    def update(self):
        self.counter_label.configure(text=f"POINTS : {self.deckbuilder_viewmodel.points_counter}")

        for cw in self.deck_cardviews:
            cw.card = None
            cw.disable()

        i = 0
        # Update of deck card list
        for card in self.deckbuilder_viewmodel.selected_cards:
            self.deck_cardviews[i].card = card
            self.deck_cardviews[i].update()
            i += 1

    def reset(self):
        self.counter_label.configure(text=f"POINTS : {self.deckbuilder_viewmodel.points_counter}")
        # On oublie tous les widgets de la zone de deck
        for widget in self.deckarea.winfo_children():
            widget.destroy()














