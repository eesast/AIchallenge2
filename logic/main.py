#! /usr/bin/env python3
# -*- coding: utf-8 -*
from gamemain import *
from json import *


# use a global variable to manage the whole game
game = GameMain()


def game_init(file_path="./"):
    # here give the parent path and load the data and return the airplane
    game.load_data(file_path)    # for platform: here input dictionary path
    return game.generate_route()


def parachute(information):
    # here game gets all players' information and jump aim, return first turn's information
    print('parachute:'+str(information))
    return game.parachute(information)


def game_main(commands):
    game.unwrap_commands(commands)
    return game.refresh()


def main():
    # this function is just to debug for logic
    object.PRINT_DEBUG = 999
    file = open("./debug/input.txt", 'r', encoding='utf-8')
    game.generate_route()
    information_tem = load(file)
    information = {}
    for key, value in information_tem.items():
        new_value = {}
        for key2, value2 in value.items():
            value2["position"] = (value2["position"][0], value2["position"][1])
            new_value[int(key2)] = value2
        information[int(key)] = new_value
    print(information)
    game.parachute(information)

    # start the loop
    # fight until there is only one team alive or be overtime
    while game.alive_teams() > 1 and game.anti_infinite_loop():
        # first get information from platform

        # then refresh game
        game.unwrap_commands(None)
        game.refresh()

        # emit information to platform

    # report the final result
    print("game over")
    return


if __name__ == '__main__':
    main()
