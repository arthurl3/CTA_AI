class Settings:
    def __init__(self):
        self.host_is_p1 = True  # True: Host, False: Guest
        self.score2win = 65
        self.affix1 = None  # No affix by default
        self.affix2 = None
        self.deck_host = "Test"
        self.deck_guest = "Test"
        self.mode = 0 # 0 : Player vs IA, 1 : IA Assist (Mode selection not implemented in UI for now)

    def __str__(self):
        return (f"starting_player : {self.host_is_p1}"
                f" - score2win : {self.score2win}"
                f" - affix1 : {self.affix1}"
                f"- affix2 : {self.affix2}"
                )

