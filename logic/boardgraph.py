import networkx as nx

from models.card import Card

'''
Contient les données du plateau de jeu sous forme de graphe en grille

Seules les données essentielles sont représentées ici
=> chaque numéro de node représente sa position à plat sur le plateau
(4x4 => 16) (EXEMPLE : la position du node (x, y) = (2, 2) devient 10)
=> Les donnée d'un node représente une carte sous forme d'un dictionnaire :
Exemple:  carte = {'element': 0, 'initial_pow': 450, 'current_pow': 550, 'owner': True }

'''


class BoardGraph(nx.Graph):
    def __init__(self, **attr):
        super().__init__(**attr)

        ### Data in cache
        self.nodes_cache = []
        self.player_turn = True # True = Host, False = Guest
        ###

        for i in range(16):
            card = {'element': -1, 'initial_pow': -1, 'current_pow': -1, 'owner': True} # owner same as player_turn
            self.add_node(i, data=card)

        # Define a grid graph
        self.add_edge(0, 1)
        self.add_edge(0, 2)
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

    def play_card(self, card, pos):
        allies, ennemies = [], []
        for i_node in self.neighbors(pos):
            node = self.nodes[i_node]['data']
            if node['element'] != -1:
                if node['owner'] == self.player_turn:
                    allies.append(i_node)
                else:
                    ennemies.append(i_node)


        # Verifier trinités et affinités proches (ensembles car ne peut contenir qu'une seule fois une trinité ou une affi)
        affinities = set()
        trinities = set()
        i = 0

        for i_ally in allies:
            ally = self.nodes[i_ally]['data']
            distance = self.get_distance(card.element, ally['element'])
            print(ally)
            print(f"distance : {distance}")
            # S'il y a encore un node à comparer avec l'actuel
            match distance:
                case 0:
                    pass
                case 1:
                    if len(allies) > i + 2:
                        for i_ally_of_ally in allies[i + 1:]:
                            ally_of_ally = self.nodes[i_ally_of_ally]['data']
                            d = self.get_distance(card.element, ally_of_ally['element'])
                            if d == 2:
                                trinities.add(1)
                            elif d == 6:
                                trinities.add(0)
                    # Voisins éloignés
                    for i_neighbor in self.neighbors(i_ally):
                        neighbor = self.nodes[i_neighbor]['data']
                        if neighbor['element'] != -1 and neighbor['owner'] == self.player_turn:
                            d = self.get_distance(card.element, neighbor['element'])
                            if d == 2:
                                trinities.add(1)
                            elif d == 6:
                                trinities.add(0)

                case 2:
                    affinities.add(1)
                    print("Add 1 to affinities")
                    if len(allies) > i + 2:
                        for i_ally_of_ally in allies[i + 1:]:
                            ally_of_ally = self.nodes[i_ally_of_ally]['data']
                            d = self.get_distance(card.element, ally_of_ally['element'])
                            if d == 1:
                                trinities.add(1)

                    for i_neighbor in self.neighbors(i_ally):
                        neighbor = self.nodes[i_neighbor]['data']
                        if neighbor['element'] != -1 and neighbor['owner'] == self.player_turn:
                            d = self.get_distance(card.element, neighbor['element'])
                            if d == 1:
                                trinities.add(1)
                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    affinities.add(-1)
                    print("Add -1 to affinities")
                    if len(allies) > i + 2:
                        for i_ally_of_ally in allies[i + 1:]:
                            ally_of_ally = self.nodes[i_ally_of_ally]['data']
                            d = self.get_distance(card.element, ally_of_ally['element'])
                            if d == 6:
                                trinities.add(-1)

                    for i_neighbor in self.neighbors(i_ally):
                        neighbor = self.nodes[i_neighbor]['data']
                        if neighbor['element'] != -1 and neighbor['owner'] == self.player_turn:
                            d = self.get_distance(card.element, neighbor['element'])
                            if d == 6:
                                trinities.add(-1)

                case 6:
                    if len(allies) > i + 2:
                        for i_ally_of_ally in allies[i + 1:]:
                            ally_of_ally = self.nodes[i_ally_of_ally]['data']
                            d = self.get_distance(card.element, ally_of_ally['element'])
                            if d == 1:
                                trinities.add(0)
                            elif d == 5:
                                trinities.add(-1)
                    for i_neighbor in self.neighbors(i_ally):
                        neighbor = self.nodes[i_neighbor]['data']
                        if neighbor['element'] != -1 and neighbor['owner'] == self.player_turn:
                            d = self.get_distance(card.element, neighbor['element'])
                            if d == 1:
                                trinities.add(0)
                            elif d == 5:
                                trinities.add(-1)
            i += 1


        # Le boost de force = la longueur de l'intersection des ensembles trinities et affinities facteur 100
        print(f"len affinities : {len(affinities)}")
        print(f"affinities {affinities}")
        print(f"len trinities : {len(trinities)}")
        print(f"trinities {trinities}")

        strength_boost = len(trinities | affinities) * 100
        print(f"strength : {strength_boost}")
        card.current_power = card.initial_power + strength_boost


        ### On calcule maintenant les prises
        for i_ennemy in ennemies:
            ennemy = self.nodes[i_ennemy]['data']
            element_gain = self.get_force(card.element, ennemy['element'])
            if card.current_power + element_gain > ennemy['current_pow']:
                ennemy['owner'] = self.player_turn

                #On calcule la chaine x1 dans le cas d'une prise
                for i_e in self.neighbors(i_ennemy):
                    e = self.nodes[i_e]['data']
                    element_gain = self.get_force(ennemy['element'], e['element'])
                    if ennemy['current_pow'] + element_gain > e['current_pow']:
                        e['owner'] = self.player_turn

        ### On ajoute la carte au board
        self.nodes[pos]['data'] = {'element': card.element, 'initial_pow': card.initial_power, 'current_pow': card.current_power, 'owner': card.owner}


        self.player_turn = not self.player_turn

    def to_board_array(self):
        board = []
        # Conversion of each node in card
        for i_node in range(16):
            node = self.nodes[i_node]['data']
            card = Card(0,
                        node['element'],
                        node['initial_pow'],
                        current_power=node['current_pow'],
                        owner=node['owner']
                        )
            board.append(card)

        return board

    # Get the distance between both elements (element 6 and element 1 has a distance of 2 because ->1->2)
    def get_distance(self, element1, element2):
        if element1 <= element2:
            return element2 - element1
        else:
            return 7 - element1 + element2

    # Get element1 vs element2 bonus or malus
    def get_force(self, e1, e2):
        match self.get_distance(e1, e2):
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
