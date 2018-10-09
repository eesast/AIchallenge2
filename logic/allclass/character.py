#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .item import *
from enum import Enum


class Character(object, Item):                # the base class of all characters
    # static variables
    all_data = []                       # save all data from setting file

    def __init__(self, vocation):
        # normal attributes
        self.heal_point_limit = 100     # max HP
        self.heal_point = 0             # current HP
        self.move_direction = None      # moving direction
        self.move_speed = 100           # move distance per second
        self.move_cd = 0                # move again in move_cd frames

        # special flags for each vocation
        self.medic_aid = False               # for medic
        self.engineer_manipulation = False   # for engineer
        self.signalman_enhance = False       # for signalman
        self.hacker_technology = False       # for hacker
        self.sniper_double = False           # for sniper

        pass

    def load_data(self):
        with open("character.ini") as file:
            file_data = file.readlines()
            for line in file_data:
                if line[0] == '#':    # judge if this is comment
                    continue
                self.all_data.append(line.split(' '))
        pass
