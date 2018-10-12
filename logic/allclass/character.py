#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .object import *
from enum import Enum, unique


@unique
class Vocation(Enum):   # the number for each vacation
    MEDIC = 0
    ENGINEER = 1
    SIGNALMAN = 2
    HACK = 3
    SNIPER = 4


class Character(Object):                # the base class of all characters
    # static variables
    all_data = []                       # save all data from setting file

    def __init__(self, vocation):
        Object.__init__(self)
        # normal attributes
        self.heal_point_limit = 100     # max HP
        self.heal_point = 0             # current HP
        self.move_direction = None      # moving direction
        self.move_speed = 100           # move distance per second
        self.move_cd = 0                # move again in move_cd frames
        self.vocation = vocation            # save the Vocation

        pass

    @staticmethod
    def load_data():
        with open("data.ini") as file:
            file_data = file.readlines()
            for line in file_data:
                if line[0] == '#':    # judge if this is comment
                    continue

                # omit the loading code in details temporarily
                Character.all_data.append(line.split(' '))
        pass


if __name__ == '__main__':
    # if necessary, test here
    pass
