import tkinter
import customtkinter

from viewmodels.matchsettingsviewmodel import MatchSettingsViewModel


class MatchSettingsView(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        TITLE_FONT = customtkinter.CTkFont(size=20, weight="bold")
        STARTING_PLAYER_FONT = customtkinter.CTkFont(size=15, weight="bold")
        self.matchsettings_viewmodel = MatchSettingsViewModel(self)

        # configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 10), weight=1)

        ### TITLE ###
        self.title_label = customtkinter.CTkLabel(self, text="CONFIGURATION DE LA PARTIE", font=TITLE_FONT)
        self.title_label.grid(row=0, column=0, pady=(10, 5))

        ### PLAYER SELECTION ###
        self.rb_frame_playerselection = customtkinter.CTkFrame(self)
        self.rb_frame_playerselection.grid(row=1, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.rb_frame_playerselection.grid_columnconfigure(0, weight=1, uniform="same_group")
        self.rb_frame_playerselection.grid_columnconfigure(1, weight=1, uniform="same_group")
        self.rb_frame_playerselection.grid_columnconfigure(2, weight=1, uniform="same_group")

        self.label_radio_group = customtkinter.CTkLabel(master=self.rb_frame_playerselection, text="STARTING PLAYER", font=STARTING_PLAYER_FONT)
        self.label_radio_group.grid(row=0, column=0, columnspan=3,  padx=10, pady=10, sticky="we")

        self.radio_button_playerselection1 = customtkinter.CTkRadioButton(master=self.rb_frame_playerselection, variable=self.matchsettings_viewmodel.starting_player, value="Random", text="Random")
        self.radio_button_playerselection1.grid(row=1, column=0, pady=10, padx=20, sticky="ns")
        self.radio_button_playerselection2 = customtkinter.CTkRadioButton(master=self.rb_frame_playerselection, variable=self.matchsettings_viewmodel.starting_player, value="Host", text="Host")
        self.radio_button_playerselection2.grid(row=1, column=1, pady=10, padx=20, sticky="ns")
        self.radio_button_playerselection3 = customtkinter.CTkRadioButton(master=self.rb_frame_playerselection, variable=self.matchsettings_viewmodel.starting_player, value="Guest", text="Guest")
        self.radio_button_playerselection3.grid(row=1, column=2, pady=10, padx=20, sticky="ns")

        ### DECK J1 AND J2 SELECTION ###
        ## In another frame
        self.frame_deck_selection = customtkinter.CTkFrame(self)
        self.frame_deck_selection.grid(row=2, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.frame_deck_selection.grid_columnconfigure(0, weight=1, uniform="one_group")
        self.frame_deck_selection.grid_columnconfigure(1, weight=1, uniform="one_group")

        # DECK 1 (HOST)
        self.deck1_label = customtkinter.CTkLabel(self.frame_deck_selection, text="DECK HOST")
        self.deck1_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.deck1_mode_optionmenu = customtkinter.CTkOptionMenu(self.frame_deck_selection,
                                                                       values=self.matchsettings_viewmodel.deck_names,
                                                                       command=self.matchsettings_viewmodel.change_deck_host)
        self.deck1_mode_optionmenu.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="n")
        self.deck1_mode_optionmenu.set("NONE")

        # DECK 2 (GUEST)
        self.deck2_label = customtkinter.CTkLabel(self.frame_deck_selection, text="DECK GUEST")
        self.deck2_label.grid(row=0, column=1, padx=20, pady=(10, 0), sticky="news")
        self.deck2_mode_optionmenu = customtkinter.CTkOptionMenu(self.frame_deck_selection,
                                                                  values=self.matchsettings_viewmodel.deck_names,
                                                                  command=self.matchsettings_viewmodel.change_deck_guest)

        self.deck2_mode_optionmenu.grid(row=1, column=1, padx=20, pady=(10, 10), sticky="n")
        self.deck2_mode_optionmenu.set("NONE")


        ##############################
        ### SCORE TO WIN SELECTION ###
        self.score2win_label = customtkinter.CTkLabel(self, text="SCORE TO WIN", anchor="w")
        self.score2win_label.grid(row=3, column=0, padx=20, pady=(10, 0))
        self.score2win_mode_optionmenu = customtkinter.CTkOptionMenu(self,
                                                                       values=["45", "50", "55", "60", "65", "70"],
                                                                       command=self.matchsettings_viewmodel.change_score2win)
        self.score2win_mode_optionmenu.grid(row=4, column=0, padx=20, pady=(10, 10))
        self.score2win_mode_optionmenu.set("65")

        ### AFFIXES SELECTION ###
        ## In another frame
        self.frame_affix_selection = customtkinter.CTkFrame(self)
        self.frame_affix_selection.grid(row=5, column=0, padx=(20, 20), pady=(20, 0), sticky="nsew")

        self.frame_affix_selection.grid_columnconfigure(0, weight=1, uniform="one_group")
        self.frame_affix_selection.grid_columnconfigure(1, weight=1, uniform="one_group")

        # Affix 1
        self.affix1_label = customtkinter.CTkLabel(self.frame_affix_selection, text="AFFIX 1")
        self.affix1_label.grid(row=0, column=0, padx=20, pady=(10, 0))
        self.affix1_mode_optionmenu = customtkinter.CTkOptionMenu(self.frame_affix_selection,
                                                                       values=["RANDOM", "NONE", "Elemental", "Inspiring", "Extended reach", "Limited reach", "Shift", "Affinity stacking"],
                                                                       command=self.matchsettings_viewmodel.change_affix1)
        self.affix1_mode_optionmenu.grid(row=1, column=0, padx=20, pady=(10, 10), sticky="n")
        self.affix1_mode_optionmenu.set("NONE")


        self.affix2_label = customtkinter.CTkLabel(self.frame_affix_selection, text="AFFIX 2")
        self.affix2_label.grid(row=0, column=1, padx=20, pady=(10, 0), sticky="news")
        self.affix2_mode_optionmenu = customtkinter.CTkOptionMenu(self.frame_affix_selection,
                                                                  values=["RANDOM", "NONE", "Elemental", "Inspiring",
                                                                          "Extended reach", "Limited reach", "Shift",
                                                                          "Affinity stacking"],
                                                                  command=self.matchsettings_viewmodel.change_affix2)

        self.affix2_mode_optionmenu.grid(row=1, column=1, padx=20, pady=(10, 10), sticky="n")
        self.affix2_mode_optionmenu.set("NONE")

        ##### BUTTON VALIDATE ###
        self.btn = customtkinter.CTkButton(self, command=self.matchsettings_viewmodel.validate, text="START")
        self.btn.grid(row=9, column=0, padx=20, pady=10)