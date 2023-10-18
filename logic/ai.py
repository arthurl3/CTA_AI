import copy
import time
from logic.boardgraph import BoardGraph

counter = 0
bg = BoardGraph()

def evaluer(position):
    if position.datas.current_player:
        return position.datas.score_p1 - position.datas.score_p2
    else:
        return position.datas.score_p2 - position.datas.score_p1

# Fonction Minimax
def minimax(position, profondeur, maximisant):
    if profondeur == 0:
        return evaluer(position)

    if maximisant:
        meilleur_score = -float("inf")
        for coup in coups_possibles(position):
            score = minimax(coup, profondeur - 1, False)
            meilleur_score = max(meilleur_score, score)
        return meilleur_score
    else:
        pire_score = float("inf")
        for coup in coups_possibles(position):
            score = minimax(coup, profondeur - 1, True)
            pire_score = min(pire_score, score)
        return pire_score

# Fonction pour obtenir les coups possibles (à adapter selon le jeu)
def coups_possibles(position):
    global counter
    coups = []
    bg.model = position.datas
    cells_index = bg.get_empty_cells()

    if position.datas.current_player:
        hand = position.hand_p1[:]
    else:
        hand = position.hand_p2[:]

    for cell in cells_index:
        for card in hand:
            if not card.field:
                if position.datas.current_player:

                    hand_p1 = hand[:]
                    hand_p1.remove(card)
                    coup = Position(copy.deepcopy(position.datas), hand_p1, position.hand_p2[:], card=card, cell=cell)
                    bg.model = coup.datas
                    bg.play_card(card, cell)
                    coups.append(coup)
                else:
                    counter += 1
                    hand_p2 = hand[:]
                    hand_p2.remove(card)
                    coup = Position(copy.deepcopy(position.datas), position.hand_p1[:], hand_p2, card=card, cell=cell)
                    bg.model = coup.datas
                    bg.play_card(card, cell)
                    coups.append(coup)



    # À adapter pour générer les coups possibles en fonction de la position
    return coups

def start_ai(position, hand_host, hand_guest):
    initial_position = copy.deepcopy(position)
    position_initiale = Position(initial_position, hand_host[:], hand_guest[:])
    meilleur_coup = None
    meilleur_score = -float("inf")
    profondeur = 1
    # Enregistrez le temps de départ
    temps_debut = time.time()

    for coup in coups_possibles(position_initiale):
        score = minimax(coup, profondeur=profondeur, maximisant=False)
        if score > meilleur_score:
            meilleur_score = score
            meilleur_coup = coup

    temps_fin = time.time()
    temps_ecoule = temps_fin - temps_debut


    ###  RESULTS ###
    print(f"Profondeur d'exploration : {profondeur}")
    print("Temps écoulé : {:.6f} secondes".format(temps_ecoule))
    if temps_ecoule > float(0):
        print(f"A évalué {counter} positions, soit {counter//temps_ecoule} évaluations par secondes")
    print("Meilleur coup :", meilleur_coup)
    print("Meilleur score :", meilleur_score)
    ################

    return meilleur_coup.coup_card, meilleur_coup.coup_cell


# OPTIMISATION - Au lieu de stocker le coup dans une position, on cherche le noeud qui était vide mais ne l'est plus
# def get_coup(self, position):
#     for i in range(16):
#         if position.datas.nodes['data']['id'] != -1:
#             if self.initial_position.model.nodes[i]['data']['id'] =! position.datas.nodes['data']['id']:
#                 pass


class Position:
    def __init__(self, boarddata, h_p1, h_p2, card=None, cell=None):
        self.datas = boarddata
        self.hand_p1 = h_p1
        self.hand_p2 = h_p2
        self.coup_card = card
        self.coup_cell = cell
