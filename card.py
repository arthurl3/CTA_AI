class Card:
    def __init__(self, element, power):
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

