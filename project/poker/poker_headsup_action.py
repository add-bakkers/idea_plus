import numpy as np


class Action:

    def __init__(self, pot, stuck_player, stuck_robot ,flag):
        self.pot = pot
        self.stuck_player = stuck_player
        self.stuck_robot = stuck_robot
        self.flag = flag

    # newgame

    def newgame_a(self, flag):
        BB = 100
        SB = 50
        self.pot = BB + SB
        if(flag):
            print("BB is robot : " + str(BB) + " / SB is player : " + str(SB))
            self.stuck_player -= SB
            self.stuck_robot -= BB
        else:
            print("BB is player : " + str(BB) + " / SB is robot : " + str(SB))
            self.stuck_robot -= SB
            self.stuck_player -= BB

    # situation

    def situation_a(self):
        print("Pot:" + str(self.pot) + "/Player's stuck:" + str(self.stuck_player) + "/Robot's stuck:" + str(self.stuck_robot))
        print()

    # action: check

    def check_a(self):
        print()
        print("The last player's action was check")
        print()

    # action: call

    def call_a(self, luck):
        self.luck = luck
        #self.stuck_player = stuck_player
        #self.stuck_robot = stuck_robot
        self.pot += self.luck
        if(self.flag):
            self.stuck_robot -= self.luck
        else:
            self.stuck_player -= self.luck
        print()
        print("The last player's action was call")
        print()

    # action: raise

    def raise_a(self, bets, flag):
        self.bets = bets
        #self.stuck_player = stuck_player
        #self.stuck_robot = stuck_robot
        self.pot += self.bets
        if(flag):
            self.stuck_player -= self.bets
        else:
            self.stuck_robot -= self.bets
        print()
        print("The last player's action was " + str(self.bets) + "bet")
        print()
                
    # action: fold

    def fold_a(self, flag):
        BB = 100
        SB = 50
        print()
        print("The last player's action was fold")
        print()
        if(flag):
            print("The robot is winner !" )
            self.stuck_robot += self.pot
        else:
            print("The player is winner !" )
            self.stuck_player += self.pot
        self.pot = BB + SB
        print()
        print()
        print("Next Game")
        print()
        print()
    
    def win_a(self, bol):
        BB = 100
        SB = 50
        if(bol):
            self.stuck_player += self.pot
        else:
            self.stuck_robot += self.pot
        self.pot = BB + SB
        print()
        print()
        print("Next Game")
        print()
        print()
