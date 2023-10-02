class GameViewModel:
    def __init__(self, board=None):
        # Elements : 0-Nature -> 1-Earth -> 2-Darkness until 6-Air
        #A card is defined by its element and its power with a tuple (struct) like this : (2, 450) for a Darkness with 450 power
        self.board = [-1 for i in range(16)]
        self.player_turn= 1 #1 ou -1 to alternate
        self.score_to_win = 65

    def getCoordinates(self, index):
        x = index % 4
        y = index // 4
        return x, y

    #Get the adjacent cells of one cell
    def getAdjacent(self, index):
        list_adjacent = []
        (x, y) = self.getCoordinates(index)
        #Left
        if x != 0:
            list_adjacent.append(x - 1)
        #Right
        if x != 3:
            list_adjacent.append(x + 1)
        #Up
        if y != 0:
            list_adjacent.append(y - 1)
        #Down
        if y != 3:
            list_adjacent.append(y + 1)

        return list_adjacent

    #Calculate if a card take another adjacent one
    def isTaken(self, attacker, defender):
        return attacker.power > defender.power

    #Get the distance between both elements (element 6 and element 1 has a distance of 2 because ->1->2)
    def getDistance(self, element1, element2):
        if element1 <= element2:
            return element2 - element1
        else:
            return 7 - element1 + element2

    #Get element1 vs element2 bonus or malus
    def getForce(self, element1, element2):
        match self.getDistance(element1, element2):
            case 0: return 0
            case 1: return 150
            case 2: return 0
            case 3: return 150
            case 4: return -150
            case 5: return 0
            case 6: return -150
        return 0

    #Same as gtForce but return if there is an affinity or not
    def getAffinity(self, element1, element2):
        match self.getDistance(element1, element2):
            case 0: return 0
            case 1: return 0
            case 2: return 100
            case 3: return 0
            case 4: return 0
            case 5: return 100
            case 6: return 0
        return 0

    def getTrinity(self, card):
        pass

    # Logic when a player play a card
    def playCard(self, position, card):
        self.board[position] = card




