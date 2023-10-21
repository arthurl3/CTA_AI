import loader
from logic.ai import AI
from logic.party import Party

class GameViewModel:
    def __init__(self, settings, view):
        self.party = Party(settings)
        self.host_is_p1 = settings.host_is_p1
        self.view = view
        self.deck_host_repr = None
        self.update_deck_host_repr()

        # Game view useful attributes
        self.selected_card = None
        self.card_to_add = None

        self.draw_host_allowed = 2
        self.draw_guest_allowed = 2

        # GESTION DU MODE ASSISTANT
        if settings.mode == 1:
            # Ajouter 6 Emplacements vides à deck_host
            if settings.host_is_p1:
                self.deck_host_repr = [self.party.static_datas.deck_p1[0]]
                self.deck_host_repr.extend([None for i in range(5)])
                self.deck_host_repr.extend(self.party.static_datas.deck_p1[1])
            else:
                self.deck_host_repr = [self.party.static_datas.deck_p2[0]]
                self.deck_host_repr.extend([None for i in range(5)])
                self.deck_host_repr.extend(self.party.static_datas.deck_p2[1])


    def ai_play(self):
        ai = AI(board=self.party)
        (position, card) = ai.start_ai()
        self.play_card(position, card)

    # Logic when a player play a card
    def play_card(self, position, card=None):
        if None in self.deck_host_repr[:6]:
            return
        if self.cell_already_played(position):
            return
        if card:
            self.selected_card = card
        if not self.selected_card:
            return

        print(self.selected_card)
        # Conversion before playing
        self.party.play_card(self.party.static_datas.get_node_data_from_card(self.selected_card), position)
        self.draw()
        self.update_deck_host_repr()
        self.view.update()



    # Changement d'une carte en main selectionnée par celle du dessus du paquet (draw mais sur demande)
    def change_card(self):
        if self.draw_host_allowed > 0 and self.selected_card:
            self.deck_host_repr.remove(self.selected_card)
            self.selected_card = None
            self.draw_host_allowed -= 1
            self.view.update()

    # Jette une carte à la poubelle
    def throw_card(self):
        if self.selected_card:
            self.deck_host_repr.remove(self.selected_card)
            self.selected_card = None
            self.view.update()

    def add_card_to_hand(self):
        if not self.card_to_add:
            return
        if not None in self.deck_host_repr[:6]:
            return

        for i in range(6):
            if not self.deck_host_repr[i]:
                self.deck_host_repr[i] = self.card_to_add
                break

        # On supprime sa double présence dans le deck
        counter = 0
        for i in range(len(self.deck_host_repr)):
            if self.deck_host_repr[i]:
                if self.deck_host_repr[i].id == self.card_to_add.id:
                    if counter == 1:
                        self.deck_host_repr.pop(i)
                        self.card_to_add = None
                        self.view.update()
                        break
                    else:
                        counter += 1

    def change_card_to_add(self, card_txt: str):
        a_id = card_txt.split()[0]
        self.card_to_add = loader.load_card_from_id(a_id)
        self.card_to_add.owned_by_p1 = True

    def draw(self):
        card_id = self.selected_card.id
        if not self.party.board_datas.current_player:
            self.party.static_datas.remove_card_from_deck(id=card_id, player=1)
        else:
            self.party.static_datas.remove_card_from_deck(id=card_id, player=2)
        self.selected_card = None

    def update_deck_host_repr(self):
        if self.host_is_p1:
            self.deck_host_repr = self.party.get_hand(player=1)
        else:
            self.deck_host_repr = self.party.get_hand(player=2)

    # When a player click on a card in his hand
    def set_selected(self, card):
        self.selected_card = card

    def get_hand(self):
        return self.deck_host_repr[:6]

    def get_scores(self):
        return self.party.board_datas.score_p1, self.party.board_datas.score_p2

    def get_host_score(self):
        if self.host_is_p1:
            return self.party.board_datas.score_p1
        else:
            return self.party.board_datas.score_p2

    def get_guest_score(self):
        if self.host_is_p1:
            return self.party.board_datas.score_p2
        else:
            return self.party.board_datas.score_p1

    def get_turn_counter(self):
        return len(self.party.board_datas.nodes)

    def get_board(self):
        return self.party.to_board_array()

    def cell_already_played(self, i_cell):
        return self.party.board_datas.has_node(i_cell)