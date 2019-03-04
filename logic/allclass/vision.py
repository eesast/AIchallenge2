#! /usr/bin/env python3
# -*- coding: utf-8 -*-
import intervals
from .position import *
from heapq import *
from .item import Item


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

    def __contains__(self, item):
        return item in self.interval


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


class Sweep:

    areas = []

    def __init__(self, player, area_to_players, map_items):
        self.player = player
        self.position = player.position
        self.direction = player.face_direction
        self.angle = player.face_direction.get_angle()
        self.half_view_angle = player.view_angle / 2
        self.view_distance2 = player.view_distance * player.view_distance
        self.area_to_players = area_to_players
        self.map_items = map_items

    def get_visible_areas(self):
        def visible(number):
            distance2, theta = polar_positions[number]
            return distance2 <= self.view_distance2 and abs(theta) < self.half_view_angle

        visible_areas = []
        polar_positions = [self.position.get_polar_position2(self.direction, Position(i * 100, j * 100)) for i in range(
            11) for j in range(11)]
        for i in range(100):
            if visible(i) or visible(i + 1) or visible(i + 10) or visible(i + 11):
                visible_areas.append(i)
        return visible_areas

    def get_potential_targets(self, visible_areas):
        potential = []
        for area_id in visible_areas:
            # blocks
            for block in Sweep.areas[area_id].blocks:
                distance2 = block.position.distance2(self.position)
                if distance2 > self.view_distance2:
                    continue
                relative_angle = self.position.get_angle(block.position)
                if self.half_view_angle < relative_angle < 360 - self.half_view_angle:
                    continue
                potential.append((block, relative_angle, distance2))
            # players
            for player in self.area_to_players.get(area_id, []):
                if player is self.player:
                    pass
                distance2 = player.position.distance2(self.position)
                if distance2 > self.view_distance2:
                    continue
                relative_angle = self.position.get_angle(player.position)
                if self.half_view_angle < relative_angle < 360 - self.half_view_angle:
                    continue
                potential.append((player, relative_angle, distance2))
            for item in self.map_items[area_id // 10][area_id % 10]:
                distance2 = item.position.distance2(self.position)
                if distance2 > self.view_distance2:
                    continue
                relative_angle = self.position.get_angle(item.position)
                if self.half_view_angle < relative_angle < 360 - self.half_view_angle:
                    continue
                potential.append((item, relative_angle, distance2))

        return potential

    def filter_targets(self, potential):
        visible = {}
        targets = []
        for target, angle, distance2 in potential:
            if isinstance(target, Item):
                targets.append((distance2, 0, target))
                targets.append((distance2, 0, target))
            else:
                angles = target.get_tangent_angle(self.position, angle, self.angle)
                targets.append((distance2, angles[0], target))
                targets.append((distance2, angles[1], target))
        # targets' element is (distance2, angle, target)
        # sorted by angle first and distance second
        targets.sort(key=lambda x: (x[1], x[0], x[2].number))
        # for priority queue, will sort by distance, element is (distance2, target) pair
        heap = []
        # for swept dictionary, key is target and value is pair in heap
        swept = {}
        for distance2, angle, target in targets:
            pair = swept.get(target, None)
            if pair:
                # this one has been swept
                if heap[0] is pair:
                    # if this is the nearest, update the pq
                    heappop(heap)
                    while len(heap) and not swept.get(heap[0][1], None):
                        heappop(heap)
                swept.pop(pair[1])
                if len(heap):
                    visible[heap[0][1]] = True
                    if not heap[0][1].block_view:
                        heappop(heap)
            else:
                # this one is just swept
                new_pair = distance2, target
                swept[target] = new_pair
                heappush(heap, new_pair)
                if heap[0][1] is target:
                    visible[target] = True
                if not heap[0][1].block_view:
                    heappop(heap)
        return visible

    def get_visible_targets(self):
        visible_areas = self.get_visible_areas()
        potential_targets = self.get_potential_targets(visible_areas)
        return self.filter_targets(potential_targets)


if __name__ == '__main__':
    # test here
    pass
