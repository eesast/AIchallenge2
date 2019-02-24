#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .object import *
from .position import *
from math import ceil
from json import load


class Block(Object):
    tree_radius = 1

    def __init__(self, type_name):
        # for inherited variables
        super().__init__()
        self.name = type_name

    def set_rectangle(self, param):
        self.shape = Object.RECTANGLE
        left_up = Position(param[0], param[1])
        right_down = Position(param[2], param[3])
        self.position = (left_up + right_down) / 2
        self.radius = abs(left_up - right_down) / 2
        self.angle = - (right_down - left_up).get_angle()

    def set_circle(self, param):
        self.shape = Object.CIRCLE
        self.position = Position(param[0], param[1])
        self.radius = param[2] if len(param) == 3 else Block.tree_radius

    @staticmethod
    def generate_block(name, param):
        block = Block(name)
        if name == 'deep_water':
            block.set_rectangle(param)
            block.bumped = True
        elif name == 'shallow_water':
            block.set_rectangle(param)
        elif name == 'rectangle_building':
            block.set_rectangle(param)
        elif name == 'circle_building':
            block.set_circle(param)
        elif name == 'wall':
            block.set_rectangle(param)
        elif name == 'tree':
            block.set_circle(param)
        elif name == 'rectangle_grass':
            block.set_rectangle(param)
        elif name == 'circle_grass':
            block.set_circle(param)
        elif name == 'high_point':
            # this one will be deleted, now just waiting for interface's update
            block.set_circle(param)
        else:
            print('resolve failed for block', name)
            assert 0
        return block


class Area:
    areas_template = {}

    def __init__(self, name):
        self.blocks = []
        self.name = name

    @staticmethod
    def load_data(parent_path, circle_file_path):
        with open(parent_path + circle_file_path, "r", encoding="utf-8") as file:
            data = load(file)
        map_data = None
        for key, values in data.items():
            if key == 'map':
                map_data = values
            else:
                area = Area(key)
                for block_type, block_params in values.items():
                    for param in block_params:
                        area.blocks.append(Block.generate_block(block_type, param))
                Area.areas_template[key] = area

        return map_data


class Map:

    def __init__(self):
        self.all_areas = []
        pass

    def __getitem__(self, item):
        if isinstance(item, tuple):
            # warning: this tuple's element should be index instead of position
            item = item[0] + item[1] * 10
        elif isinstance(item, Position):
            item = ceil(item.x / 100) + ceil(item.y / 100) * 10
        assert isinstance(item, int)
        return self.all_areas[item]

    def get_block(self, area_index, block_index):
        relative_block = self.all_areas[area_index].blocks[block_index]
        block = Block(relative_block.name)
        block.shape = relative_block.shape
        block.radius = relative_block.radius
        block.angle = relative_block.angle
        block.position = relative_block.position + Position(area_index % 10 * 100, area_index // 10 * 100)
        return block

    def initialize(self, data):
        for area_type in data:
            self.all_areas.append(Area.areas_template[area_type])

