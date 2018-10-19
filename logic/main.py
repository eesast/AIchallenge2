#! /usr/bin/env python3
# -*- coding: utf-8 -*
from gamemain import *


def main():
    # initialize the game

    game = GameMain()

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
