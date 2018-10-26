#! /usr/bin/env python3
# -*- coding: utf-8 -*
from gamemain import *


# use a global variable to manage the whole game
game = GameMain()


def game_init():
    # here initialize the game and return the airplane
    return game.generate_route()


def parachute(information):
    # here game gets all players' information and jump aim, return first turn's information
    return game.parachute(information)


def game_main(commands):
    game.unwrap_commands(commands)
    return game.refresh()


def main():
    # this function is just to debug for logic
    game.generate_route()
    game.parachute(None)

    # start the loop
    while game.alive_teams() > 1:   # fight until there is only one team alive
        # first get information from platform

        # then refresh game
        game.refresh()

        # emit information to platform

    # report the final result

    return


if __name__ == '__main__':
    main()
