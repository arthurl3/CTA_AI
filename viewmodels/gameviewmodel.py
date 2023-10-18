from random import shuffle
import loader
from logic.boardgraph import BoardGraph
from logic import ai as ai

class GameViewModel:
    def __init__(self, settings, view):

        self.settings = settings
        self.view = view

        self.selected_card = None
        self.card_to_add = None

        self.current_player = True  # True is p1, False is p2
        self.turn_counter = 0  # Turn counter

        self.score_host = 0
        self.score_guest = 0

        self.draw_host_allowed = 2
        self.draw_guest_allowed = 2

        self.board = [None for i in range(16)]
        self.board_graph = BoardGraph()

        self.deck_host = []
        self.deck_guest = []

        #### DECK LOADING ###
        (tmp_deck_host, sa1) = loader.load_deck(settings.deck_host)
        (tmp_deck_guest, sa2) = loader.load_deck(settings.deck_guest)

        c_tmp1 = tmp_deck_host[0]
        c_tmp2 = tmp_deck_guest[0]
        tmp_deck_host.remove(c_tmp1)
        tmp_deck_guest.remove(c_tmp2)
        shuffle(tmp_deck_host)
        shuffle(tmp_deck_guest)

        self.deck_host.append(c_tmp1)
        self.deck_guest.append(c_tmp2)
        self.deck_host.extend(tmp_deck_host[:])
        self.deck_guest.extend(tmp_deck_guest[:])

        if self.settings.host_is_p1:
            self.board_graph.set_special_abilities(sa1, sa2)
            for card in self.deck_guest:
                card.owned_by_p1 = False
        else:
            self.board_graph.set_special_abilities(sa2, sa1)
            for card in self.deck_host:
                card.owned_by_p1 = False

        ###


        ### GESTION DU MODE ASSISTANT ###
        if self.settings.mode == 1:
            # Ajouter 6 Emplacements vides à deck_host
            tmp_deck_host = [self.deck_host[0]]
            tmp_deck_host.extend([None for i in range(5)])
            tmp_deck_host.extend(self.deck_host[1:])
            self.deck_host = tmp_deck_host



    # When a player click on a card in his hand
    def set_selected(self, card):
        self.selected_card = card

    def get_hand(self):
        return self.deck_host[:6]

    # Logic when a player play a card
    def play_card(self, position, card=None):
        if None in self.deck_host[:6]:
            return
        if self.board[position]:
            return
        if card:
            self.selected_card = card
        if not self.selected_card:
            return

        # Verification du tour de host si c'est lui qui clique
        # if not self.settings.host_is_p1 == self.current_player and not card:
        #     return

        self.board_graph.play_card(self.selected_card, position)

        if not self.selected_card.field:
            if self.settings.host_is_p1:
                self.score_host = self.board_graph.model.score_p1
                self.score_guest = self.board_graph.model.score_p2
            else:
                self.score_host = self.board_graph.model.score_p2
                self.score_guest = self.board_graph.model.score_p1

            self.draw()
            self.turn_counter += 1
            self.current_player = not self.current_player

        self.board = self.board_graph.to_board_array()
        self.view.update()



    def ai_play(self):
        (card, position) = ai.start_ai(self.board_graph.model, self.deck_host[:6], self.deck_guest[:6])
        self.play_card(position, card)

    def draw(self):
        if self.current_player:
            self.deck_host.remove(self.selected_card)
        else:
            self.deck_guest.remove(self.selected_card)
        self.selected_card = None

    # Changement d'une carte en main selectionnée par celle du dessus du paquet (draw mais sur demande)
    def change_card(self):
        if self.draw_host_allowed > 0 and self.selected_card:
            self.deck_host.remove(self.selected_card)
            self.selected_card = None
            self.draw_host_allowed -= 1
            self.view.update()

    def throw_card(self):
        if self.selected_card:
            self.deck_host.remove(self.selected_card)
            self.selected_card = None
            self.view.update()

    def add_card_to_hand(self):
        if not self.card_to_add:
            return
        if not None in self.deck_host[:6]:
            return

        for i in range(6):
            if not self.deck_host[i]:
                self.deck_host[i] = self.card_to_add
                break

        # On supprime sa double présence dans le deck
        counter = 0
        for i in range(len(self.deck_host)):
            if self.deck_host[i]:
                if self.deck_host[i].id == self.card_to_add.id:
                    if counter == 1:
                        self.deck_host.pop(i)
                        self.card_to_add = None
                        self.view.update()
                        break
                    else:
                        counter += 1

    def change_card_to_add(self, card_txt: str):
        a_id = card_txt.split()[0]
        self.card_to_add = loader.load_card_from_id(a_id)
        self.card_to_add.owned_by_p1 = True
