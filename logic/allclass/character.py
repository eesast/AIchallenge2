#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .object import *
from json import load

MOVE = 0
SHOOT = 1
PICKUP = 2
RADIO = 3


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
    VOCATION_COUNT = 5  # an important number to save how many vocations in total

    # enum for status
    RELAX = 0
    ON_PLANE = 1
    JUMPING = 2
    MOVING = 3
    SHOOTING = 4
    PICKUP = 5
    MOVING_SHOOTING = 6
    DEAD = 7

    MOVE_PERMITTED_STATUS = [RELAX, MOVING, MOVING_SHOOTING]
    SHOOTING_PERMITTED_STATUS = [RELAX, MOVING]

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
        self.last_command = None   # save command to deal with information when CD is over

    @staticmethod
    def load_data(parent_path="./", print_debug=PRINT_DEBUG):
        with open(parent_path + CHARACTER_FILE_PATH, "r", encoding="utf-8") as file:
            config_data = load(file)
            if print_debug >= 100:
                print(config_data)
        return

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

    def command_status_legal(self, command_type):
        if command_type == MOVE:
            return self.status in self.MOVE_PERMITTED_STATUS
        elif command_type == SHOOT:
            return self.status in self.SHOOTING_PERMITTED_STATUS
        elif command_type == PICKUP:
            return True
        elif command_type == RADIO:
            return True
        else:
            return False


if __name__ == '__main__':
    # if necessary, test here
    pass
