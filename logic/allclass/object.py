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

    def get_tangent_angle(self, other):
        # return two angles in [-180, 180]
        if not isinstance(other, Position):
            return
        if self.shape == Object.CIRCLE:
            angle = other.get_angle(self.position)
            cos_theta = self.radius / other.distance(self.position)
            if cos_theta > 1:
                return None
            delta = acos(cos_theta)
            if angle + delta > 360:
                return angle - delta - 360, angle + delta - 360
            else:
                return angle - delta, angle + delta
        else:
            x = self.radius * cos(self.angle)
            y = self.radius * sin(self.angle)
            positions = [Position(x, y) + self.position,
                         Position(-x, y) + self.position,
                         Position(-x, -y) + self.position,
                         Position(x, -y) + self.position]
            if other.x > x:
                if other.y > y:
                    positions = [positions[1], positions[3]]
                elif other.y < y:
                    positions = [positions[0], positions[2]]
                else:
                    positions = [positions[1], positions[2]]
            elif other.x < x:
                if other.y > y:
                    positions = [positions[2], positions[0]]
                elif other.y < y:
                    positions = [positions[3], positions[1]]
                else:
                    positions = [positions[3], positions[0]]
            else:
                if other.y > y:
                    positions = [positions[2], positions[3]]
                elif other.y < y:
                    positions = [positions[0], positions[1]]
                else:
                    return None

            angles = [(pos - other).get_angle() for pos in positions]
            if angles[1] > 180:
                angles[1] -= 360
                angles[0] -= 360
            elif angles[0] > 180:
                angles[0] -= 360
            return angles[0], angles[1]


if __name__ == '__main__':
    # if necessary, we can test here
    pass
