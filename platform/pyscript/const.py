#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import os
from functools import reduce


def load_json(config_path):
    with open(config_path, 'r', encoding='utf-8') as config_file:
        data_paths = json.load(config_file)
    data_dct = {}
    data_keys = ['CHARACTER', 'ITEM', 'SOUND']
    for data_key in data_keys:
        path = os.path.join(os.path.dirname(config_path),
                            data_paths[data_key+'_FILE_PATH'])
        with open(path, 'r', encoding='utf-8') as data_file:
            data_dct[data_key] = json.load(data_file)
    return data_dct


def enum2str(enum_name, enum_list, upper=True):
    enum_name = enum_name.upper() if upper else enum_name.lower()
    enum_list2 = list(set(enum_list))
    enum_list2.sort(key=enum_list.index)
    enum_list2 = [w.upper() if upper else w.lower() for w in enum_list2]
    enum_str = 'enum %s\n{\n' % (enum_name,)
    for i, name in enumerate(enum_list2):
        enum_str += '    %s = %d,\n' % (name, i)
    enum_str += '    %s = %d,\n' % (enum_name +
                                    ('_NB' if upper else '_nb'), len(enum_list2))
    enum_str += '};\n\n'
    return enum_str


def character2str(character_dct):
    dct_by_nb = character_dct.items()
    dct_by_nb = sorted(dct_by_nb, key=lambda k: k[1]['number'])
    vocation_nb = len(dct_by_nb)
    data_keys = list(dct_by_nb[0][1].keys())

    # property struct
    property_str = 'struct vocation_property\n{\n'
    for key in data_keys:
        property_str += '    %s %s;\n' % ('int' if key ==
                                          'number' else 'double', key)
    property_str += '};\n\n'

    # enum
    vocation_str = enum2str('VOCATION', [macro for macro, _ in dct_by_nb])

    # data table
    table = 'const vocation_property VOCATION_DATA[%d] = \n{ // ' % (
        vocation_nb,)
    for key in data_keys:
        table += '%10s' % (key,)
    table += '\n'
    for name, data in dct_by_nb:
        table += '    {'
        for key, value in data.items():
            if key != 'number':
                table += '%9.2f,' % (value,)
            else:
                table += '%9d,' % (value,)
        table = table[:-1] + '},    // %s\n' % (name,)
    table += '};\n\n'

    return vocation_str + property_str + table


def item2str(item_dct):
    dct_by_nb = item_dct.items()
    dct_by_nb = sorted(dct_by_nb, key=lambda k: k[1]['number'])
    item_nb = len(dct_by_nb)
    key_infos = {}
    for sub_dct in item_dct.values():
        for key, value in sub_dct.items():
            if isinstance(value, str):
                if key in key_infos:
                    key_infos[key][1].append(value)
                else:
                    key_infos[key] = ('enum', [value])
            elif isinstance(value, int):
                key_infos[key] = ('int', [])
            elif isinstance(value, float):
                key_infos[key] = ('double', [])
            else:
                raise TypeError
    key_infos.pop('macro')
    print(key_infos)

    # enum
    enum_str = ''
    for key_str, info in key_infos.items():
        if info[0] == 'enum':
            enum_str += enum2str('ITEM_' + key_str, info[1])
    enum_str += enum2str('ITEM', [macro for macro, _ in dct_by_nb])

    # property struct
    property_str = 'struct item_property\n{\n'
    for key_str, info in key_infos.items():
        if info[0] == 'enum':
            ctype = ('ITEM_' + key_str).upper()
        else:
            ctype = info[0]
        property_str += '    %s %s;\n' % (ctype, key_str)
    property_str += '};\n\n'

    # data table
    table = 'const item_property ITEM_DATA[%d] = \n{ // ' % (
        item_nb,)
    for key in key_infos.keys():
        table += '%11s' % (key,)
    table += '\n'
    for name, data in dct_by_nb:
        table += '    {'
        for key_str, info in key_infos.items():
            value = data.get(key_str, 0 if info[0] != 'enum' else (
                'ITEM_'+key_str+'_NB').upper())
            if info[0] == 'enum':
                table += '%10s,' % (value,)
            elif info[0] == 'int':
                table += '%10d,' % (value,)
            elif info[0] == 'double':
                table += '%10.2f,' % (value,)
            else:
                raise TypeError
        table = table[:-1] + '},    // %s\n' % (name,)
    table += '};\n\n'

    return enum_str + property_str + table


def sound2str(sound_dct):
    dct_by_nb = sound_dct.items()
    dct_by_nb = sorted(dct_by_nb, key=lambda k: k[1]['number'])
    sound_nb = len(dct_by_nb)
    data_keys = list(dct_by_nb[0][1].keys())

    # property struct
    property_str = 'struct sound_property\n{\n'
    for key in data_keys:
        property_str += '    %s %s;\n' % ('int' if key ==
                                          'number' else 'double', key)
    property_str += '};\n\n'

    # enum
    sound_str = enum2str('SOUND', [macro for macro, _ in dct_by_nb])

    # data table
    table = 'const sound_property SOUND_DATA[%d] = \n{ // ' % (sound_nb,)
    for key in data_keys:
        table += '%10s' % (key,)
    table += '\n'
    for name, data in dct_by_nb:
        table += '    {'
        for key, value in data.items():
            if key != 'number':
                table += '%9.2f,' % (value,)
            else:
                table += '%9d,' % (value,)
        table = table[:-1] + '},    // %s\n' % (name,)
    table += '};\n\n'

    return sound_str + property_str + table

def map2str(map_dct):
    return ''

DEBUG = True


def main():
    argv = sys.argv[1:]
    if not DEBUG:
        if len(argv) == 0:
            print('python const.py <INPUT config file path> <OUTPUT file path>')
            return
        elif len(argv) != 2:
            print('Too many parameters')
            print('python const.py <INPUT config file path> <OUTPUT filepath>')
            return
        else:
            config_path = argv[0]
            constant_path = argv[1]
    else:
        config_path = r'C:\Users\zhang\Desktop\AIchallenge2\logic\config.ini'
        constant_path = 'constant.h'

    constant_dct = load_json(config_path)
    s = '''// Generated by const.py.  DO NOT EDIT!
#ifndef CONSTANT_H
#define CONSTANT_H

struct XYPosition
{
    double x, y;
};

struct PolarPosition
{
    double distance;
    double angle;
};

const double AIRPLANE_SPEED = 5;
const double JUMPING_SPEED = 1;

enum STATUS
{
    RELAX = 0,
    ON_PLANE = 1,
    JUMPING = 2,
    MOVING = 3,
    SHOOTING = 4,
    PICKUP = 5,
    MOVING_SHOOTING = 6,
    DEAD = 7,
    REAL_DEAD = 8
};

'''
    s = s+character2str(constant_dct['CHARACTER'])+item2str(
        constant_dct['ITEM']) + sound2str(constant_dct['SOUND'])
    s += '#endif'
    with open(constant_path, 'w') as const:
        const.write(s)


if __name__ == "__main__":
    main()
