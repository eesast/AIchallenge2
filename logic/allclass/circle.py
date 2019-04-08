#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .position import *
from random import random, gauss
from json import load


class Circle:
    # poison circle (electronic circle indeed)
    def __init__(self, edge):
        self.center_now = None
        self.center_next = None
        self.radius_now = None
        self.radius_next = None
        # 0 means hasn't started, 1 means moving
        # 2 means waiting, 3 means over
        self.flag = 0
        self.shrink = None              # radius shrinking speed
        self.move = None                # center's moving speed
        self.edge = edge
        self.damage_per_frame = None
        self.rest_frames = None
        self.all_data = {}
        # stage number to query data
        self.stage = None

    def load_data(self, parent_path, circle_file_path):
        with open(parent_path + circle_file_path, "r", encoding="utf-8") as file:
            data = load(file)
        for key, value in data.items():
            self.all_data[int(key)] = value
        self.rest_frames = self.all_data[0]['delay']
        return self.all_data

    def start(self):
        # start the circle after the initial waiting frames
        edge = self.edge
        rho = edge + 1
        self.center_now = Position(edge/2, edge/2)
        while rho > edge/4:
            rho = abs(gauss(0, edge/12))
        self.center_next = self.center_now + angle_to_position(random() * 360) * rho
        self.radius_now = edge
        self.radius_next = self.all_data[0]['shrink'] * edge
        self.rest_frames = self.all_data[0]['wait']
        self.stage = 0
        self.flag = 2
        self.damage_per_frame = self.all_data[0]['damage']
        return self.center_next

    def update(self):
        # update circle current status
        assert 0 <= self.flag <= 3 and isinstance(self.flag, int)
        if self.flag == 3:
            # 3 means all over
            return False
        elif self.flag == 2:
            # 2 means the circle is waiting
            self.rest_frames -= 1
            if not self.rest_frames:
                # wait over, start to move
                self.flag = 1
                self.rest_frames = self.all_data[self.stage]['move']
                self.move = (self.center_next - self.center_now) / self.rest_frames
                self.shrink = (self.radius_now - self.radius_next) / self.rest_frames
                return True
        elif self.flag == 1:
            # 1 means the circle is shrinking
            self.rest_frames -= 1
            if not self.rest_frames:
                # move over, next wait
                self.stage += 1
                if not self.all_data.get(self.stage, None):
                    self.flag = 3
                    return True
                self.radius_now = self.radius_next
                self.center_now = self.center_next
                self.radius_next = self.radius_now * self.all_data[self.stage]['shrink']
                new_center = self.get_next_center()
                while not new_center.good(1000):
                    new_center = self.get_next_center()
                self.center_next = new_center
                self.flag = 2
                self.rest_frames = self.all_data[self.stage]['wait']
                self.damage_per_frame = self.all_data[self.stage]['damage']
                return True
            else:
                self.radius_now -= self.shrink
                self.center_now += self.move
        else:
            # 0 means still don't know where is the circle
            self.rest_frames -= 1
            if not self.rest_frames:
                self.start()
                return True
        return False

    def get_next_center(self):
        # get next center randomly
        rho = random() ** 0.5 * (self.radius_now - self.radius_next)
        return self.center_now + angle_to_position(random() * 360) * rho

    def safe(self, player):
        return self.flag == 0 or (player.position - self.center_now).length2() < self.radius_now * self.radius_now

    def is_processing(self):
        return self.flag == 1 or self.flag == 2


if __name__ == '__main__':
    # test place
    # install matplotlib before test
    import matplotlib.pyplot as plt
    c = Circle(1000)
    c.center_now = Position(500, 500)
    c.radius_now = 500
    c.radius_next = 300
    plt.figure(figsize=(6, 6))
    for i in range(1000):
        pos = c.get_next_center()
        print(pos, i)
        plt.plot(pos.x, pos.y, '*', color='black')
    plt.legend()
    plt.show()

