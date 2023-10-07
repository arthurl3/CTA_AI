import customtkinter
from models.settings import Settings
from viewmodels.gameviewmodel import GameViewModel
from views.widgets.boardwidget import BoardWidget
from views.widgets.drawncardwidget import DrawnCardWidget
from views.widgets.handwidget import HandWidget
from views.widgets.nextmovewidget import NextMoveWidget


class GameView(customtkinter.CTkFrame):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # View Model
        self.game_viewmodel = GameViewModel(Settings(), self)

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=4)
        self.grid_rowconfigure(3, weight=2)
        self.grid_rowconfigure(0, weight=1)

        # To Select opponent plays
        self.nextmove_widget = NextMoveWidget(self, self.game_viewmodel)
        self.nextmove_widget.grid(row=0, column=0)

        # The Board
        self.board_widget = BoardWidget(self, self.game_viewmodel)
        self.board_widget.grid(row=1, column=0)

        # The card drawn
        self.drawncard_widget = DrawnCardWidget(self, self.game_viewmodel)
        self.drawncard_widget.grid(row=2, column=0)

        # The host player hand
        self.hand_widget = HandWidget(self, self.game_viewmodel)
        self.hand_widget.grid(row=3, column=0)

    def update(self):
        self.board_widget.update()
        self.hand_widget.update()







