import json
from config import Config
from models.card import Card
import copy

from models.deck import Deck


# Return a list of all existing cards
def load_cards():
    cards = []
    with open(Config.DATA_PATH) as file:
        data = json.load(file)
        for card in data['cards']:
            c = Card(card['id'], card['element'], card['power'])
            cards.append(c)
    return cards

# Return an object deck by binding the deck id from the json data file list of decks
def load_deck(deck_index):
    remettre_bien_les_ids()
    remettre_bien_les_elements()

    deck_cards = []
    card_list = load_cards()

    # Chargement des datas
    with open(Config.DATA_PATH) as file:
        data = json.load(file)

    deck = data['decks'][deck_index]
    #Get the list of card id
    for card in deck:
        id = card['id']
        for c in card_list:
            if c.id == id:
                deck_cards.append(copy.deepcopy(c))

    return Deck(deck_cards)


#Remet de l'ordre dans le fichier data (tri par attribut)
def remettre_bien_les_elements():
    cards = []
    data = None
    with open(Config.DATA_PATH) as file:
        data = json.load(file)
        data['cards'] = sorted(data['cards'], key=lambda k: k.get('element', 0), reverse=True)

    with open(Config.DATA_PATH, 'w') as file:
        json.dump(data, file, indent=4)
    # for line in lines:
    #     print(line)

def remettre_bien_les_ids():
    cards = []
    i = 0
    with open(Config.DATA_PATH, 'r') as file:
        data = json.load(file)
        for card in data['cards']:
            card['id'] = i
            i += 1
    with open(Config.DATA_PATH, 'w') as file:
        json.dump(data, file, indent=4)


def insert_deck(deck):
    id = -1
    data = None
    # On ouvre pour connaitre le dernier id
    with open(Config.DATA_PATH) as file:
        data = json.load(file)

    # On rouvre en écriture pour mettre à jour les données avec json.dump
    with open(Config.DATA_PATH, 'w') as file:
        data['decks'].append(deck)
        json.dump(data, file, indent=4)




