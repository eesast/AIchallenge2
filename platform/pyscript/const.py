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
    data_keys = ['CHARACTER', 'ITEM', 'SOUND', 'MAP', 'CIRCLE']
    for data_key in data_keys:
        path = os.path.join(os.path.dirname(config_path),
                            data_paths[data_key+'_FILE_PATH'])
        with open(path, 'r', encoding='utf-8') as data_file:
            data_dct[data_key] = json.load(data_file)
    return data_dct


def enum2str(enum_name, enum_list, ignore_list=[], upper=True):
    ignore_list = [w.upper() if upper else w.lower() for w in ignore_list]
    enum_name = enum_name.upper() if upper else enum_name.lower()
    enum_list2 = list(set(enum_list))
    enum_list2.sort(key=enum_list.index)
    enum_list2 = [w.upper() if upper else w.lower() for w in enum_list2]
    enum_list2 = list(filter(lambda x: not x in ignore_list, enum_list2))
    enum_str = 'enum %s\n{\n' % (enum_name,)
    for i, name in enumerate(enum_list2):
        enum_str += '    %s = %d,\n' % (name, i)
    enum_str += '    %s = %d,\n' % (enum_name +
                                    ('_SZ' if upper else '_sz'), len(enum_list2))
    enum_str += '};\n\n'
    return enum_str


def character2str(character_dct):
    dct_by_nb = character_dct.items()
    dct_by_nb = sorted(dct_by_nb, key=lambda k: k[1]['number'])
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
    table = 'const vocation_property VOCATION_DATA[%s] = \n{ // ' % (
        'VOCATION_SZ',)
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

    # enum
    enum_str = ''
    for key_str, info in key_infos.items():
        if info[0] == 'enum':
            enum_str += enum2str('ITEM_' + key_str, info[1], ignore_list=[''])
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
    table = 'const item_property ITEM_DATA[%s] = \n{ // ' % (
        'ITEM_SZ',)
    for key in key_infos.keys():
        table += '%11s' % (key,)
    table += '\n'
    for name, data in dct_by_nb:
        table += '    {'
        for key_str, info in key_infos.items():
            value = data[key_str]
            if isinstance(value, str) and value == '':
                value = ('ITEM_' + key_str + '_SZ').upper()
            if info[0] == 'enum':
                table += '%*s,' % (12 if key_str == 'mode' else 10, value)
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
    table = 'const sound_property SOUND_DATA[%s] = \n{ // ' % ('SOUND_SZ',)
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
    ignore_list = ['rectangle_walking', 'probability']
    s = ''
    block_shape = ['DOT', 'CIRCLE', 'RECTANGLE']
    s += enum2str('BLOCK_SHAPE', block_shape)
    block_type = []
    for key, value in map_dct.items():
        if key == 'map':
            continue
        else:
            block_type += list(value.keys())
    s += enum2str('BLOCK_TYPE', block_type,
                  ignore_list=ignore_list)
    s += '''
struct block {
    BLOCK_SHAPE shape;
    BLOCK_TYPE type;
    int x0, y0, r, x1, y1;
    //when shape == RECTANGLE, (x0, y0) and (x1, y1) are used (left-top and right-bottom)
    //when shape == CIRCLE, (x0, y0) and r are used (center and radius)
    //when shape == DOT, only (x0, y0) is used as its position
};

'''

    # AREA_DATA
    s += enum2str('AREA', list(map_dct.keys()), ignore_list=['map'])
    # area data table
    area_table = 'const std::vector<block> AREA_DATA[%s] = \n{ //     ' % (
        'AREA_SZ',)
    data_widths = [11, 21, 6, 6, 6, 6, 6]
    data_keys = ['shape', 'type', 'x0', 'y0', 'r', 'x1', 'y2']

    for width, key in zip(data_widths, data_keys):
        area_table += '%*s' % (width, key)
    area_table += '\n'
    for area_name, data in map_dct.items():
        if area_name == 'map':
            continue
        area_table += '    {\n'
        for key, values_list in data.items():
            if not key in ignore_list:
                for values in values_list:
                    # shape
                    area_table += '        {%10s,' % (
                        block_shape[len(values) - 2],)
                    # type
                    area_table += '%20s,' % (key.upper(),)
                    area_table += '%5d,%5d,' % (values[0], values[1])
                    if (len(values) == 3):
                        area_table += '%5d,%5d,%5d},\n' % (values[2], 0, 0)
                    elif (len(values) == 4):
                        area_table += '%5d,%5d,%5d},\n' % (
                            0, values[2], values[3])
                    else:
                        area_table += '%5d,%5d,%5d},\n' % (0, 0, 0)
        area_table += '    },    // %s\n' % (area_name,)
    area_table += '};\n\n'

    # MAP
    map_str = 'const int MAP_SZ = %d;\n\n' % (len(map_dct['map']),)
    map_str += 'const AREA MAP[%s] = \n{\n    ' % ('MAP_SZ',)
    cnt = 0
    for name in map_dct['map']:
        if cnt == 10:
            map_str += '\n    '
            cnt = 0
        map_str += '%10s,' % (name.upper(),)
        cnt += 1
    map_str += '\n};\n\n'
    return s + area_table + map_str


def circle2str(circle_dct):
    dct_by_nb = circle_dct.items()
    dct_by_nb = sorted(dct_by_nb, key=lambda k: int(k[0]))
    data_keys = list(dct_by_nb[0][1].items())
    circle_sz = len(dct_by_nb)

    # property struct
    property_str = 'struct circle_property\n{\n'
    for key, value in data_keys:
        property_str += '    %s %s;\n' % (
            'int' if isinstance(value, int) else 'double', key)
    property_str += '};\n\n'

    # data table
    table = 'const int CIRCLE_SZ = %d;\n\n' % (circle_sz,)
    table += 'const circle_property CIRCLE_DATA[%s] = \n{ // ' % ('CIRCLE_SZ',)
    for key, _ in data_keys:
        table += '%10s' % (key,)
    table += '\n'
    for _, data in dct_by_nb:
        table += '    {'
        for value in data.values():
            if isinstance(value, float):
                table += '%9.2f,' % (value,)
            else:
                table += '%9d,' % (value,)
        table = table[:-1] + '},\n'
    table += '};\n\n'

    return property_str + table


DEBUG = False


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
    s = '''// Generated by const.py.  DO NOT EDIT! DO NOT FORMAT!
//recommend using 1920*1080 zoom 100% to display
#ifndef CONSTANT_H
#define CONSTANT_H

#include <vector>

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
        constant_dct['ITEM']) + sound2str(constant_dct['SOUND']) + \
        map2str(constant_dct['MAP']) + circle2str(constant_dct['CIRCLE'])
    s += '#endif'
    with open(constant_path, 'w') as const:
        const.write(s)


if __name__ == "__main__":
    main()
