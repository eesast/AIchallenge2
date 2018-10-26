#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from math import *


class Position:     # this is a class for position and reload some operator
    def __init__(self, x=0., y=0.):
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

    def length(self):   # for position it means length start from (0, 0)
        return sqrt(self.x * self.x + self.y * self.y)

    def length2(self):  # length's square
        return self.x * self.x + self.y * self.y

    def distance(self, other_position):     # distance form other position
        return (self - other_position).length()

    def distance2(self, other_position):    # distance's square
        return (self-other_position).length2()

    def unitize(self, other_position=0):
        if other_position == 0:     # without other position, unitize itself and return self
            self.x = self.x / self.length()
            self.y = self.y / self.length()
            return self
        else:   # else return the unitization(not misspelling) of other position
            return other_position / self.length()

    def good(self, size_x, size_y=0):
        if size_y == 0:
            size_y = size_x
        return 0 <= self.x <= size_x and 0 <= self.y <= size_y


def delta_y(position1, position2):
    return position1.y - position2.y


def delta_x(position1, position2):
    return position1.x - position2.x


def dot_product(position1, position2):
    return position1.x * position2.x + position1.y * position2.y


def cross_product(position1, position2):
    return position1.x * position2.y - position1.y * position2.x

