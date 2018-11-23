#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .object import *


class LandForm(Object):
    # here are some enums for different landforms
    WALL = 1
    TREE = 2
    # I haven't finish all enums, it's not so urgent

    # here are all objects with circle shape
    CIRCLE_SHAPE = [TREE]   # waiting for finishing
    # here are all objects with
    RECTANGLE_SHAPE = [WALL]    # waiting for finishing

    def __init__(self, land_type):
        if land_type in LandForm.CIRCLE_SHAPE:
            self.shape = Object.CIRCLE
        elif land_type in LandForm.RECTANGLE_SHAPE:
            self.shape = Object.RECTANGLE
        else:
            Exception("wrong type for LandForm!")
        super().__init__(self.shape)
        self.land_type = land_type
        # haven't finished yet, only a start
        if land_type == LandForm.WALL:
            pass


class Vision:
    def __init__(self, id_num=None, distance=0, angle=0):
        self.ID = id_num
        self.distance = distance
        self.angle = angle
