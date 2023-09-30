import json


class Card():
    def __init__(self, id, element, power):
        self.id = id
        self.element = element
        self.initial_power = power
        self.current_power = power
        self.list_trinity = []
        self.list_affinity = []

    def addTrinity(self, trinity):
        # Before adding, we must verify if it already exists or not
        if not trinity in self.list_trinity:
            self.list_trinity.append(trinity)

        # Verify also for affinities
        for element in trinity:
            if element in self.list_affinity:
                self.list_affinity.remove(element)

    def addAffinity(self, affinity):
        if not affinity in self.list_affinity:
            self.list_affinity.append(affinity)


    def __str__(self):
        return f"id : {self.id} - element : {self.element} - power : {self.initial_power}"

    # never used
    def serialize(self):
        return json.dumps(
            {
            'id': self.id,
            'element': self.element,
            'power': self.initial_power
            }
        )

