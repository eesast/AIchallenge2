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

    # next entity's id
    next_id = 0

    def __init__(self, item_type, number):
        super().__init__()
        # some important characteristics
        self.durability = Item.all_data[item_type].durability       # using durability
        self.item_type = item_type                                  # should be type enum
        self.id = number              # item's id
        self.owner = -1           # owner's id
        return

    @staticmethod
    def load_data(parent_path, item_file_path):
        with open(parent_path + item_file_path, "r", encoding="utf-8") as file:
            all_data = load(file)
        return all_data

    @staticmethod
    def add(new_type):
        new_item = Item(new_type, Item.next_id)
        new_item.durability = Item.all_data[new_type].durability
        Item.all_items[Item.next_id] = new_item
        Item.next_id += 1
        return new_item.id


if __name__ == '__main__':
    # if necessary, test here
    pass
