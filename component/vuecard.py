from models.card import Card
import tkinter
import customtkinter

class VueCard(customtkinter.CTkButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.parent = args[0]
        self.configure(height=60)
        self.configure(width=27)
        self.configure(command=self.onclick)
        self.card = None
        self.text = None
        self.color = None
        self.element = None
        self.f_parent = None




    def initialize_with_model(self, card):
        self.card = card
        self.text = customtkinter.CTkLabel(master=self, text=card.current_power)

        #Element color
        match card.element:
            case 0:
                self.color = "#29B621"
            case 1:
                self.color = "#E5A360"
            case 2:
                self.color = "#C615FE"
            case 3:
                self.color = "#359EFE"
            case 4:
                self.color = "#F42602"
            case 5:
                self.color = "#FEFD9B"
            case 6:
                self.color = "#A8FFFE"

        self.configure(bg_color=self.color)
        self.configure(fg_color=self.color)
        self.configure(text_color="#484848")
        self.configure(font=("Helvetica",  18, "bold"))
        self.configure(text=card.current_power)

    def onclick(self):
        print(self.card.id)
        self.configure(fg_color="white")
        self.configure(bg_color="white")
        self.configure(text_color="white")
        self.f_parent(self.card)


    def set_onclick(self, f):
        self.f_parent = f

