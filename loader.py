import json
from config import Config
from models.card import Card
import copy

# Return a list of all existing cards object
def load_cards():
    #Tris en Debug pour garder le fichier propre
    remettre_bien_les_ids()
    remettre_bien_les_elements()
    cards = []
    with open(Config.CARDS_DATA_PATH) as file:
        data = json.load(file)
        for card in data['cards']:
            c = Card(card['id'], card['element'], card['power'])
            cards.append(c)
    return cards

#Return the list of all decks
def load_decks():
    # Chargement des datas
    with open(Config.DECKS_DATA_PATH) as file:
        data = json.load(file)
        return data['decks']

# !!!!!  A changer !!!!!
# Return an object deck by binding the deck name from the json data file list of decks
def load_deck(deck_index):
    card_list = load_cards()
    deck_cards = []
    deck = {}

    with open(Config.DECKS_DATA_PATH) as file:
        data = json.load(file)

    for d in data['decks']:
        if d['name'] == str(deck_index):
            deck = d

    #Get the list of card id
    for card_id in deck['cards']:
        for c in card_list:
            if c.id == card_id:
                deck_cards.append(copy.deepcopy(c))

    return deck_cards

# Insère un deck mais il faut encore insérer le nom à la main (sinon le nom est donné par défaut)
def insert_deck(cards):
    data = None
    deck = {}

    # On ouvre les decks
    with open(Config.DECKS_DATA_PATH) as file:
        data = json.load(file)

    deck['name'] = str(len(data['decks']) + 1)
    deck['cards'] = [card for card in cards]

    # On rouvre en écriture pour mettre à jour les données avec json.dump
    with open(Config.DECKS_DATA_PATH, 'w') as file:
        data['decks'].append(deck)
        json.dump(data, file, indent=4)


###### NON PRODUCTION FUNCTION #######
#Remet de l'ordre dans le fichier data (tri par attribut)
def remettre_bien_les_elements():
    cards = []
    data = None
    with open(Config.CARDS_DATA_PATH) as file:
        data = json.load(file)
        data['cards'] = sorted(data['cards'], key=lambda k: k.get('element', 0), reverse=True)

    with open(Config.CARDS_DATA_PATH, 'w') as file:
        json.dump(data, file, indent=4)
    # for line in lines:
    #     print(line)

def remettre_bien_les_ids():
    cards = []
    i = 0
    with open(Config.CARDS_DATA_PATH, 'r') as file:
        data = json.load(file)
        for card in data['cards']:
            card['id'] = i
            i += 1
    with open(Config.CARDS_DATA_PATH, 'w') as file:
        json.dump(data, file, indent=4)






