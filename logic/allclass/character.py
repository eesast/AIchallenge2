#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .object import *


class Character(Object):                # the base class of all characters
    # static variables
    all_data = []                       # save all data from setting file
    AIRPLANE_SPEED = 5                  # flying speed, will load from file
    JUMPING_SPEED = 1                   # jumping speed, also load from file

    # enum for vocation
    MEDIC = 0
    ENGINEER = 1
    SIGNALMAN = 2
    HACK = 3
    SNIPER = 4

    # enum for status
    RELAX = 0
    ON_PLANE = 1
    JUMPING = 2
    MOVING = 3
    SHOOTING = 4
    PICKUP = 5

    def __init__(self, vocation):
        super().__init__(Object.CIRCLE)
        # define some variables
        self.__heal_point_limit = 100.                  # max HP
        self.heal_point = self.__heal_point_limit       # current HP
        self.bag = []
        self.status = self.RELAX

        # initialize inherit variables
        self.move_direction = None      # moving direction
        self.move_speed = 1.2           # move distance per second
        self.move_cd = 0                # move again in move_cd frames
        self.vocation = vocation            # save the Vocation

        # platform needn't these variables
        self.jump_position = None  # it means where he jump out airplane
        self.land_position = None  # it means where he want to land

    @staticmethod
    def load_data(parent_path="./"):
        if parent_path[-1] != '/':
            parent_path += '/'
        with open(parent_path + DATA_FILE_NAME) as file:
            file_data = file.readlines()
            for line in file_data:
                if line[0] == '#':    # judge if this is comment
                    continue

                # omit the loading code in details temporarily
                Character.all_data.append(line.split(' '))
        pass

    # I use some special function to simplify function in game main
    def is_flying(self):
        return self.status == self.ON_PLANE

    def is_jumping(self):
        return self.status == self.JUMPING

    def move(self):
        # without move direction, needn't move
        if self.move_direction is None:
            return
        # warning: it's not enough, must justify other objects, now just for test
        self.position += self.move_direction * self.move_speed


if __name__ == '__main__':
    # if necessary, test here
    pass
