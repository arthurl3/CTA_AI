from . import *

class NextMoveWidget(customtkinter.CTkFrame):
    def __init__(self, master, viewmodel,  *args, **kwargs):
        super().__init__(master, *args, **kwargs)

        self.viewmodel = viewmodel
        FONT = customtkinter.CTkFont(size=10, weight="bold")

        ### TEXT 1 ###
        self.label1 = customtkinter.CTkLabel(self, text="Opponent move : ", font=FONT)
        self.label1.grid(row=0, column=0)

        ### CARD POWER ENTRY ###
        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, placeholder_text="450")
        self.entry.grid(row=0, column=1, padx=20)

        ### ELEMENT OPTION MENU ###
        self.deck1_mode_optionmenu = customtkinter.CTkOptionMenu(self,
                                                                values=Config.ARKHOME_COLORS_NAME,
                                                                command=None)
        self.deck1_mode_optionmenu.grid(row=0, column=3, padx=10)
        self.deck1_mode_optionmenu.set("NATURE")

        ### TEXT 2 ###
        self.label2 = customtkinter.CTkLabel(self, text="in", font=FONT)
        self.label2.grid(row=0, column=4, padx=(3, 3))

        ### POSITION OF CARD ###
        position = ["A1", "A2", "A3", "A4",
                    "B1", "B2", "B3", "B4",
                    "C1", "C2", "C3", "C4",
                    "D1", "D2", "D3", "D4"]

        self.deck1_mode_optionmenu = customtkinter.CTkOptionMenu(self,
                                                                values=position,
                                                                command=None)
        self.deck1_mode_optionmenu.grid(row=0, column=5)
        self.deck1_mode_optionmenu.set("A1")

        ##### BUTTON VALIDATE ###
        self.btn = customtkinter.CTkButton(self, command=None, text="OK")
        self.btn.grid(row=0, column=6, padx=20)
