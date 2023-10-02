from . import *

class NextMoveWidget(customtkinter.CTkButton):
    def __init__(self, master, card_viewmodel, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        FONT = customtkinter.CTkFont(size=10, weight="bold")