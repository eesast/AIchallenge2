#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from allclass import *


class GameMain:

    class Players:
        # this class try to manager all players information, not sure
        def __init__(self, players):
            self.players = []

    def __init__(self):
        # first load some module data here
        character.Character.load_data()
        prop.Prop.load_data()

        # it's more like a define instead of an initialization
        self.map_size = (10000, 10000)
        self.die_order = []          # save the player's dying order
        self.map_items = [[[] for i in range(16)]for j in range(16)]    # try to divide map into 256 parts

        # here load map data
        self.load_map()

    def refresh(self):
        # refresh a new frame according to the orders
        pass

    def refresh_items(self):
        pass

    def load_map(self):
        pass

    def alive_teams(self):
        # now not sure how to count
        return 0
        pass


if __name__ == '__main__':
    # if necessary, test here
    pass
