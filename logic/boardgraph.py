import networkx as nx

from models.card import Card

'''
Contient les données du plateau de jeu sous forme de graphe en grille

Seules les données essentielles sont représentées ici
=> chaque numéro de node représente sa position à plat sur le plateau
(4x4 => 16) (EXEMPLE : la position du node (x, y) = (2, 2) devient 10)
=> Les donnée d'un node représente une carte sous forme d'un dictionnaire :
Exemple:  carte = {'element': 0, 'initial_pow': 450, 'current_pow': 550, 'owned_by_p1': True }

'''


class BoardGraph(nx.Graph):
    def __init__(self, **attr):
        super().__init__(**attr)

        ### Data in cache
        self.nodes_cache = []
        self.current_player = True  # True p1 false p2
        self.score_p1 = 0
        self.score_p2 = 0
        ###

        for i in range(16):
            card = {'element': -1, 'initial_pow': -1, 'current_pow': -1, 'owned_by_p1': True}
            self.add_node(i, data=card)

        # Define a grid graph
        self.add_edge(0, 1)
        self.add_edge(0, 4)
        self.add_edge(1, 2)
        self.add_edge(1, 5)
        self.add_edge(2, 3)
        self.add_edge(2, 6)
        self.add_edge(3, 7)
        self.add_edge(4, 5)
        self.add_edge(4, 8)
        self.add_edge(5, 6)
        self.add_edge(5, 9)
        self.add_edge(6, 7)
        self.add_edge(6, 10)
        self.add_edge(7, 11)
        self.add_edge(8, 9)
        self.add_edge(8, 12)
        self.add_edge(9, 10)
        self.add_edge(9, 13)
        self.add_edge(10, 11)
        self.add_edge(10, 14)
        self.add_edge(11, 15)
        self.add_edge(12, 13)
        self.add_edge(13, 14)
        self.add_edge(14, 15)

        self.reset_marqued_node()

    def play_card(self, card, pos):

        ### On convertie la carte en data node
        self.nodes[pos]['data'] = self.get_node_data_from_card(card)

        # Récupérer les alliés et ennemies
        allies, ennemies = self.get_allies_and_ennemies(pos)

        # Calcule des affinités et des trinités
        card.current_power = card.initial_power + self.get_power_boost_with_affinities_and_trinities(card, allies)

        # Calcule des reprises
        self.calculate_taken_ennemies(card, ennemies)

        # Calcule des nouvelles forces
        for i_node in range(16):
            if self.exists(i_node):
                self.update_power(i_node)

        self.current_player = not self.current_player


    def exists(self, i_node):
        node = self.nodes[i_node]['data']
        if node['element'] != -1:
            return True
        return False


    def update_power(self, i_node):
        card = self.get_card_from_node(i_node)
        # Récupérer les alliés et ennemies
        allies, ennemies = self.get_allies_and_ennemies(i_node)

        node = self.nodes[i_node]['data']
        # Calcule des affinités et des trinités
        node['current_pow'] = node['initial_pow'] + self.get_power_boost_with_affinities_and_trinities(card, allies)

    def calculate_taken_ennemies(self, card, ennemies):
        ### On calcule maintenant les prises
        for i_ennemy in ennemies:
            ennemy = self.nodes[i_ennemy]['data']
            element_gain = self.get_force(card.element, ennemy['element'])
            if card.current_power + element_gain > ennemy['current_pow']:
                ennemy['owned_by_p1'] = self.current_player
                if self.current_player:
                    self.score_p1 += 2
                else:
                    self.score_p2 += 2

                # On calcule la chaine x1 dans le cas d'une prise
                for i_e in self.neighbors(i_ennemy):
                    e = self.nodes[i_e]['data']
                    element_gain = self.get_force(ennemy['element'], e['element'])
                    if ennemy['current_pow'] + element_gain > e['current_pow']:
                        e['owned_by_p1'] = self.current_player
                        if self.current_player:
                            self.score_p1 += 2
                        else:
                            self.score_p2 += 2

    def get_power_boost_with_affinities_and_trinities(self, card, allies):
        # Verifier trinités et affinités proches (ensembles car ne peut contenir qu'une seule fois une trinité ou une affi)
        affinities = set()
        trinities = set()
        i = 0

        for i_ally in allies:
            ally = self.nodes[i_ally]['data']
            element_distance = self.get_element_distance(card.element, ally['element'])
            # S'il y a encore un node à comparer avec l'actuel
            match element_distance:
                case 0:
                    pass
                case 1:
                    if len(allies) > i + 2:
                        for i_ally_of_ally in allies[i + 1:]:
                            ally_of_ally = self.nodes[i_ally_of_ally]['data']
                            d = self.get_element_distance(card.element, ally_of_ally['element'])
                            if d == 2:
                                trinities.add(1)
                            elif d == 6:
                                trinities.add(0)
                    # Voisins éloignés
                    for i_neighbor in self.neighbors(i_ally):
                        neighbor = self.nodes[i_neighbor]['data']
                        if neighbor['element'] != -1 and neighbor['owned_by_p1'] == self.current_player:
                            d = self.get_element_distance(card.element, neighbor['element'])
                            if d == 2:
                                trinities.add(1)
                            elif d == 6:
                                trinities.add(0)

                case 2:
                    affinities.add(1)

                    if len(allies) > i + 2:
                        for i_ally_of_ally in allies[i + 1:]:
                            ally_of_ally = self.nodes[i_ally_of_ally]['data']
                            d = self.get_element_distance(card.element, ally_of_ally['element'])
                            if d == 1:
                                trinities.add(1)

                    for i_neighbor in self.neighbors(i_ally):
                        neighbor = self.nodes[i_neighbor]['data']
                        if neighbor['element'] != -1 and neighbor['owned_by_p1'] == self.current_player:
                            d = self.get_element_distance(card.element, neighbor['element'])
                            if d == 1:
                                trinities.add(1)
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    affinities.add(-1)
                    print(f"Mise à jour de la carte avec la p_init de {card.initial_power}")
                    if len(allies) > i + 2:
                        for i_ally_of_ally in allies[i + 1:]:
                            ally_of_ally = self.nodes[i_ally_of_ally]['data']
                            d = self.get_element_distance(card.element, ally_of_ally['element'])
                            if d == 6:
                                trinities.add(-1)

                    for i_neighbor in self.neighbors(i_ally):
                        neighbor = self.nodes[i_neighbor]['data']
                        if neighbor['element'] != -1 and neighbor['owned_by_p1'] == self.current_player:
                            d = self.get_element_distance(card.element, neighbor['element'])
                            if d == 6:
                                trinities.add(-1)

                case 6:
                    if len(allies) > i + 2:
                        for i_ally_of_ally in allies[i + 1:]:
                            ally_of_ally = self.nodes[i_ally_of_ally]['data']
                            d = self.get_element_distance(card.element, ally_of_ally['element'])
                            if d == 1:
                                trinities.add(0)
                            elif d == 5:
                                trinities.add(-1)
                    for i_neighbor in self.neighbors(i_ally):
                        neighbor = self.nodes[i_neighbor]['data']
                        if neighbor['element'] != -1 and neighbor['owned_by_p1'] == self.current_player:
                            d = self.get_element_distance(card.element, neighbor['element'])
                            if d == 1:
                                trinities.add(0)
                            elif d == 5:
                                trinities.add(-1)
            i += 1

        # Le boost de force = la longueur de l'intersection des ensembles trinities et affinities facteur 100
        return len(trinities | affinities) * 100

    def get_node_data_from_card(self, card):
        return {'element': card.element, 'initial_pow': card.initial_power,
                'current_pow': card.current_power, 'owned_by_p1': card.owned_by_p1,
                'leader': card.leader}

    def get_card_from_node(self, i_node):
        node = self.nodes[i_node]['data']
        # S'il n'y a pas de carte, on append un No
        if node['initial_pow'] == -1:
            return None
        else:
            return Card(0,
                        node['element'],
                        node['initial_pow'],
                        current_power=node['current_pow'],
                        owned_by_p1=node['owned_by_p1'],
                        leader=node['leader']
                        )

    def to_board_array(self):
        board = []
        # Conversion of each node in card
        for i_node in range(16):
            board.append(self.get_card_from_node(i_node))

        return board

    # Get the distance between both elements (element 6 and element 1 has a distance of 2 because ->1->2)
    def get_element_distance(self, element1, element2):
        if element1 <= element2:
            return element2 - element1
        else:
            return 7 - element1 + element2

    # Get element1 vs element2 bonus or malus
    def get_force(self, e1, e2):
        match self.get_element_distance(e1, e2):
            case 0:
                return 0
            case 1:
                return 150
            case 2:
                return 0
            case 3:
                return 150
            case 4:
                return -150
            case 5:
                return 0
            case 6:
                return -150
        return 0

    def reset_marqued_node(self):
        for i_node in self.nodes:
            self.nodes[i_node]['marque'] = False

    def get_allies_and_ennemies(self, id_node):
        node = self.nodes[id_node]['data']
        allies, ennemies = [], []

        for i_node in self.neighbors(id_node):
            neighbor = self.nodes[i_node]['data']
            if neighbor['element'] != -1:
                if neighbor['owned_by_p1'] == node['owned_by_p1']:
                    allies.append(i_node)
                else:
                    ennemies.append(i_node)
        return allies, ennemies
