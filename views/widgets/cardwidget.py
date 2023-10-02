import customtkinter


class CardWidget(customtkinter.CTkButton):
    def __init__(self, master, card_viewmodel, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.card_viewmodel = card_viewmodel
        self.configure(height=60)
        self.configure(width=27)
        self.configure(text_color="#484848")
        self.configure(font=("Helvetica", 18, "bold"))
        self.configure(bg_color=self.card_viewmodel.color)
        self.configure(fg_color=self.card_viewmodel.color)

        self.text_label = customtkinter.CTkLabel(master=self, text=self.card_viewmodel.text)
        self.configure(text=self.card_viewmodel.cardmodel.current_power)

    def disable(self):
        self.configure(fg_color="white")
        self.configure(bg_color="white")
        self.configure(text_color="white")
