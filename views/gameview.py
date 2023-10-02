import customtkinter

from viewmodels.gameviewmodel import GameViewModel


class GameView(customtkinter.CTkFrame):
    def __init__(self, master, settings, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        # View Model
        self.game_viewmodel = GameViewModel(settings)

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # add widgets onto the frame, for example:
        self.label = customtkinter.CTkLabel(self)
        self.label.grid(row=0, column=0, padx=20)
