#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .object import *
from json import load
from random import randint
from bisect import bisect


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

    # to get random item
    probability_weights = [0]
    modified_weights = [0]
    index_to_type = {}

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
        self.durability = self.data['durability']    # using durability
        self.item_type = item_type                   # type index
        self.number = number
        self.block_view = False
        return

    @staticmethod
    def load_data(parent_path, item_file_path):
        with open(parent_path + item_file_path, "r", encoding="utf-8") as file:
            all_data = load(file)
        for key, value in all_data.items():
            item_type = value['number']
            Item.all_data[key] = value
            Item.all_data[item_type] = all_data[key]
            Item.all_data[item_type]['name'] = key
            occur = value['occur']
            if occur:
                Item.index_to_type[len(Item.index_to_type)] = value['number']
                Item.probability_weights.append(Item.probability_weights[-1] + occur)
                Item.modified_weights.append(Item.modified_weights[-1] + occur if occur < 50 else 0)

        # get probability for hacker
        Item.modified_weights = [x if x < 50 else 0 for x in Item.probability_weights]
        # now just copy default weights, continue to be finished
        Item.modified_weights = Item.probability_weights

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
        return new_item.number

    @staticmethod
    def remove(item_id):
        Item.all_items.pop(item_id)
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

    @staticmethod
    def get_random_item():
        return Item.index_to_type[bisect(Item.probability_weights, randint(0, Item.probability_weights[-1] - 1)) - 1]

    @staticmethod
    def get_reward_item():
        return Item.index_to_type[bisect(Item.modified_weights, randint(0, Item.modified_weights[-1] - 1)) - 1]


if __name__ == '__main__':
    # if necessary, test here
    pass
