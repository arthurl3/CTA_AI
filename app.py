import tkinter
import customtkinter
from functools import partial
from component.deckbuilderarea import DeckbuilderArea
from component.gamearea import GameArea

class App(customtkinter.CTk):
    DARK_MODE = "dark"
    FRAMEID_DECKBUILDER = "frame1"
    FRAMEID_GAMEAREA = "frame2"
    customtkinter.set_appearance_mode(DARK_MODE)
    customtkinter.set_default_color_theme("blue")
    frames = {}
    current = None
    bg = ""

    def __init__(self):
        super().__init__()
        self.num_of_frames = 0
        self.title("CTA AI")

        # screen size
        self.geometry("1200x600")

        # root!
        main_container = customtkinter.CTkFrame(self, corner_radius=8)
        main_container.pack(fill=tkinter.BOTH, expand=True, padx=8, pady=8)

        # left side panel -> for frame selection
        self.left_side_panel = customtkinter.CTkFrame(main_container, width=280, corner_radius=8)
        self.left_side_panel.pack(side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=5, pady=5)

        # right side panel -> to show the frame1 or frame 2, or ... frame + n where n <= 5
        self.right_side_panel = customtkinter.CTkFrame(main_container, corner_radius=8, fg_color="#212121")
        self.right_side_panel.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=0, pady=0)
        self.right_side_panel.configure(border_width=1)
        self.right_side_panel.configure(border_color="#323232")

        #Navigation
        self.create_nav(self.left_side_panel, self.FRAMEID_DECKBUILDER)
        self.create_nav(self.left_side_panel, self.FRAMEID_GAMEAREA)


    # button to select the correct frame
    def frame_selector_bt(self, parent, frame_id):
        # create frame
        bt_frame = customtkinter.CTkButton(parent)
        # style frame
        bt_frame.configure(height=40)
        # creates a text label
        if frame_id == self.FRAMEID_DECKBUILDER:
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
        if frame_id == self.FRAMEID_DECKBUILDER:
            App.frames[frame_id] = DeckbuilderArea(master=self)
        elif frame_id == self.FRAMEID_GAMEAREA:
            App.frames[frame_id] = GameArea(master=self)

    # method to change component
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

    # method to create a pair button selector and its related frame
    def create_nav(self, parent, frame_id):
        self.frame_selector_bt(parent, frame_id)
        self.create_frame(frame_id)
