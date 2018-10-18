#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import random


def game_main(last_turn_state, player_demands):
    '''
    This function will return the state and the demand list of next turn.

    last_turn_state is a dict
    which contains all objects in the game.
    player_demands is a list
    which contains all demands that wait for being executed.
    '''
    last_turn_state['turn'] += 1
    for demand in player_demands:
        demand['cd'] -= 1
        if demand['order'] == 1:
            last_turn_state['test'] += 1
        elif demand['order'] == 2:
            last_turn_state['test'] //= 2
        else:
            pass
    player_demands = [demand for demand in player_demands if demand['cd'] > 0]
    return last_turn_state, player_demands


def game_init():
    '''
    This function will return the state and the demand list of the first turn.
    '''
    test = random.randint(100,200)
    # print(test)
    state = {'turn': 0, 'test': test}
    demand = []
    return state, demand


def change_to_string(last_turn_state, player_demands):
    '''
    just for debugging
    '''
    return (str(last_turn_state)+'\n'+str(player_demands)+'\n=========================\n')


def main():
    '''
    test in python3
    '''
    # state, player_demands = game_init()
    # while state['turn'] < 100:
    #     for i in range(random.randint(1, 10)):
    #         demand = {'cd': random.randint(
    #             1, 5), 'order': random.randint(0, 2)}
    #         player_demands.append(demand)
    #     state, player_demands = game_main(state, player_demands)
    #     print(change_to_string(state, player_demands))


if __name__ == '__main__':
    main()
