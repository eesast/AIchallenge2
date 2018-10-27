#! /usr/bin/env python3
# -*- coding: utf-8 -*-


#   here define file name
DATA_FILE_NAME = "data.ini"

#   here define a debug level variable to debug print-oriented
PRINT_DEBUG = 1
#   level 1: only print illegal information
#   level 2: also print some adjustment


class Object(object):
    # all objects in the map, including players, should be its subclass instead of object

    # all shapes
    CIRCLE = 0
    RECTANGLE = 1

    def __init__(self, shape=CIRCLE):
        # some basic attributes, mainly for interface
        self.position = (None, None)
        self.shape = shape
        self.move_speed = None
        self.number = -1

        # remember: for security, direction use unit vector
        self.move_direction = None  # record which direction it's heading of
        self.face_direction = None  # record which direction it's facing

        # for circle and rectangle
        self.radius = 0

        # for rectangle, means any diagonal's angle based on x-axis
        self.angle = 0


if __name__ == '__main__':
    # if necessary, we can test here
    pass
