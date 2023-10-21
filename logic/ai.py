import copy
import time


class AI:
    def __init__(self, board):
        self.initial_board = board
        self.party = copy.deepcopy(board)
        self.counter = 0

    def evaluer(self, position):
        # Calcul du nombre de noeud final
        self.counter += 1
        if position.position_datas.current_player:
            return position.position_datas.score_p1 - position.position_datas.score_p2
        else:
            return position.position_datas.score_p2 - position.position_datas.score_p1

    # Fonction Minimax
    def minimax(self, position, profondeur, maximisant):
        if profondeur == 0:
            return self.evaluer(position)

        if maximisant:
            meilleur_score = -float("inf")
            for coup in self.coups_possibles(position):
                score = self.minimax(coup, profondeur - 1, False)
                meilleur_score = max(meilleur_score, score)
            return meilleur_score
        else:
            pire_score = float("inf")
            for coup in self.coups_possibles(position):
                score = self.minimax(coup, profondeur - 1, True)
                pire_score = min(pire_score, score)
            return pire_score

    # Fonction pour obtenir les coups possibles (à adapter selon le jeu)
    def coups_possibles(self, position):
        coups = []
        self.party.board_datas = position.position_datas
        cells_index = self.party.get_empty_cells()

        if position.position_datas.current_player:
            hand = position.hand_p1[:]
        else:
            hand = position.hand_p2[:]

        for cell in cells_index:
            for card in hand:
                if not card['field']:
                    if position.position_datas.current_player:
                        hand_p1 = hand[:]
                        hand_p1.remove(card)
                        coup = Position(copy.deepcopy(position.position_datas), hand_p1, position.hand_p2[:])
                        self.party.board_datas = coup.position_datas
                        self.party.play_card(card, cell)
                        coups.append(coup)
                    else:
                        hand_p2 = hand[:]
                        hand_p2.remove(card)
                        coup = Position(copy.deepcopy(position.position_datas), position.hand_p1[:], hand_p2)
                        self.party.board_datas = coup.position_datas
                        self.party.play_card(card, cell)
                        coups.append(coup)
        return coups

    def start_ai(self):
        meilleur_coup = None
        meilleur_score = -float("inf")
        profondeur = 2

        hand_p1 = self.party.static_datas.deck_p1[:6]
        hand_p2 = self.party.static_datas.deck_p2[:6]

        datas = copy.deepcopy(self.party.board_datas)
        position_initiale = Position(datas, hand_p1, hand_p2)

        # Stop calculate when board is full
        if len(self.initial_board.get_empty_cells()) < 1:
            return None, None

        if profondeur > len(self.initial_board.get_empty_cells()):
            profondeur = len(self.initial_board.get_empty_cells())


        # Start time
        temps_debut = time.time()

        for coup in self.coups_possibles(position_initiale):
            score = self.minimax(coup, profondeur=profondeur - 1, maximisant=True)
            if score > meilleur_score:
                meilleur_score = score
                meilleur_coup = coup

        # End time
        temps_fin = time.time()
        temps_ecoule = temps_fin - temps_debut

        #  RESULTS ###
        print(f"Profondeur d'exploration : {profondeur}")
        print("Temps écoulé : {:.6f} secondes".format(temps_ecoule))
        if temps_ecoule > float(0):
            print(f"A évalué {self.counter} positions, soit {self.counter // temps_ecoule} évaluations par secondes")
        print("Meilleur coup :", meilleur_coup)
        print("Meilleur score :", meilleur_score)
        ################

        self.party.board_datas = meilleur_coup.position_datas
        (meilleur_coup_position, meilleur_coup_card) = self.get_play(meilleur_coup.position_datas)
        return meilleur_coup_position, meilleur_coup_card


    # OPTIMISATION - Au lieu de stocker le coup dans une position, on cherche le nœud qui était vide, mais ne l'est
    # plus en comparant le board au tour t et t+1
    def get_play(self, board_next):
        for i_node in board_next.nodes:
            if not self.initial_board.board_datas.has_node(i_node):
                return i_node, self.party.get_card_from_card_data(self.party.board_datas.nodes[i_node]['data'])

class Position:
    def __init__(self, position_datas, h_p1, h_p2):
        self.position_datas = position_datas
        self.hand_p1 = h_p1
        self.hand_p2 = h_p2
