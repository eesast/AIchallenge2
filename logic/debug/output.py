#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from json import *
from random import *


def get_tuple():
    return randrange(0, 100000)/100, randrange(0, 100000)/100


def main():
    information = {
            0: {'vocation': 0, 'position': (100, 200)},
            1: {'vocation': 1, 'position': (100, 200)},
            2: {'vocation': 2, 'position': (100, 200)},
            3: {'vocation': 3, 'position': (100, 200)},
            4: {'vocation': 1, 'position': (100, 200)},
            5: {'vocation': 2, 'position': (100, 200)},
            6: {'vocation': 3, 'position': (100, 200)},
            7: {'vocation': 4, 'position': (100, 200)},
            8: {'vocation': 2, 'position': (100, 200)},
            9: {'vocation': 3, 'position': (100, 200)},
            10: {'vocation': 4, 'position': (100, 200)},
            11: {'vocation': 1, 'position': (100, 200)}
    }
    for i in range(12):
        # information[i]['position'] = get_tuple()
        information[i]['team'] = i
    file = open("input.json", 'w', encoding='utf-8')
    dump(information, file)


if __name__ == '__main__':
    main()
