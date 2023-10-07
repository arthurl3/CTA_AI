from models.card import Card
from . import *
from .cardwidget import CardWidget


class BoardWidget(customtkinter.CTkFrame):
    def __init__(self, master, viewmodel, *args, **kwargs):
        self.parent = master
        super().__init__(master, *args, **kwargs)

        self.viewmodel = viewmodel
        self.cardwidgets = []

        self.rowconfigure(0, weight=1)
        self.columnconfigure(tuple(range(16)), weight=1)

        p, x, y = 0, 0, 0
        for card in viewmodel.board:
            cw = CardWidget(self, card)
            self.cardwidgets.append(cw)
            cw.grid(row=y, column=x, padx=10, pady=(5, 5), sticky="n")
            cw.configure(height=100, width=70)
            cw.configure(command=lambda pos=p: self.play_card(pos))
            cw.disable()

            x += 1
            p += 1
            if x % 4 == 0:
                x = 0
                y += 1

    def play_card(self, pos):
        if not self.cardwidgets[pos].is_activate:
            self.cardwidgets[pos].activate()
            self.viewmodel.play_card(pos)
            self.parent.update()


    def update(self):
        for pos in range(16):
            self.cardwidgets[pos].card = self.viewmodel.board[pos]
            self.cardwidgets[pos].update()


