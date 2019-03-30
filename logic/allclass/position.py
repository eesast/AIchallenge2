#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from math import *


class Position:  # this is a class for position and reload some operator
    def __init__(self, x, y=0.):
        if isinstance(x, Position):
            self.x, self.y = x.x, x.y
        elif isinstance(x, tuple):
            self.x, self.y = x[0], x[1]
        else:
            self.x, self.y = x, y

    def __add__(self, other_position):
        return Position(self.x + other_position.x, self.y + other_position.y)

    def __sub__(self, other_position):
        return Position(self.x - other_position.x, self.y - other_position.y)

    def __abs__(self):
        return self.length()

    def __mul__(self, other):
        if isinstance(other, Position):
            return dot_product(self, other)
        elif isinstance(other, int) or isinstance(other, float):
            return Position(self.x * other, self.y * other)
        else:
            raise Exception("wrong type for * of Position!")

    def __truediv__(self, number):
        return Position(self.x / number, self.y / number)

    def __str__(self):
        return "(%g,%g)" % (self.x, self.y)

    def length(self):  # for position it means length start from (0, 0)
        return sqrt(self.x * self.x + self.y * self.y)

    def length2(self):  # length's square
        return self.x * self.x + self.y * self.y

    def distance(self, other_position):  # distance form other position
        return (self - other_position).length()

    def distance2(self, other_position):  # distance's square
        return (self - other_position).length2()

    def unitize(self, other_position=0):
        if other_position == 0:  # without other position, unitize itself and return self
            length = self.length()
            if length:
                self.x = self.x / length
                self.y = self.y / length
            return self
        else:  # else return the unitization(not misspelling) of other position
            return other_position / self.length()

    def good(self, size_x, size_y=0):
        if size_y == 0:
            size_y = size_x
        return 0 <= self.x <= size_x and 0 <= self.y <= size_y

    # it should be in [0,360)
    def get_angle(self, other=None):
        if other is None:
            # get the angle of the vector itself
            angle = atan2(self.y, self.x) * 180 / pi
            return angle if angle >= 0 else angle + 360

        # get the angle for two vector
        length_product = sqrt(self.length2() * other.length2())
        if length_product < 1e-5:
            return 0
        cos_theta = self * other / length_product
        # avoid cos number > 1 because of calculate precision
        if cos_theta > 1:
            theta = 0
        elif cos_theta < -1:
            theta = 180
        else:
            theta = acos(cos_theta) * 180 / pi
        if cross_product(self, other) < 0:
            theta = 360 - theta
        return theta

    def get_polar_position(self, direction, other):
        if not (isinstance(other, Position) and isinstance(direction, Position)):
            raise Exception("wrong type of position!")
        distance = self.distance(other)
        theta = direction.get_angle(other - self)
        return distance, theta

    def get_polar_position2(self, direction, other):
        # return length2 instead of length to optimize the algorithm
        distance2 = self.distance2(other)
        theta = direction.get_angle(other - self)
        return distance2, theta

    def get_area_id(self):
        return int(self.y) // 100 * 10 + int(self.x) // 100

    def distance_to_segment(self, start, over):
        if cross_product(self - start, over - start) * cross_product(self - over, start - over) >= 0:
            distance = abs(cross_product(self - start, over - start)) / abs(over - start)
        else:
            distance = min(abs(self - start), abs(self - over))
        return distance

    def distance_to_rectangle(self, center, radius, angle):
        # get distance to a rectangle's edge
        # return -1 if self is in the rectangle
        distance, theta = center.get_polar_position(Position(1, 0), self)
        if theta >= 180:
            theta -= 180
        if theta >= 90:
            theta = 180 - theta
        theta = theta * pi / 180
        angle = angle * pi / 180
        dx = distance * cos(theta) - radius * cos(angle)
        dy = distance * sin(theta) - radius * sin(angle)
        if dx < 0:
            return -1 if dy < 0 else dy
        else:
            return dx if dy < 0 else abs(Position(dx, dy))


def delta_y(position1, position2):
    return position1.y - position2.y


def delta_x(position1, position2):
    return position1.x - position2.x


def dot_product(position1, position2):
    return position1.x * position2.x + position1.y * position2.y


def cross_product(position1, position2):
    return position1.x * position2.y - position1.y * position2.x


def angle_to_position(angle):
    while angle > 180:
        angle -= 360
    angle = angle * pi / 180
    return Position(cos(angle), sin(angle))


def segments_intersected(start1, over1, start2, over2):
    vectors = [start2 - start1, over1 - start2, over2 - over1, start1 - over2]
    param = sum([1 if cross_product(vectors[i], vectors[(i + 1) % 4]) > 0 else -1 for i in range(4)])
    return param == 4 or param == -4
