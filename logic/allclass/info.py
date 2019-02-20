#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .character import *


class Information:
    def __init__(self, player):
        if not isinstance(player, Character):
            raise Exception("wrong player type!")
        self.id = player.number
        self.hp_max = player.health_point
        self.items = []
        self.landform = []
        self.others = []
        self.sounds = []

    def update(self):
        pass

    def clear(self):
        self.items.clear()
        self.landform.clear()
        self.others.clear()
        self.sounds.clear()
