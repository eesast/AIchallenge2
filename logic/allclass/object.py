#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .position import *


class Object(object):
    # all entities in the map, should be its subclass instead of object

    # all shapes
    CIRCLE = 0
    RECTANGLE = 1

    def __init__(self, shape=CIRCLE, bumped=False):
        # some basic attributes, mainly for interface
        self.position = Position(0, 0)
        self.shape = shape
        self.move_speed = None
        self.number = -1
        self.block_view = None

        # remember: for security, direction use unit vector
        self.move_direction = None  # record which direction it's heading of
        self.face_direction = None  # record which direction it's facing

        # for circle and rectangle
        self.radius = 0

        # for rectangle, means any diagonal's angle based on x-axis
        self.angle = 0

        # to distinguish if an object can be bumped
        self.bumped = bumped

    def is_intersecting(self, start, over):
        if self.shape == self.CIRCLE:
            if self.position.distance_to_segment(start, over) < self.radius:
                return True
        elif self.shape == self.RECTANGLE:
            angles = [self.angle, 180 - self.angle, self.angle + 180, 360 - self.angle]
            for vector in [angle_to_position(angle) for angle in angles]:
                if segments_intersected(self.position, self.position + vector, start, over):
                    return True
        else:
            assert 0 and "wrong shape"
        return False

    def is_bumped(self, pos, radius):
        if self.shape == Object.CIRCLE:
            return (pos - self.position).length2() >= (radius + self.radius) * (radius + self.radius)
        elif self.shape == Object.RECTANGLE:
            distance = pos.distance_to_rectangle(self.position, self.radius, self.angle)
            return True if distance < 0 else distance < radius
        return True

    def is_opaque(self):
        return self.block_view


if __name__ == '__main__':
    # if necessary, we can test here
    pass
