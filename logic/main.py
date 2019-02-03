#! /usr/bin/env python3
# -*- coding: utf-8 -*
from gamemain import *
from json import *
import random   # for logic to debug

# use a global variable to manage the whole game
game = GameMain()


def game_init(file_path="./", config_file_name="config.ini", debug_level=None):
    # first adjust debug level if necessary
    game.set_debug_level(debug_level)
    # here give the parent path and load the data and return the airplane
    game.load_data(file_path, config_file_name)  # for platform: here input dictionary path
    game.map_init()
    return game.generate_route()


def parachute(information):
    # here game gets all players' information and jump aim, return first turn's information
    return game.parachute(information)


def game_main(commands):
    game.unwrap_commands(commands)
    return game.refresh()


def main():
    # this function is just to debug for logic
    object.PRINT_DEBUG = 999
    game_init("./", "config.ini")
    file = open("./debug/input.json", 'r', encoding='utf-8')
    information_tem = load(file)
    information = {}
    for key, value in information_tem.items():
        value["position"] = (value["position"][0], value["position"][1])
        information[int(key)] = value
    print(information)
    game.parachute(information)
    # for debug
    commands = \
        {
            5: [
                {'command_type': 0, 'target': 12, "move_angle": 1.2, "view_angle": 3.6, "other": 13}
            ],
        }
    for i in range(12):
        commands[i] = [
            {'command_type': 0, "move_angle": 1.2, "view_angle": 3.6}
        ]
    # start the loop
    # fight until there is only one team alive or be overtime
    while game.alive_teams() > 1 and game.anti_infinite_loop():
        # first get information from platform
        for i in range(12):
            commands[i][0]['move_angle'] = random.randrange(0, 360)
            commands[i][0]['view_angle'] = random.randrange(0, 360)

        # then refresh game
        game.unwrap_commands(commands)
        game.refresh()

        # emit information to platform

    # report the final result
    print("game over")
    return


if __name__ == '__main__':
    main()
