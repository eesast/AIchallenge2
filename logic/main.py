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
    import debug.ai as ai
    me = ai.AI()
    object.PRINT_DEBUG = 999
    game_init("./", "config.ini")
    file = open("./debug/input.json", 'r', encoding='utf-8')
    information_tem = load(file)
    information = {}
    for key, value in information_tem.items():
        value["position"] = (value["position"][0], value["position"][1])
        information[int(key)] = value
    print(information)
    parachute(information)
    # for debug
    commands = {}
    for i in range(12):
        commands[i] = [
            {
                'command_type': 0,
                "move_angle": 0,
                "view_angle": 0,
            }
        ]
    # start the loop
    # fight until there is only one team alive or be overtime
    while game.alive_teams() > 1 and game.anti_infinite_loop():
        # here create random move instructions
        for i in range(11):
            commands[i][0]['move_angle'] = random.randrange(0, 360)
            commands[i][0]['view_angle'] = random.randrange(0, 360)

        # then refresh game and get current info
        current_info = game_main(commands)

        # here give a simple ai for player No.11
        commands[11] = me.get_command(current_info[11])

    # report the final result
    print("game over")
    return


if __name__ == '__main__':
    main()
