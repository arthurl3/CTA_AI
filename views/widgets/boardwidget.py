from . import *


class BoardWidget(customtkinter.CTkButton):
    def __init__(self, master, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.card_viewmodel = None
        self.configure(height=60)
        self.configure(width=27)
        self.configure(text_color="#484848")
        self.configure(font=("Helvetica", 18, "bold"))