from logic.boarddatas import BoardDatas
from logic.staticboarddatas import StaticBoardDatas
from models.card import Card

'''
Contient les données du plateau de jeu sous forme de graphe en grille

Seules les données essentielles sont représentées ici
=> chaque numéro de node représente sa position à plat sur le plateau
(4x4 => 16) (EXEMPLE : la position du node (x, y) = (2, 2) devient 10)
=> Les donnée d'un node représente une carte sous forme d'un dictionnaire :
Exemple:  carte = {'element': 0, 'initial_pow': 450, 'current_pow': 550, 'owned_by_p1': True }

'''


def get_element_distance(element1, element2):
    if element1 <= element2:
        return element2 - element1
    else:
        return 7 - element1 + element2


def get_force(e1, e2):
    match get_element_distance(e1, e2):
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


class Party:
    def __init__(self, settings=None, **attr):
        super().__init__(**attr)
        self.board_datas = BoardDatas()
        self.static_datas = StaticBoardDatas(settings)
        # Sert à calculer si on appelle la fonction de calcul des points ou non dans le calcul d'affinité
        self.pos_flag = True
        self.field_play = False

    # i_node is the node index where the card is played
    def play_card(self, card, i_node):
        if card['field']:
            self.field_play = True
            self.board_datas.field_turn_left = 3
            self.board_datas.field_power = card['initial_power']
            self.board_datas.field_element = card['element']
            # Calcule des nouvelles forces
            for i_n in self.board_datas.nodes:
                self.update_power(i_n, self.board_datas.nodes[i_n]['data'])
            self.field_play = False
        else:
            if card['leader']:
                self.enable_leader()

            # On convertit la carte en data node
            self.board_datas.add_node(i_node, data=card)
            self.board_datas.add_edges(i_node)

            self.pos_flag = False
            # Calcule des affinités et des trinités
            self.update_power(i_node, card)
            self.pos_flag = True

            # Calcule des reprises
            if self.current_player_control_leader():
                self.calculate_taken_ennemies(i_node, card, chain=2)
            else:
                self.calculate_taken_ennemies(i_node, card, chain=1)

                # Calcule des nouvelles forces
                for i_n in self.board_datas.nodes:
                    n = self.board_datas.nodes[i_n]['data']
                    self.update_power(i_n, n)

                    # Si le leader est de nouveau contrôlé par le joueur actuel après reprise
                    if n['leader']:
                        if n['original_owner'] == self.board_datas.current_player:
                            self.enable_leader()

            self.board_datas.field_turn_left -= 1
            self.board_datas.current_player = not self.board_datas.current_player

    def update_power(self, i_node, node):
        # Calcule des affinités et des trinités
        node['current_pow'] = node['initial_pow'] + self.get_power_boost_with_affinities_and_trinities(i_node, node)

        if self.board_datas.field_element == node['element']:
            node['current_pow'] += self.board_datas.field_power

    def calculate_taken_ennemies(self, pos, node, chain):
        _, ennemies = self.get_allies_and_ennemies(pos)
        # On calcule maintenant les prises
        for i_enemy in ennemies:
            enemy = self.board_datas.nodes[i_enemy]['data']
            element_gain = get_force(node['element'], enemy['element'])
            if node['current_pow'] + element_gain > enemy['current_pow']:
                enemy['owned_by_p1'] = self.board_datas.current_player
                self.increase_score(2)

                # On enlève le flag de possession du leader s'il est capturé
                if enemy['leader'] and enemy['original_owner'] == (not self.board_datas.current_player):
                    self.disable_leader()

                # Récursif si chaine > 0
                if chain > 0:
                    self.calculate_taken_ennemies(i_enemy, enemy, chain=chain - 1)

    def increase_score(self, points):
        if self.board_datas.current_player:
            self.board_datas.score_p1 += points
        else:
            self.board_datas.score_p2 += points

    def enable_leader(self):
        if self.board_datas.current_player:
            self.board_datas.p1_control_leader = True
        else:
            self.board_datas.p2_control_leader = True

    # Met à False la possession du leader par le joueur non actif
    def disable_leader(self):
        if self.board_datas.current_player:
            self.board_datas.p2_control_leader = False
        else:
            self.board_datas.p1_control_leader = False

    def current_player_control_leader(self):
        if self.board_datas.current_player:
            return self.board_datas.p1_control_leader
        else:
            return self.board_datas.p2_control_leader

    # Method to light the get_power_boost_with_affinities_and_trinities method (verify direct neighbors)
    def verify_proximity(self, node, allies, trinities, possible_trinity_distances, trinity_distances):
        for i_ally_of_ally in allies:
            ally_of_ally = self.board_datas.nodes[i_ally_of_ally]['data']
            d = get_element_distance(node['element'], ally_of_ally['element'])
            for i in range(len(possible_trinity_distances)):
                if d == possible_trinity_distances[i]:
                    trinities.add(trinity_distances[i])

    # 2nd Method to light the get_power_boost_with_affinities_and_trinities
    def verify_neighborhood(self, i_node, node, trinities, possible_trinity_distances, trinity_distances):
        # Voisins éloignés
        allies, _ = self.get_allies_and_ennemies(i_node)
        for i_neighbor in allies:
            neighbor = self.board_datas.nodes[i_neighbor]['data']
            d = get_element_distance(node['element'], neighbor['element'])
            for i in range(len(possible_trinity_distances)):
                if d == possible_trinity_distances[i]:
                    trinities.add(trinity_distances[i])

    def get_power_boost_with_affinities_and_trinities(self, i_node, node):
        allies, _ = self.get_allies_and_ennemies(i_node)
        # Verifier trinités et affinités proches (ensemble ne peut contenir qu'une seule fois tri ou une aff)
        affinities = set()
        trinities = set()
        i = 0

        for i_ally in allies:
            ally = self.board_datas.nodes[i_ally]['data']
            element_distance = get_element_distance(node['element'], ally['element'])
            # S'il y a encore un node à comparer avec l'actuel
            match element_distance:
                case 0:
                    pass
                case 1:
                    if len(allies) > i + 1:
                        self.verify_proximity(node, allies[i + 1:], trinities, [2, 6], [1, 0])
                    self.verify_neighborhood(i_ally, node, trinities, [2, 6], [1, 0])

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

        if not self.field_play and len(trinities) > 0 and self.pos_flag:
            self.increase_score(1)

        return len(trinities | affinities) * 100

    def to_board_array(self):
        board = []
        # Conversion of each node in card
        for i_node in range(16):
            board.append(self.get_card_from_node(i_node))
        return board

    # Get the distance between both elements (element 6 and element 1 has a distance of 2 because ->1->2)

    # Get element1 vs element2 bonus or malus

    def get_allies_and_ennemies(self, id_node):
        node = self.board_datas.nodes[id_node]['data']
        allies, ennemies = [], []
        for i_node in self.board_datas.neighbors(id_node):
            neighbor = self.board_datas.nodes[i_node]['data']
            if neighbor['owned_by_p1'] == node['owned_by_p1']:
                allies.append(i_node)
            else:
                ennemies.append(i_node)
        return allies, ennemies

    def get_empty_cells(self):
        empty_cells = []
        for i_node in range(16):
            if not self.board_datas.has_node(i_node):
                empty_cells.append(i_node)
        return empty_cells

    def get_hand(self, player):
        if player == 1:
            hand_card_data = self.static_datas.deck_p1[:6]
        else:
            hand_card_data = self.static_datas.deck_p2[:6]
        hand = []
        for card_data in hand_card_data:
            hand.append(self.get_card_from_card_data(card_data))
        return hand

    def get_card_from_node(self, i_node):
        if self.board_datas.has_node(i_node):
            node = self.board_datas.nodes[i_node]['data']
        else:
            return None
        return Card(a_id=node['id'],
                    element=node['element'],
                    power=node['initial_pow'],
                    current_power=node['current_pow'],
                    owned_by_p1=node['owned_by_p1'],
                    leader=node['leader']
                    )

    def get_card_from_card_data(self, card_data):
        return Card(a_id=card_data['id'],
                    element=card_data['element'],
                    power=card_data['initial_pow'],
                    current_power=card_data['current_pow'],
                    owned_by_p1=card_data['owned_by_p1'],
                    leader=card_data['leader']
                    )