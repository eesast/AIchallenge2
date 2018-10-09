#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from allclass.equipment import *


class GameMain(object):
    def __init__(self, players):
        # it's more like a define instead of an initialization
        self.map_size = (10000, 10000)
        self.load_data()
        self.__players = players
        self.out_order = []          # save the player's dying order
        self.map_items = [[[] for i in range(16)]for j in range(16)]    # try to divide map into 256 parts

    def refresh_items(self):
        pass

    def load_data(self):
        pass
