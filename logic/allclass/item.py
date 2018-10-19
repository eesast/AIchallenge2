#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .object import *


class Item(Object):   # class for each weapon and goods
    # two name for different prop types
    WEAPON = 0
    GOODS = 1

    # save all props data
    all_data = []

    def __init__(self, prop_type):
        super().__init__()
        # some important characteristics
        self.durability = None      # using durability
        self.prop_type = prop_type  # 0 means weapon and 1 means goods
        self.damage = None          # including real damage and heal(negative number)
        pass

    @staticmethod
    def load_data():
        pass

    # enum all props' name
    WEAPON_HANDGUN = 1
    GOODS_CHARGER = 51


if __name__ == '__main__':
    # if necessary, test here
    pass
