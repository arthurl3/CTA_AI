from . import *

class DrawnCardWidget(customtkinter.CTkFrame):
    def __init__(self, master, viewmodel, *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        FONT = customtkinter.CTkFont(size=10, weight="bold")

        self.viewmodel = viewmodel

        ### TEXT ###
        self.label1 = customtkinter.CTkLabel(self, text="DRAWN CARD : ", font=FONT)
        self.label1.grid(row=0, column=0)

        ### CARD FROM DECK ###
        self.deck1_mode_optionmenu = customtkinter.CTkOptionMenu(self,
                                                                values=Config.ARKHOME_COLORS_NAME,
                                                                command=None)
        self.deck1_mode_optionmenu.grid(row=0, column=1, padx=10)
        self.deck1_mode_optionmenu.set("1")


        ##### BUTTON VALIDATE ###
        self.btn = customtkinter.CTkButton(self, command=None, text="OK")
        self.btn.grid(row=0, column=2, padx=20)