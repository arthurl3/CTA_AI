import tkinter

import customtkinter


class MatchParametersArea(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        TITLE_FONT = customtkinter.CTkFont(size=20, weight="bold")
        STARTING_PLAYER_FONT = customtkinter.CTkFont(size=15, weight="bold")


        # Attributes
        self.starting_player = "Random"
        self.deck_j1 = None
        self.deck_j2 = None
        self.score_to_win = 65
        self.affix1 = None
        self.affix2 = None

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 10), weight=1)

        ### TITLE ###
        self.title_label = customtkinter.CTkLabel(self, text="CONFIGURATION DE LA PARTIE", font=TITLE_FONT)
        self.title_label.grid(row=0, column=0, pady=(10, 5))

        ### PLAYER SELECTION ###
        self.rb_frame_playerselection = customtkinter.CTkFrame(self)
        self.rb_frame_playerselection.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.radio_var = tkinter.IntVar(value=0)

        self.rb_frame_playerselection.grid_columnconfigure(0, weight=1, uniform="same_group")
        self.rb_frame_playerselection.grid_columnconfigure(1, weight=1, uniform="same_group")
        self.rb_frame_playerselection.grid_columnconfigure(2, weight=1, uniform="same_group")

        self.label_radio_group = customtkinter.CTkLabel(master=self.rb_frame_playerselection, text="STARTING PLAYER", font=STARTING_PLAYER_FONT)
        self.label_radio_group.grid(row=0, column=0, columnspan=3,  padx=10, pady=10, sticky="we")

        self.radio_button_playerselection1 = customtkinter.CTkRadioButton(master=self.rb_frame_playerselection, variable=self.radio_var, value=0)
        self.radio_button_playerselection1.grid(row=1, column=0, pady=10, padx=20, sticky="ns")
        self.radio_button_playerselection2 = customtkinter.CTkRadioButton(master=self.rb_frame_playerselection, variable=self.radio_var, value=1)
        self.radio_button_playerselection2.grid(row=1, column=1, pady=10, padx=20, sticky="ns")
        self.radio_button_playerselection3 = customtkinter.CTkRadioButton(master=self.rb_frame_playerselection, variable=self.radio_var, value=2)
        self.radio_button_playerselection3.grid(row=1, column=2, pady=10, padx=20, sticky="ns")

        ### DECK J1 AND J2 SELECTION ###


        ### SCORE TO WIN SELECTION ###
        self.score2win_label = customtkinter.CTkLabel(self, text="SCORE TO WIN", anchor="w")
        self.score2win_label.grid(row=2, column=0, padx=20, pady=(10, 0))
        self.score2win_mode_optionmenu = customtkinter.CTkOptionMenu(self,
                                                                       values=["45", "50", "55", "60", "65", "70"],
                                                                       command=self.change_score2win)
        self.score2win_mode_optionmenu.grid(row=3, column=0, padx=20, pady=(10, 10))
        self.score2win_mode_optionmenu.set("65")

        ### AFFIXES SELECTION ###

        ## In another frame
        self.rb_frame_affix_selection = customtkinter.CTkFrame(self)
        self.rb_frame_affix_selection.grid(row=4, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.rb_frame_affix_selection.grid_columnconfigure(0, weight=1, uniform="one_group")
        self.rb_frame_affix_selection.grid_columnconfigure(1, weight=1, uniform="one_group")

        # Affix 1
        self.affix1_label = customtkinter.CTkLabel(self.rb_frame_affix_selection, text="AFFIX 1")
        self.affix1_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.affix1_mode_optionmenu = customtkinter.CTkOptionMenu(self.rb_frame_affix_selection,
                                                                       values=["RANDOM", "NONE", "Elemental", "Inspiring", "Extended reach", "Limited reach", "Shift", "Affinity stacking"],
                                                                       command=self.change_affix1)
        self.affix1_mode_optionmenu.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="n")
        self.affix1_mode_optionmenu.set("NONE")


        self.affix2_label = customtkinter.CTkLabel(self.rb_frame_affix_selection, text="AFFIX 2")
        self.affix2_label.grid(row=0, column=1, padx=20, pady=(10, 0), sticky="news")
        self.affix2_mode_optionmenu = customtkinter.CTkOptionMenu(self.rb_frame_affix_selection,
                                                                  values=["RANDOM", "NONE", "Elemental", "Inspiring",
                                                                          "Extended reach", "Limited reach", "Shift",
                                                                          "Affinity stacking"],
                                                                  command=self.change_affix2)

        self.affix2_mode_optionmenu.grid(row=1, column=1, padx=20, pady=(10, 10), sticky="n")
        self.affix2_mode_optionmenu.set("NONE")


        ##### BUTTON VALIDATE ###
        self.btn = customtkinter.CTkButton(self, command=self.validate, text="START")
        self.btn.grid(row=9, column=0, padx=20, pady=10)


    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_score2win(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_affix1(self):
        pass

    def change_affix2(self):
        pass

    def validate(self):
        print("Validate click")


