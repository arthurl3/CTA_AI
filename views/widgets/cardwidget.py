from tkinter import PhotoImage

import customtkinter
from customtkinter import CTkImage
from PIL import Image, ImageTk
from config import Config


class CardWidget(customtkinter.CTkButton):
    def __init__(self, master, card=None, leader=False, owner=False, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.card = card
        self.leader = leader
        self.owner = owner

        #  CONFIGURE  #
        self.configure(height=75)
        self.configure(width=50)
        self.configure(border_spacing=0)
        self.configure(corner_radius=10)
        self.configure(fg_color="#867979")
        self.configure(text="")
        self.configure(hover_color="#ECF0F1")
        self.configure(font=("Helvetica", 18, "bold"))

        self.image = None

        self.update()

    def disable(self):
        self.configure(fg_color="#867979")
        self.configure(text="")
        self.configure(border_color="#867979")

    def update(self):
        if self.card:
            self.configure(text_color="#484848")
            self.configure(text=self.card.current_power)
            self.configure(fg_color=self.card.color)
            self.configure(border_color=self.card.color)

            if self.card.leader or self.leader:
                self.image = CTkImage(Image.open(Config.CROWN_PATH))
            elif self.card.field:
                self.image = CTkImage(Image.open(Config.FIELD_PATH))
            else:
                self.image = None

            if self.image:
                self.configure(image=self.image)
                self.configure(compound="top")
            else:
                self.configure(image=CTkImage(light_image=Image.new('RGBA', (1, 1),  (255, 255, 255, 0)), size=(1, 1)))
                self.configure(compound='top')
                self.configure(anchor='center')
            if self.owner:
                self.configure(border_width=5)
                # Appartenance Bleu si ça nous appartient, rouge sinon
                if self.card.owned_by_p1:
                    self.configure(border_color="#2874A6")
                else:
                    self.configure(border_color="#ff0000")

        else:
            self.disable()


