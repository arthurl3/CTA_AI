import json

from config import Config


class Card:
    def __init__(self, a_id, element, power, current_power=-1, owned_by_p1=True, leader=False, field=False):
        self.id = a_id
        self.leader = leader
        self.field = field
        self.element = element
        self.initial_power = power
        self.current_power = current_power
        self.owned_by_p1 = owned_by_p1  # True = Host, False = Guest
        self.color = Config.ARKHOME_COLORS[element]

        if self.current_power == -1:
            self.current_power = self.initial_power

    def __str__(self, option_format=False):
        if option_format:
            return f"{self.id} {Config.ARKHOME_COLORS_NAME[self.element]} {self.current_power}"
        return f"id : {self.id} - element : {self.element} - power : {self.current_power} - owned_by_p1 : {self.owned_by_p1} - field : {'Yes' if self.field else 'No'}"
