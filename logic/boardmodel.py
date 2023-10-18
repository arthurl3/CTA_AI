import networkx as nx

'''
Contient les données du plateau de jeu sous forme de graphe en grille

Seules les données essentielles sont représentées ici
=> chaque numéro de node représente sa position à plat sur le plateau
(4x4 => 16) (EXEMPLE : la position du node (x, y) = (2, 2) devient 10)
=> Les donnée d'un node représente une carte sous forme d'un dictionnaire :
Exemple:  carte = {'element': 0, 'initial_pow': 450, 'current_pow': 550, 'owned_by_p1': True }

'''


class BoardModel(nx.Graph):
    def __init__(self, **attr):
        super().__init__(**attr)

        self.current_player = True  # True p1 false p2
        self.score_p1 = 0
        self.score_p2 = 0

        self.p1_control_leader = False
        self.p2_control_leader = False

        # FIELD HANDLING
        self.field_play = False
        self.field_turn_left = 0
        self.field_power = 0
        self.field_element = -1

        self.special_ability_p1 = None
        self.special_ability_p2 = None
        self.hand_host = []
        self.hand_guest = []
        # Sert à calculer si on appelle la fonction de calcul des points ou non dans le calcul d'affinité
        self.pos_flag = True

    # Ajoute les les aretes au fur et à mesure
    def add_edges(self, position):
        x = position % 4
        to_add = []

        if position > 4:
            to_add.append(position - 4)
        if x == 3:
            to_add.append(position + 1)
        if position < 12:
            to_add.append(position + 4)
        if x == 0:
            to_add.append(position - 1)

        for i_node in to_add:
            if self.has_node(i_node):
                self.add_edge(position, i_node)
