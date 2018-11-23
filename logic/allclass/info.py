#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .character import *


class Information:
    def __init__(self, player):
        if not isinstance(player, Character):
            raise Exception("wrong player type!")
        self.player = player
        self.vision = []
        self.sound = []

    def clear(self):
        self.vision.clear()
        self.sound.clear()
