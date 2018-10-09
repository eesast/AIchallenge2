#! /usr/bin/env python3
# -*- coding: utf-8 -*-


class Item(object):         # an important basic class for all shown objects
    def __init__(self):
        self.position = (None, None)
        self.shape = None
        self.move_speed = None
        self.move_direction = None
        pass
