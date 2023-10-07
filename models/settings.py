class Settings:
    def __init__(self):
        self.starting_player = True  # True: Host, False: Guest
        self.score2win = 65
        self.affix1 = None  # No affix by default
        self.affix2 = None
        self.deck_host = "2"
        self.deck_guest = "2"

    def __str__(self):
        return (f"starting_player : {self.starting_player}"
                f" - score2win : {self.score2win}"
                f" - affix1 : {self.affix1}"
                f"- affix2 : {self.affix2}"
                )

