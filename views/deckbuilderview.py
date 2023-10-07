import customtkinter

from viewmodels.deckbuilderviewmodel import DeckBuilderViewModel
class DeckbuilderView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.deckbuilder_viewmodel = DeckBuilderViewModel(self)


        # Deck area zone
        self.deckarea = customtkinter.CTkFrame(self, fg_color="#8c7373")
        self.deckarea.columnconfigure(tuple(range(15)), weight=1)
        self.deckarea.rowconfigure(tuple(range(2)), weight=1)
        self.deckarea.grid(row=0, column=0, sticky="nsew", pady=(5,5), padx=(0,0),ipadx=1, ipady=2)


        # Card selection zone
        self.cardselector = customtkinter.CTkFrame(self, fg_color='#ffe6e6')
        self.cardselector.columnconfigure(tuple(range(15)), weight=1)
        self.cardselector.rowconfigure(tuple(range(4)), weight=1)
        self.cardselector.grid(row=1, column=0, sticky="news")


        # Ok button
        self.bt = customtkinter.CTkButton(self, command=self.deckbuilder_viewmodel.create_deck, text="Create")
        self.bt.grid(row=2, column=0, pady=2)

        # Divide the frame into 2 equally sized frames
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=4)
        self.grid_rowconfigure(1, weight=5)
        self.grid_rowconfigure(2, weight=1)

        self.deckbuilder_viewmodel.draw_cardselector()















