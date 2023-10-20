import json
from config import Config
from models.card import Card
import copy

# Return a list of all existing cards object
def load_cards():
    #Tris en Debug pour garder le fichier propre
    #sort_cards()
    cards = []
    with open(Config.CARDS_DATA_PATH) as file:
        data = json.load(file)

        for card in data['cards']:

            type = 0
            try:
                type = card['type']
            except KeyError:
                pass

            c = None
            if type == 1:  # Cas d'un terrain
                c = Card(card['id'], card['element'], card['power'], field=True)
            else:
                c = Card(card['id'], card['element'], card['power'])
            cards.append(c)
    return cards

#Return the list of all decks
def load_decks():
    # Chargement des datas
    with open(Config.DECKS_DATA_PATH) as file:
        data = json.load(file)
        return data['decks']


def load_card_from_id(id):
    data = None
    with open(Config.CARDS_DATA_PATH) as file:
        data = json.load(file)

    for card in data['cards']:
        if card['id'] == int(id):
            return Card(card['id'], card['element'], card['power'])


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

    deck_cards[0].leader = True
    return (deck_cards, deck['special_ability'])

# Insère un deck mais il faut encore insérer le nom à la main (sinon le nom est donné par défaut)
def insert_deck(cards, deck_name, special_ability):
    data = None
    deck = {}

    # On ouvre les decks
    with open(Config.DECKS_DATA_PATH) as file:
        data = json.load(file)

    deck['name'] = deck_name
    deck['special_ability'] = special_ability
    deck['cards'] = [card for card in cards]


    # On rouvre en écriture pour mettre à jour les données avec json.dump
    with open(Config.DECKS_DATA_PATH, 'w') as file:
        data['decks'].append(deck)
        json.dump(data, file, indent=4)


###### NON PRODUCTION FUNCTION #######
#Remet de l'ordre dans le fichier data (tri par attribut)
def sort_cards():
    data = None

    with open(Config.CARDS_DATA_PATH) as file:
        data = json.load(file)
        data['cards'] = sorted(data['cards'], key=lambda k: k.get('power', 0), reverse=False)
        data['cards'] = sorted(data['cards'], key=lambda k: k.get('element', 0), reverse=True)

    i = 0
    for card in data['cards']:
        card['id'] = i
        i += 1

    with open(Config.CARDS_DATA_PATH, 'w') as file:
        json.dump(data, file, indent=4)








