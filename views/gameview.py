import customtkinter
from PIL import Image, ImageTk
from customtkinter import CTkButton, CTkLabel, CTkImage

from config import Config
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
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=4)
        self.grid_rowconfigure(4, weight=2)
        self.grid_rowconfigure(5, weight=1)

        # To Select opponent plays
        self.nextmove_widget = NextMoveWidget(self, self.game_viewmodel)
        self.nextmove_widget.grid(row=0, column=0)

        # The score
        self.score = CTkLabel(self, text="SCORE : HOST 0 - 0 GUEST")
        self.score.grid(row=1, column=0)

        # The Board
        self.board_widget = BoardWidget(self, self.game_viewmodel)
        self.board_widget.grid(row=2, column=0)

        # The card drawn
        self.drawncard_widget = DrawnCardWidget(self, self.game_viewmodel)
        self.drawncard_widget.grid(row=3, column=0)

        ### HAND AND DRAW AREA on the same row
        self.bottom = customtkinter.CTkFrame(self)
        self.bottom.configure(bg_color="#2B2B2B")
        self.bottom.configure(fg_color="#2B2B2B")
        self.bottom.grid(row=4, column=0)
        self.grid_columnconfigure(0, weight=10)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)


        # The host player hand
        self.hand_widget = HandWidget(self.bottom, self.game_viewmodel)
        self.hand_widget.grid(row=0, column=0, padx=40)

        # The Draw btn
        self.draw_btn = CTkButton(self.bottom, height=50, width=40, text=f"DRAW\n{self.game_viewmodel.draw_host_allowed}", anchor="center")
        self.draw_btn.configure(corner_radius=5)
        self.draw_btn.configure(bg_color="#2B2B2B")
        self.draw_btn.configure(command=self.game_viewmodel.change_card)
        self.draw_btn.grid(row=0, column=1, sticky='ws')

        # The Trash btn
        self.trash_btn = CTkButton(self.bottom, height=50, width=40, text="", image=CTkImage(Image.open(Config.TRASH_PATH)), anchor="center")
        self.trash_btn.configure(corner_radius=5)
        self.trash_btn.configure(bg_color="#2B2B2B")
        self.trash_btn.configure(command=self.game_viewmodel.throw_card)
        self.trash_btn.grid(row=0, column=2, sticky='ws')


        # Start IA calculation button
        self.ai_btn = CTkButton(self, text="START AI")
        self.ai_btn.configure(corner_radius=5)
        self.ai_btn.configure(command=self.game_viewmodel.ai_play)
        self.ai_btn.grid(row=5, column=0, sticky='news')


    def update(self):
        self.draw_btn.configure(text=f"DRAW\n{self.game_viewmodel.draw_host_allowed}")
        self.score.configure(text=f"SCORE : HOST {self.game_viewmodel.score_host} - {self.game_viewmodel.score_guest} GUEST")
        self.board_widget.update()
        self.hand_widget.update()







