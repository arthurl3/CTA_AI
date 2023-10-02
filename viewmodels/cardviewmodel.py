from config import Config

class CardViewModel:
    def __init__(self, cardmodel):
        self.cardmodel = cardmodel
        self.id = cardmodel.id
        self.text = cardmodel.initial_power
        self.color = Config.CARDS_COLORS[cardmodel.element]
        self.initialpower = cardmodel.initial_power
        self.currentpower = cardmodel.current_power