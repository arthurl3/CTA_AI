import json

from config import Config


class Card:
    def __init__(self, a_id, element, power, current_power=-1, owner=True):
        self.id = a_id
        self.element = element
        self.initial_power = power
        self.current_power = power
        if current_power != -1:
            self.current_power = current_power
        self.owner = owner  # True = Host, False = Guest
        self.color = Config.ARKHOME_COLORS[element]


    def __str__(self):
        return f"id : {self.id} - element : {self.element} - power : {self.current_power}"


