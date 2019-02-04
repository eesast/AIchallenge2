#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from xlrd import *
# from json import dump

# here give some enums
START_ROW = 2

# for weapon
WEAPON_INDEX = 0

WEAPON_NUMBER = 0
WEAPON_NAME = 1
WEAPON_MACRO = 2
WEAPON_DURABILITY = 3
WEAPON_RANGE = 4
WEAPON_CD = 5
WEAPON_DAMAGE = 6
WEAPON_OCCUR = 7
WEAPON_EFFECT = 8
WEAPON_COLUMN = 9

# for armor
ARMOR_INDEX = 1

ARMOR_NUMBER = 0
ARMOR_NAME = 1
ARMOR_MACRO = 2
ARMOR_DURABILITY = 3
ARMOR_REDUCE = 4
ARMOR_PARAMETER = 5
ARMOR_OCCUR = 6
ARMOR_EFFECT = 7
ARMOR_COLUMN = 8

# for goods
GOODS_INDEX = 2

GOODS_NUMBER = 0
GOODS_NAME = 1
GOODS_MACRO = 2
GOODS_MODE = 3
GOODS_PARAMETER = 4
GOODS_OCCUR = 5
GOODS_INSTRUCTION = 6
GOODS_COLUMN = 7

# for character
CHARACTER_INDEX = 3

CHARACTER_NUMBER = 0
CHARACTER_VOCATION = 1
CHARACTER_MACRO = 2
CHARACTER_HP = 3
CHARACTER_DISTANCE = 4
CHARACTER_ANGLE = 5
CHARACTER_MOVE = 6
CHARACTER_SKILL = 7
CHARACTER_PARAMETER = 8
CHARACTER_COLUMN = 9


def open_file(path):
    return open_workbook(path)


def get_item_data(file):
    def get_weapon_data(sheet_weapon, data):
        for i in range(START_ROW, sheet_weapon.nrows):
            row = sheet_weapon.row_values(i)
            if len(row[WEAPON_MACRO]) < 1:
                break  # if this row is empty, break
            number = int(row[WEAPON_NUMBER])
            macro = row[WEAPON_MACRO]
            durability = int(row[WEAPON_DURABILITY])
            attack_range = int(row[WEAPON_RANGE])
            cd = int(row[WEAPON_CD])
            damage = int(row[WEAPON_DAMAGE])
            occur = int(row[WEAPON_OCCUR])
            data[macro] = {
                'type': 'WEAPON',
                'number': number,
                'durability': durability,
                'range': attack_range,
                'cd': cd,
                'damage': damage,
                'occur': occur,
            }
        return

    def get_armor_data(sheet_armor, data):
        for i in range(START_ROW, sheet_armor.nrows):
            row = sheet_armor.row_values(i)
            if len(row[ARMOR_MACRO]) < 1:
                break  # if this row is empty, break
            number = int(row[ARMOR_NUMBER])
            macro = row[ARMOR_MACRO]
            durability = int(row[ARMOR_DURABILITY])
            reduce = int(row[ARMOR_REDUCE])
            param = row[ARMOR_PARAMETER]
            occur = int(row[ARMOR_OCCUR])
            data[macro] = {
                'type': 'ARMOR',
                'number': number,
                'durability': durability,
                'reduce': reduce,
                'param': param,
                'occur': occur,
            }
        return

    def get_goods_data(sheet_goods, data):
        for i in range(START_ROW, sheet_goods.nrows):
            row = sheet_goods.row_values(i)
            if len(row[GOODS_MACRO]) < 1:
                break  # if this row is empty, break
            number = int(row[GOODS_NUMBER])
            macro = row[GOODS_MACRO]
            mode = row[GOODS_MODE]
            param = row[GOODS_PARAMETER]
            occur = int(row[GOODS_OCCUR])
            data[macro] = {
                'type': 'GOODS',
                'number': number,
                'macro': macro,
                'mode': mode,
                'param': param,
                'occur': occur,
            }
        return

    all_data = {}
    get_weapon_data(file.sheet_by_index(WEAPON_INDEX), all_data)
    get_armor_data(file.sheet_by_index(ARMOR_INDEX), all_data)
    get_goods_data(file.sheet_by_index(GOODS_INDEX), all_data)
    return all_data


def output_item_data(data, path):
    formatter = JsonFormatter(data=data)
    data = formatter.render()
    with open(path, 'w') as fp:
        # dump(data, fp)
        fp.write(data)


def get_character_data(sheet_character):
    data = {}
    for i in range(START_ROW, sheet_character.nrows):
        row = sheet_character.row_values(i)
        if len(row[CHARACTER_MACRO]) < 1:
            break  # if this row is empty, break
        number = int(row[CHARACTER_NUMBER])
        macro = row[CHARACTER_MACRO]
        hp = int(row[CHARACTER_HP])
        distance = row[CHARACTER_DISTANCE]
        angle = row[CHARACTER_ANGLE]
        move = row[CHARACTER_MOVE]
        param = row[CHARACTER_PARAMETER]
        data[macro] = {
            'number': number,
            'hp': hp,
            'distance': distance,
            'angle': angle,
            'move': move,
            'skill': param,
        }
    return data


def output_character_data(data, path):
    formatter = JsonFormatter(data=data)
    data = formatter.render()
    with open(path, 'w') as fp:
        # dump(data, fp)
        fp.write(data)


# here is a class from internet to format json data
class JsonFormatter:

    def __init__(self, intend=4, data=""):
        self.intend = intend
        self.stack = []
        '''self.obj = None
        self.source = data
        self.prepare()'''
        self.obj = data

    @staticmethod
    def json_str(s):
        return '"' + s + '"'

    '''@staticmethod
    def get_source(name):
        with open(name, 'r') as f:
            return ''.join(f.read().split())

    def prepare(self):
        try:
            self.obj = eval(self.source)
        except:
            raise Exception('Invalid json string!')'''

    def line_intend(self, level=0):
        return '\n' + ' ' * self.intend * level

    def parse_dict(self, obj=None, intend_level=0):
        self.stack.append(self.line_intend(intend_level) + '{')
        intend_level += 1
        for key, value in obj.items():
            key = self.json_str(str(key))
            self.stack.append(self.line_intend(intend_level) + key + ':')
            self.parse(value, intend_level)
            self.stack.append(',')
        if self.stack[-1] == ',':
            self.stack.pop(-1)
        self.stack.append(self.line_intend(intend_level - 1) + '}')

    def parse_list(self, obj=None, intend_level=0):
        self.stack.append(self.line_intend(intend_level) + '[')
        intend_level += 1
        for item in obj:
            self.parse(item, intend_level)
            self.stack.append(',')
        self.stack.append(self.line_intend(intend_level - 1) + ']')

    def parse(self, obj, intend_level=0):
        if obj is None:
            self.stack.append('null')
        elif obj is True:
            self.stack.append('true')
        elif obj is False:
            self.stack.append('false')
        elif isinstance(obj, (int, int, float)):
            self.stack.append(str(obj))
        elif isinstance(obj, str):
            self.stack.append(self.json_str(obj))
        elif isinstance(obj, (list, tuple)):
            self.parse_list(obj, intend_level)
        elif isinstance(obj, dict):
            self.parse_dict(obj, intend_level)
        else:
            raise Exception('Invalid json type %s!' % obj)

    def render(self):
        self.parse(self.obj, 0)
        res = ''.join(self.stack).strip()
        return res


def main():
    file = open_file('./data.xlsx')
    data = get_item_data(file)
    output_item_data(data, '../data/item.json')
    data = get_character_data(file.sheet_by_index(CHARACTER_INDEX))
    output_character_data(data, '../data/character.json')
    return


if __name__ == '__main__':
    main()
