#                                                  #
#                  Game Logic                      #
#                                                  #
####################################################
####################################################
# 0 <--> Nature
# 1 <--> Earth
# 2 <--> Darkness
# .
# .
# .
# 6 <--> Air

####################################################
#            Data structures are globals           #
#                                                  #
starting_player = True  # True: Host, False: Guest
score2win = 65
affix1 = None  # No affix by default
affix2 = None

board = [-1 for i in range(16)]  # Initialize
deck_host = []
deck_guest = []
#                                                  #
#                                                  #
####################################################


# Initialization of all structures
def initialize(*args):
    global starting_player, score2win, affix1, affix2
    starting_player = args[0]