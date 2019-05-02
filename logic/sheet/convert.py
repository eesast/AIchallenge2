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
WEAPON_ANGLE = 5
WEAPON_CD = 6
WEAPON_DAMAGE = 7
WEAPON_OCCUR = 8
WEAPON_EFFECT = 9
WEAPON_COLUMN = 10

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
GOODS_CD = 5
GOODS_OCCUR = 6
GOODS_INSTRUCTION = 7
GOODS_COLUMN = 8

# for character
CHARACTER_INDEX = 3

CHARACTER_NUMBER = 0
CHARACTER_VOCATION = 1
CHARACTER_MACRO = 2
CHARACTER_HP = 3
CHARACTER_DISTANCE = 4
CHARACTER_ANGLE = 5
CHARACTER_RADIUS = 6
CHARACTER_MOVE = 7
CHARACTER_SKILL = 8
CHARACTER_PARAMETER = 9
CHARACTER_COLUMN = 10

# for circle
CIRCLE_INDEX = 4

CIRCLE_STAGE = 0
CIRCLE_ITEMS = 1
CIRCLE_DELAY = 2
CIRCLE_WAIT = 3
CIRCLE_MOVE = 4
CIRCLE_DAMAGE = 5
CIRCLE_SHRINK = 6
CIRCLE_RADIUS = 7
CIRCLE_SPEED = 8
CIRCLE_FRAMES = 9
CIRCLE_TOTAL = 10

# for sound
SOUND_INDEX = 5

SOUND_NUMBER = 0
SOUND_TYPE = 1
SOUND_MACRO = 2
SOUND_SPEED = 3
SOUND_DISTANCE = 4
SOUND_DESCRIPTION = 5

# for parameters
PARAMETER_INDEX = 6


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
            param = row[WEAPON_ANGLE]
            occur = int(row[WEAPON_OCCUR])
            data[macro] = {
                'type': 'WEAPON',
                'number': number,
                'durability': durability,
                'macro': macro,
                'mode': '',
                'range': attack_range,
                'cd': cd,
                'damage': damage,
                'reduce': 0,
                'param': param,
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
            reduce = row[ARMOR_REDUCE]
            param = row[ARMOR_PARAMETER]
            occur = int(row[ARMOR_OCCUR])
            data[macro] = {
                'type': 'ARMOR',
                'number': number,
                'durability': durability,
                'macro': macro,
                'mode': '',
                'range': 0,
                'cd': 0,
                'damage': 0,
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
            cd = int(row[GOODS_CD])
            occur = int(row[GOODS_OCCUR])
            data[macro] = {
                'type': 'GOODS',
                'number': number,
                'durability': 1,
                'macro': macro,
                'mode': mode,
                'range': 0,
                'cd': cd,
                'damage': 0,
                'reduce': 0,
                'param': param,
                'occur': occur,
            }
        for key, value in data.items():
            if 'SCOPE' in key:
                value['param'] = int(value['param'])

        return

    all_data = {}
    get_weapon_data(file.sheet_by_index(WEAPON_INDEX), all_data)
    get_armor_data(file.sheet_by_index(ARMOR_INDEX), all_data)
    get_goods_data(file.sheet_by_index(GOODS_INDEX), all_data)
    return all_data


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
        radius = row[CHARACTER_RADIUS]
        move = row[CHARACTER_MOVE]
        param = row[CHARACTER_PARAMETER]
        data[macro] = {
            'number': number,
            'hp': hp,
            'distance': distance,
            'angle': angle,
            'radius': radius,
            'move': move,
            'skill': param,
        }
    return data


def get_parameter_data(sheet_parameter):
    data = {
        'character': {},
        'main': {
            'score_by_rank': {},
        },
    }
    col = sheet_parameter.col_values(1)
    data['character']['move_step'] = [0, col[2], col[3], col[4]]
    for i in range(1, 9):
        data['main']['score_by_rank'][i] = int(col[i + 4])

    data['character']['airplane'] = col[13]
    data['character']['pick_distance'] = col[14]

    col = sheet_parameter.col_values(4)
    data['main']['damage_param'] = col[2]
    data['character']['reduce'] = col[3]
    data['main']['score_by_kill_one'] = int(col[4])
    for i in range(9, 17):
        data['main']['score_by_rank'][i] = int(col[i - 4])

    data['character']['jumping'] = col[13]
    data['character']['swimming'] = col[14]

    return data


def get_circle_data(sheet_circle):
    data = {}
    for i in range(START_ROW, sheet_circle.nrows):
        row = sheet_circle.row_values(i)
        if not row[CIRCLE_MOVE]:
            break
        stage = int(row[CIRCLE_STAGE])
        items = int(row[CIRCLE_ITEMS])
        delay = int(row[CIRCLE_DELAY])
        wait = int(row[CIRCLE_WAIT])
        move = int(row[CIRCLE_MOVE])
        damage = row[CIRCLE_DAMAGE]
        shrink = row[CIRCLE_SHRINK]
        data[stage] = {
            'items': items,
            'delay': delay,
            'wait': wait,
            'move': move,
            'damage': damage,
            'shrink': shrink,
        }
    return data


def get_sound_data(sheet_sound):
    data = {}
    for i in range(START_ROW, sheet_sound.nrows):
        row = sheet_sound.row_values(i)
        if len(row[SOUND_MACRO]) < 1:
            break
        number = int(row[SOUND_NUMBER])
        macro = row[SOUND_MACRO]
        speed = row[SOUND_SPEED]
        distance = row[SOUND_DISTANCE]
        data[macro] = {
            'number': number,
            'speed': speed,
            'distance': distance,
        }
    return data


def output_data(data, path):
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
        # self.stack.append(self.line_intend(intend_level) + '[')
        self.stack.append('[')
        intend_level += 1
        for item in obj:
            self.parse(item, intend_level)
            self.stack.append(',')
        if self.stack[-1] == ',':
            self.stack.pop(-1)
        self.stack.append(']')
        # self.stack.append(self.line_intend(intend_level - 1) + ']')

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
    output_data(data, '../data/item.json')
    data = get_character_data(file.sheet_by_index(CHARACTER_INDEX))
    output_data(data, '../data/character.json')
    data = get_circle_data(file.sheet_by_index(CIRCLE_INDEX))
    output_data(data, '../data/circle.json')
    data = get_sound_data(file.sheet_by_index(SOUND_INDEX))
    output_data(data, '../data/sound.json')
    data = get_parameter_data(file.sheet_by_index(PARAMETER_INDEX))
    output_data(data, '../data/parameter.json')
    return


if __name__ == '__main__':
    main()
