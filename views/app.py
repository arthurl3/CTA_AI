import tkinter
import customtkinter
from functools import partial

from config import Config
from views.deckbuilderview import DeckbuilderView
from views.gameview import GameView
from views.matchsettingsview import MatchSettingsView


class App(customtkinter.CTk):

    customtkinter.set_appearance_mode("dark")
    customtkinter.set_default_color_theme("blue")
    frames = {}
    current = None

    def __init__(self):
        super().__init__()
        self.num_of_frames = 0
        self.title("CTA AI")

        # screen size
        self.geometry(f"{Config.WINDOW_WIDTH}x{Config.WINDOW_HEIGHT}")

        # root
        main_container = customtkinter.CTkFrame(self, corner_radius=8)
        main_container.pack(fill=tkinter.BOTH, expand=True, padx=8, pady=8)

        # left side panel -> for frame selection
        self.left_side_panel = customtkinter.CTkFrame(main_container, width=280, corner_radius=8)
        self.left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=5, pady=5)

        # right side panel -> to show the frames
        self.right_side_panel = customtkinter.CTkFrame(main_container, corner_radius=8, fg_color="#212121")
        self.right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        self.right_side_panel.configure(border_width=1)
        self.right_side_panel.configure(border_color="#323232")

        # Navigation buttons
        self.frame_selector_bt(self.left_side_panel, Config.FRAMEID_DECKBUILDER)
        self.frame_selector_bt(self.left_side_panel, Config.FRAMEID_SETTINGS)

        self.create_frame(Config.FRAMEID_DECKBUILDER)
        self.create_frame(Config.FRAMEID_SETTINGS)
        self.create_frame(Config.FRAMEID_GAME)

        ### FOR DEBUGGING ###
        self.toggle_frame_by_id(Config.FRAMEID_GAME)


    # button to select the correct frame
    def frame_selector_bt(self, parent, frame_id):
        # create frame
        bt_frame = customtkinter.CTkButton(parent)
        # style frame
        bt_frame.configure(height=40)
        # creates a text label
        if frame_id == Config.FRAMEID_DECKBUILDER:
            bt_frame.configure(text="Deck Builder")
        else:
            bt_frame.configure(text="Start Game")
        bt_frame.configure(command=partial(self.toggle_frame_by_id, "frame" + str(self.num_of_frames + 1)))
        # set layout
        bt_frame.grid(pady=5, row=self.num_of_frames, column=0)
        # update state
        self.num_of_frames = self.num_of_frames + 1

    # create the frame
    def create_frame(self, frame_id):
        if frame_id == Config.FRAMEID_DECKBUILDER:
            App.frames[frame_id] = DeckbuilderView(master=self)
        elif frame_id == Config.FRAMEID_SETTINGS:
            App.frames[frame_id] = MatchSettingsView(master=self)
        elif frame_id == Config.FRAMEID_GAME:
            App.frames[frame_id] = GameView(master=self)

    # method to change views
    def toggle_frame_by_id(self, frame_id):
        if App.frames[frame_id] is not None:
            if App.current is App.frames[frame_id]:
                App.current.pack_forget()
                App.current = None
            elif App.current is not None:
                App.current.pack_forget()
                App.current = App.frames[frame_id]
                App.current.pack(in_=self.right_side_panel, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0,
                                 pady=0)
            else:
                App.current = App.frames[frame_id]
                App.current.pack(in_=self.right_side_panel, side=tkinter.TOP, fill=tkinter.BOTH, expand=True, padx=0,
                                 pady=0)
