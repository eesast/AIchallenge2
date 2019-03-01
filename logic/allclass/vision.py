#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import intervals
from .position import *


class Vision:
    def __init__(self, angle):
        self.interval = intervals.closed(- angle / 2, angle / 2)

    def see(self, other):
        other = intervals.closed(other[0], other[1])
        if self.interval & other:
            self.interval -= other
            return True
        return False

    def empty(self):
        return len(self.interval) <= 0.1


class AreaManager:
    def __init__(self, position, angle, width, distance):
        self.pos, self.angle, self.width, self.dist2 = position, angle, width, distance * distance
        self.area = self.pos.get_area_id()
        self.current = 0
        self.x = self.area % 10
        self.y = self.area // 10
        area_list = [(abs(area // 10 - self.y) + abs(area % 10 - self.x), area) for area in range(100)]
        area_list.sort(key=lambda x: x[0])
        self.list = [area for dis, area in area_list]

    def get_next_area_id(self):
        while self.current < 100:
            if self.accessible():
                area = self.list[self.current]
                self.current += 1
                return area
            self.current += 1
        return None

    def accessible(self):
        def delta(relative_position):
            theta = abs(relative_position.get_angle() - self.angle)
            if theta > 180:
                theta = 360 - theta
            return theta

        area = self.list[self.current]
        if area == self.area:
            return True
        y, x = area // 10, area % 10
        positions = [Position(x * 100, y * 100),
                     Position(x * 100 + 100, y * 100),
                     Position(x * 100 + 100, y * 100 + 100),
                     Position(x * 100, y * 100 + 100)]
        for pos in positions:
            if pos.distance2(self.pos) < self.dist2 and delta(pos - self.pos) < self.width / 2:
                return True
        return False

    def get_sorted_blocks(self, blocks):
        distance = []
        for block in blocks:
            if not block.is_opaque():
                continue
            dist2 = block.position.distance2(self.pos)
            if 0 < dist2 < self.dist2:
                distance.append((dist2, block))
        distance.sort(key=lambda x: x[0])
        return [block for dist2, block in distance]


if __name__ == '__main__':
    # test here
    pass
