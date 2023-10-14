from . import *
from .cardwidget import CardWidget


class HandWidget(customtkinter.CTkFrame):
    def __init__(self, master, viewmodel, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.viewmodel = viewmodel
        self.cardwidgets = []

        self.rowconfigure(0, weight=1)
        self.columnconfigure(tuple(range(6)), weight=1)

        i = 0
        for card in self.viewmodel.get_hand():
            cardwidget = CardWidget(self, card)
            self.cardwidgets.append(cardwidget)
            cardwidget.grid(row=0, column=i, padx=10)
            cardwidget.configure(height=100)
            cardwidget.configure(width=70)
            cardwidget.configure(command=lambda c=card: self.onclick(c))
            i += 1


    def update(self):
        hand = self.viewmodel.get_hand()
        for i in range(6):
            if hand[i]:
                self.cardwidgets[i].card = hand[i]
                self.cardwidgets[i].configure(command=lambda c=hand[i]: self.onclick(c))
                self.cardwidgets[i].update()


    def onclick(self, c):
        self.viewmodel.set_selected(c)
        self.update()









                


