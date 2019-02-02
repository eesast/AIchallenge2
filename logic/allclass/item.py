#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .object import *
from json import load


class Item(Object):   # class for each equipment and goods
    # two name for different item types
    WEAPON = 0
    ARMOR = 1
    GOODS = 2

    # save all items' data
    all_data = {}

    # all items' entities
    all_items = {}

    def __init__(self, item_type):
        super().__init__()
        # some important characteristics
        self.durability = None      # using durability
        self.item_type = item_type  # should be type enum
        self.damage = None          # including real damage and heal(negative number)
        self.owner = None           # owner's id
        self.param = None
        pass

    @staticmethod
    def load_data(parent_path, item_file_path):
        with open(parent_path + item_file_path, "r", encoding="utf-8") as file:
            all_data = load(file)
        return all_data

    # enum all items' name
    EQUIP_CHARGER = 1
    GOODS_CHARGER = 51


if __name__ == '__main__':
    # if necessary, test here
    pass
