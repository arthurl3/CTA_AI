from logic.boardmodel import BoardModel
from models.card import Card

'''
Contient les données du plateau de jeu sous forme de graphe en grille

Seules les données essentielles sont représentées ici
=> chaque numéro de node représente sa position à plat sur le plateau
(4x4 => 16) (EXEMPLE : la position du node (x, y) = (2, 2) devient 10)
=> Les donnée d'un node représente une carte sous forme d'un dictionnaire :
Exemple:  carte = {'element': 0, 'initial_pow': 450, 'current_pow': 550, 'owned_by_p1': True }

'''


class BoardGraph:
    def __init__(self, **attr):
        super().__init__(**attr)
        self.model = BoardModel()

    # i_node is the node index where the card is played
    def play_card(self, card, i_node):
        if card.field:
            self.model.field_play = True
            self.model.field_turn_left = 3
            self.model.field_power = card.initial_power
            self.model.field_element = card.element

            # Calcule des nouvelles forces
            for i_n in self.model.nodes:
                self.update_power(i_n)

        else:
            if card.leader:
                self.enable_leader()

            ### On convertit la carte en data node
            node = self.get_node_data_from_card(card)
            self.model.add_node(i_node, data=node)
            self.model.add_edges(i_node)

            self.model.pos_flag = False
            # Calcule des affinités et des trinités
            self.update_power(i_node)
            self.model.pos_flag = True

            # Calcule des reprises
            if self.current_player_control_leader():
                self.calculate_taken_ennemies(i_node, chain=2)
            else:
                self.calculate_taken_ennemies(i_node, chain=1)

                # Calcule des nouvelles forces
                for i_n in self.model.nodes:
                    self.update_power(i_n)

                    # Si le leader est de nouveau controlé par le joueur actuel après reprise
                    if self.model.nodes[i_n]['data']['leader']:
                        if self.model.nodes[i_n]['data']['original_owner'] == self.model.current_player:
                            self.enable_leader()

            if self.model.field_turn_left > 0:
                self.model.field_turn_left -= 1

            self.model.current_player = not self.model.current_player
        self.model.field_play = False

    def set_special_abilities(self, sa_p1, sa_p2):
        self.model.special_ability_p1 = sa_p1
        self.model.special_ability_p2 = sa_p2

    def update_power(self, i_node):
        node = self.model.nodes[i_node]['data']
        # Calcule des affinités et des trinités
        node['current_pow'] = node['initial_pow'] + self.get_power_boost_with_affinities_and_trinities(i_node)

        if self.model.field_turn_left > 0 and self.model.field_element == node['element']:
            node['current_pow'] += self.model.field_power

    def calculate_taken_ennemies(self, pos, chain):
        node = self.model.nodes[pos]['data']
        _, ennemies = self.get_allies_and_ennemies(pos)

        ### On calcule maintenant les prises
        for i_ennemy in ennemies:
            ennemy = self.model.nodes[i_ennemy]['data']
            element_gain = self.get_force(node['element'], ennemy['element'])
            if node['current_pow'] + element_gain > ennemy['current_pow']:
                ennemy['owned_by_p1'] = self.model.current_player
                self.increase_score(2)

                # On enlève le flag de possession du leader s'il est capturé
                if ennemy['leader'] and ennemy['original_owner'] == (not self.model.current_player):
                    self.disable_leader()

                # Récursif si chaine > 0
                if chain > 0:
                    self.calculate_taken_ennemies(i_ennemy, chain=chain - 1)

    def increase_score(self, points):
        if self.model.current_player:
            self.model.score_p1 += points
        else:
            self.model.score_p2 += points

    def enable_leader(self):
        if self.model.current_player:
            self.model.p1_control_leader = True
        else:
            self.model.p2_control_leader = True

    # Met à False la possession du leader par le joueur non actif
    def disable_leader(self):
        if self.model.current_player:
            self.model.p2_control_leader = False
        else:
            self.model.p1_control_leader = False

    def current_player_control_leader(self):
        if self.model.current_player:
            return self.model.p1_control_leader
        else:
            return self.model.p2_control_leader


    # Method to light the get_power_boost_with_affinities_and_trinities method (verify direct neighbors)
    def verify_proximity(self, node, allies, trinities, possible_trinity_distances, trinity_distances):
        for i_ally_of_ally in allies:
            ally_of_ally = self.model.nodes[i_ally_of_ally]['data']
            d = self.get_element_distance(node['element'], ally_of_ally['element'])
            for i in range(len(possible_trinity_distances)):
                if d == possible_trinity_distances[i]:
                    trinities.add(trinity_distances[i])

    # 2nd Method to light the get_power_boost_with_affinities_and_trinities
    def verify_neighborhood(self, i_node, node, trinities, possible_trinity_distances, trinity_distances):
        # Voisins éloignés
        allies, _ = self.get_allies_and_ennemies(i_node)
        for i_neighbor in allies:
            neighbor = self.model.nodes[i_neighbor]['data']
            d = self.get_element_distance(node['element'], neighbor['element'])
            for i in range(len(possible_trinity_distances)):
                if d == possible_trinity_distances[i]:
                    trinities.add(trinity_distances[i])

    def get_power_boost_with_affinities_and_trinities(self, i_node):
        allies, _ = self.get_allies_and_ennemies(i_node)
        node = self.model.nodes[i_node]['data']
        # Verifier trinités et affinités proches (ensembles car ne peut contenir qu'une seule fois une trinité ou une affi)
        affinities = set()
        trinities = set()
        i = 0

        for i_ally in allies:
            ally = self.model.nodes[i_ally]['data']
            element_distance = self.get_element_distance(node['element'], ally['element'])
            # S'il y a encore un node à comparer avec l'actuel
            match element_distance:
                case 0:
                    pass
                case 1:
                    if len(allies) > i + 1:
                        self.verify_proximity(node, allies[i + 1:], trinities, [2, 6], [1, 0])
                    self.verify_neighborhood(i_ally, node,  trinities, [2, 6], [1, 0])

                case 2:
                    affinities.add(1)
                    if len(allies) > i + 1:
                        self.verify_proximity(node, allies[i + 1:], trinities, [1], [1])
                    self.verify_neighborhood(i_ally, node, trinities, [1], [1])

                case 3:
                    pass
                case 4:
                    pass
                case 5:
                    affinities.add(-1)
                    if len(allies) > i + 1:
                        self.verify_proximity(node, allies[i + 1:], trinities, [6], [-1])
                    self.verify_neighborhood(i_ally, node, trinities, [6], [-1])

                case 6:
                    if len(allies) > i + 1:
                        self.verify_proximity(node, allies[i + 1:], trinities, [1, 5], [0, -1])
                    self.verify_neighborhood(i_ally, node, trinities, [1, 5], [0, -1])
            i += 1

        if len(trinities) > 0 and self.model.pos_flag and not self.model.field_play:
            self.increase_score(1)

        return len(trinities | affinities) * 100

    def get_node_data_from_card(self, card):
        return {'element': card.element, 'initial_pow': card.initial_power,
                'current_pow': card.current_power, 'owned_by_p1': card.owned_by_p1,
                'leader': card.leader, 'original_owner': card.owned_by_p1}

    def get_card_from_node(self, i_node):
        node = None
        if self.model.has_node(i_node):
            node = self.model.nodes[i_node]['data']
        else:
            return None

        return Card(0,
                    element=node['element'],
                    power=node['initial_pow'],
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

    def get_allies_and_ennemies(self, id_node):
        node = self.model.nodes[id_node]['data']
        allies, ennemies = [], []

        for i_node in self.model.neighbors(id_node):
            neighbor = self.model.nodes[i_node]['data']
            if neighbor['element'] != -1:
                if neighbor['owned_by_p1'] == node['owned_by_p1']:
                    allies.append(i_node)
                else:
                    ennemies.append(i_node)
        return allies, ennemies

    def get_empty_cells(self):
        empty_cells = []
        for i_node in range(16):
            if not self.model.has_node(i_node):
                empty_cells.append(i_node)
        return empty_cells

