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

    # get enum data from string
    string_to_type = {
        'WEAPON': WEAPON,
        'ARMOR': ARMOR,
        'GOODS': GOODS
    }

    def __init__(self, item_type, number):
        super().__init__()
        # some important characteristics
        self.data = Item.all_data[item_type]
        self.durability = Item.all_data[item_type]['durability']    # using durability
        self.item_type = item_type                   # type id
        self.id = number                             # item's id
        return

    @staticmethod
    def load_data(parent_path, item_file_path):
        with open(parent_path + item_file_path, "r", encoding="utf-8") as file:
            all_data = load(file)
        for key, value in all_data.items():
            Item.all_data[key] = value
            Item.all_data[key]['name'] = key
            Item.all_data[value['number']] = Item.all_data[key]
        return all_data

    @staticmethod
    def add(new_type, pos):
        # generate a new item in the map
        if isinstance(new_type, str):
            new_type = Item.all_data[new_type]['number']
        new_item = Item(new_type, Item.next_id)
        new_item.position = pos
        Item.all_items[Item.next_id] = new_item
        Item.next_id += 1
        return new_item.id

    @staticmethod
    def remove(item_id):
        pass

    def is_weapon(self):
        return self.data['type'] == 'WEAPON'

    def is_armor(self):
        return self.data['type'] == 'ARMOR'

    def is_goods(self):
        return self.data['type'] == 'GOODS'

    @staticmethod
    def get_data_by_item_id(item_id):
        return Item.all_data[Item.all_items[item_id].item_type]


if __name__ == '__main__':
    # if necessary, test here
    pass
