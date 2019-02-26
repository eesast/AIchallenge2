#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .object import *
from .position import *
from copy import deepcopy
from math import ceil
from json import load


class Block(Object):
    tree_radius = 1
    next_id = 0

    def __init__(self, type_name):
        # for inherited variables
        super().__init__()
        self.name = type_name
        self.id = None

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
            block.bumped = False
        elif name == 'rectangle_building':
            block.set_rectangle(param)
            block.bumped = True
        elif name == 'circle_building':
            block.set_circle(param)
            block.bumped = True
        elif name == 'wall':
            block.set_rectangle(param)
            block.bumped = True
        elif name == 'tree':
            block.set_circle(param)
            block.bumped = True
        elif name == 'rectangle_grass':
            block.set_rectangle(param)
            block.bumped = False
        elif name == 'circle_grass':
            block.set_circle(param)
            block.bumped = False
        elif name == 'high_point':
            # this one will be deleted, now just waiting for interface's update
            block.set_circle(param)
            block.bumped = False
        else:
            print('resolve failed for block', name)
            assert 0
        return block

    @staticmethod
    def get_id():
        new_id = Block.next_id
        Block.next_id += 1
        return new_id


class Area:
    areas_template = {}

    def __init__(self, name):
        self.blocks = []
        self.name = name
        self.id = None

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

    @staticmethod
    def generate_area(name, number):
        area = deepcopy(Area.areas_template[name])
        area.id = number
        for block in area.blocks:
            block.position += Position(number % 10 * 100, number // 10 * 100)
            block.id = Block.get_id()
        return area


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

    def initialize(self, data):
        for area_type in data:
            self.all_areas.append(Area.generate_area(area_type, len(self.all_areas)))
        # release memory
        Area.areas_template.clear()

    @staticmethod
    def get_id_list(start, over):
        # given two position, return an id list, each of which will be crossed by the straight line of tow positions
        start_id = start.get_area_id()
        over_id = over.get_area_id()
        id_set = set()
        id_set.add(start_id)
        id_set.add(over_id)
        # along y
        if over_id // 10 < start_id // 10:
            start_id, over_id = over_id, start_id
        if over_id // 10 > start_id // 10:
            m = abs((over.x - start.x) / (over.y - start.y))
            for i in range(start_id // 10, over_id // 10):
                y = 100 * (i + 1)
                x = start.x + m * y - start.y
                id_set.add(int(x) // 100 + i * 10)
        # along x
        if over_id % 10 < start_id % 10:
            start_id, over_id = over_id, start_id
        if over_id % 10 > start_id % 10:
            k = abs((over.y - start.y) / (over.x - start.x))
            for i in range(start_id % 10, over_id % 10):
                x = 100 * (i + 1)
                y = start.y + k * x - start.x
                id_set.add(int(y) // 100 * 10 + i)
        id_list = [x for x in id_set if 0 <= x < 100]
        return id_list

    def accessible(self, start, over):
        # given two position, return if a straight line can across blocks
        for area_id in self.get_id_list(start, over):
            for block in self[area_id].blocks:
                if block.bumped and block.is_intersecting(start, over):
                    # intersected! just break
                    break
            else:
                # if "for block in self.map[area_id].blocks" breaks, continue breaking
                break
        else:
            # if breaks the loop, means vision blocked
            return False
        return True
