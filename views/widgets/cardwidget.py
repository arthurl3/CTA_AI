import customtkinter


class CardWidget(customtkinter.CTkButton):
    def __init__(self, master, card, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.card = card
        self.is_activate = True

        self.configure(height=60)
        self.configure(width=27)
        self.configure(border_spacing=0)
        self.configure(corner_radius=10)
        self.configure(font=("Helvetica", 18, "bold"))

        self.text_label = customtkinter.CTkLabel(master=self, text=self.card.current_power)

        self.activate()

    def disable(self):
        self.is_activate = False
        self.configure(fg_color="white")
        self.configure(text_color="white")
        self.configure(text="")
        self.configure(hover_color="#DC143C")
        self.configure(border_color="#DC143C")

    def activate(self):
        self.is_activate = True
        self.configure(text_color="#484848")
        self.configure(border_color="#DC143C")
        self.update()

    def update(self):
        if self.is_activate or self.card.id != -1:
            self.configure(fg_color=self.card.color)
            self.configure(text=self.card.current_power)

