from django.shortcuts import render
from django.http import HttpResponse
#from migrations.poker_headsup_main import test
# Create your views here.
def main_page(request,params):
    #heads up (player and robot)
    
    # position (True : player, False : robot)
    BB_posi = True
    SB_posi = False
    flag = SB_posi
    checker = [False, False]

    # blind
    BB = 100
    SB = 50
    pot = BB + SB
    luck = SB
    bets = 0
    # stuck
    stuck_player = 50 * BB
    stuck_robot = 50 * BB


            
    action = Action(pot, stuck_player, stuck_robot,flag)
    stuck_player += SB
    stuck_robot += BB
    
    while stuck_player != 0 or stuck_robot != 0:
    
            if(BB_posi):
                BB_posi = False
                SB_posi = True
            else:
                BB_posi = True
                SB_posi = False
    
            flag = SB_posi
            luck = SB
    
            # preflop - flop - turn - river
    
            action.newgame_a(flag)
            now_step = 0
            checker = [False, False]
            params = {}
            
    return render(request,'poker/top.html',params)
