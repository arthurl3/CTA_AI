from . import *


class DrawnCardWidget(customtkinter.CTkFrame):
    def __init__(self, master, viewmodel, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        FONT = customtkinter.CTkFont(size=10, weight="bold")

        self.viewmodel = viewmodel

        ### TEXT ###
        self.label1 = customtkinter.CTkLabel(self, text="DRAWN CARD : ", font=FONT)
        self.label1.grid(row=0, column=0)

        cards = self.viewmodel.deck_host

        # Supprimer les occurrences de None
        cards_purified = [card.__str__(option_format=True) for card in cards if card is not None]


        ### CARD FROM DECK ###
        self.deck1_mode_optionmenu = customtkinter.CTkOptionMenu(self,
                                                                 values=cards_purified,
                                                                 command=self.viewmodel.change_card_to_add)
        self.deck1_mode_optionmenu.grid(row=0, column=1, padx=10)
        self.deck1_mode_optionmenu.set("1")

        ##### BUTTON VALIDATE ###
        self.btn = customtkinter.CTkButton(self, command=self.viewmodel.add_card_to_hand, text="OK")
        self.btn.grid(row=0, column=2, padx=20)





















