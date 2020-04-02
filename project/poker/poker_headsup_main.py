import numpy as np

from django import forms
from django.shortcuts import render
from django.http import HttpResponse
from .poker_headsup_deck import card_deck
from .poker_headsup_deck import draw
from .poker_headsup_deck import make_list_num
from .poker_headsup_deck import make_list_mark
from .poker_headsup_deck import check
from .poker_headsup_roles import roles
from .poker_headsup_roles import roles_name
from .poker_headsup_action import Action
from .poker_page import main_page

def main(request):

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

    # -------------------------------------------------------------------------------------------------

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
        # preflop
        while 0 <= now_step and now_step <= 4:

            if(checker[0] and checker[1]):
                flag = BB_posi
                now_step += 1
                bets = 0
                luck = 0
                checker = [False, False]
                continue

            if(now_step == 0):
                print("preflop")
                comunitee_card = draw(card_deck(), 5)
                params['comunitee_card'] = ""
                bol = True
                while(bol):
                    player_card = draw(card_deck(), 2)
                    bol = check(comunitee_card, player_card)
                boo = [True, True]
                while(boo[0] and boo[1]):
                    robot_card = draw(card_deck(), 2)
                    boo[0] = check(comunitee_card, robot_card)
                    boo[1] = check(player_card, robot_card)
                params['player_card'] = player_card[0]+player_card[1]
                params['robot_card'] = robot_card[0]+robot_card[1]
                main_page(request,params)
            elif(now_step == 1):
                print("flop")
                params['comunitee_card'] = comunitee_card[0]+comunitee_card[1]+comunitee_card[2]
                main_page(request,params)
            elif(now_step == 2):
                print("turn")
                params['comunitee_card'] =params['comunitee_card'] + comunitee_card[3]
                main_page(request,params)
            elif(now_step == 3):
                print("river")
                params['comunitee_card'] =params['comunitee_card'] + comunitee_card[4]
                main_page(request,params)
            elif now_step == 4:
                print("showdown")
                player_card += comunitee_card
                robot_card += comunitee_card

                player_card_num = make_list_num(player_card, 7)
                player_card_mark = make_list_mark(player_card, 7)
                player_result = roles(player_card_num, player_card_mark)
                player_roles = roles_name(player_result)

                robot_card_num = make_list_num(robot_card, 7)
                robot_card_mark = make_list_mark(robot_card, 7)
                robot_result = roles(robot_card_num, robot_card_mark)
                robot_roles = roles_name(robot_result)

                print("Player is " + player_roles + ".")
                print("Robot is " + robot_roles + ".")
                if player_result > robot_result:
                    print("Player is winner!")
                    action.win_a(True)
                else:
                    print("Robot is winner!")
                    action.win_a(False)
                now_step = 0

            action.situation_a()
            # preflop: action is player
            if(flag):
                print("Player's action.")
                act = str(input())

                if(act == "call"):
                    checker[0] = True
                    action.call_a(luck)
                    flag = False
                    continue

                elif(act == "check"):
                    action.check_a()
                    checker[0] = True
                    flag = False
                    continue

                elif(act == "raise"):
                    checker = [True, False]
                    print("How much ?")
                    bets = int(input())
                    action.raise_a(bets, flag)
                    flag = False
                    continue

                elif(act == "fold"):
                    action.fold_a(flag)
                    now_step = 0
                    break

                else:
                    print("Please follow the sentence.")
                    continue
            
            # preflop: action is robot
            else:
                print("Robot's action.")
                #act = input()
                if checker[0] == True and checker[1] == False:
                    act = "call"
                else:
                    act = "check"

                if(act == "call"):
                    checker[1] = True
                    action.call_a(luck)
                    continue

                if(act == "check"):
                    action.check_a()
                    checker[1] = True
                    flag = True
                    continue

                elif(act == "raise"):
                    checker = [False, True]
                    print("How much ?")
                    bets = int(input())
                    action.raise_a(bets, flag)
                    flag = True
                    continue

                elif(act == "fold"):
                    action.fold_a(flag)
                    now_step = 0
                    break
            
        # showdown

        if(now_step == 4):
            print()
            print("ゲーム終了")
            print()
    # ------------------------------------------------------------------------------

    if stuck_player == 0:
        print("The player won all the stucks.")
    elif stuck_robot == 0:
        print("The robot won all the stucks.")
    return 0
