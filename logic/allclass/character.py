#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from .object import *
from .item import Item
from json import load
from math import exp

MOVE = 0
SHOOT = 1
PICKUP = 2
RADIO = 3


class Character(Object):  # the base class of all characters
    # static variables
    all_data = {}  # save all data from setting file
    AIRPLANE_SPEED = 50  # flying speed, will load from file
    JUMPING_SPEED = 20  # jumping speed, also load from file
    PICKUP_DISTANCE = 1  # pick up farthest distance, load from file

    # save some parameters for calculation
    all_params = {}

    all_characters = {}  # key: id, value: all characters' entities

    # enum for vocation
    MEDIC = 0
    SIGNALMAN = 1
    HACK = 2
    SNIPER = 3
    VOCATION_COUNT = 4  # an important number to save how many vocations in total

    # error
    NO_VOCATION = -1

    # enum for status
    RELAX = 0
    ON_PLANE = 1
    JUMPING = 2
    MOVING = 3
    SHOOTING = 4
    PICKING = 5
    MOVING_SHOOTING = 6
    DEAD = 7
    REAL_DEAD = 8

    MOVE_PERMITTED_STATUS = [RELAX, MOVING, MOVING_SHOOTING, SHOOTING]
    SHOOTING_PERMITTED_STATUS = [RELAX, MOVING]

    def __init__(self, vocation):
        super().__init__(Object.CIRCLE)
        if vocation == Character.NO_VOCATION:
            return
        # define some variables
        self.health_point_limit = Character.all_data[vocation]['hp']  # max HP
        self.health_point = self.health_point_limit  # current HP
        self.bag = {0: 9999}
        self.status = self.RELAX
        self.move_cd = 0  # move finished after move_cd frames
        self.shoot_cd = 0  # shoot finished after move_cd frames
        self.vocation = vocation  # save the Vocation
        self.team = -1  # team id

        # some special variables for view
        self.view_distance = Character.all_data[vocation]['distance']
        self.view_angle = Character.all_data[vocation]['angle']  # view sector's angle

        # initialize some inherited variables
        self.move_speed = Character.all_data[vocation]['move']
        self.radius = Character.all_data[vocation]['radius']
        self.block_view = True

        # platform needn't these variables
        self.jump_position = None  # it means where he jump out airplane
        self.land_position = None  # it means where he want to land

        # these variables are just for interface
        self.last_weapon = -1
        self.best_armor = -1
        self.move_cd_max = None

        # for save the killing information
        self.killer = -1
        self.most_damage = 0

        # save if the character is in some special block
        self.block = None

    @staticmethod
    def load_data(parent_path, character_file_path):
        with open(parent_path + character_file_path, "r", encoding="utf-8") as file:
            config_data = load(file)
        Character.MEDIC = config_data['MEDIC']['number']
        Character.SIGNALMAN = config_data['SIGNALMAN']['number']
        Character.HACK = config_data['HACK']['number']
        Character.SNIPER = config_data['SNIPER']['number']
        for key, value in config_data.items():
            Character.all_data[value['number']] = value
        return config_data

    @staticmethod
    def add_character(new_id, vocation):
        if Character.all_characters.get(new_id, None):
            # this bug is logically impossible
            raise Exception("repeated character id!")
        Character.all_characters[new_id] = Character(vocation)
        Character.all_characters[new_id].number = new_id
        return Character.all_characters[new_id]

    # I use some special function to simplify function in game main
    def is_flying(self):
        return self.status == self.ON_PLANE

    def is_jumping(self):
        return self.status == self.JUMPING

    def is_alive(self):
        return self.status != Character.REAL_DEAD

    def is_picking(self):
        return self.status == self.PICKING

    def can_be_hit(self):
        return self.status != Character.REAL_DEAD and self.status != Character.DEAD

    def can_be_healed(self):
        return self.status != Character.REAL_DEAD

    move_factor = [0, 0.2, 0.5, 0.3]

    def update(self):
        # first initialize some variables for this turn
        self.most_damage = 0

        # then deal with moving
        # without move cd, needn't move
        if self.move_cd == 0:
            return None
        # warning: it's not enough, must justify other objects, now just for test
        if self.is_jumping() or self.is_flying():
            self.position += self.move_direction * self.move_speed
        else:
            move_distance = self.move_speed * Character.all_params['move_step'][self.move_cd]
            new_position = self.position + self.move_direction * move_distance
            if new_position.good(1000):
                self.position = new_position
            else:
                return False
        return True

    def command_status_legal(self, command_type):
        if command_type == MOVE:
            return self.status in self.MOVE_PERMITTED_STATUS
        elif command_type == SHOOT:
            return self.status in self.SHOOTING_PERMITTED_STATUS
        elif command_type == PICKUP:
            return True
        elif command_type == RADIO:
            return True
        else:
            return False

    def change_status(self, new_status):
        # deal with some special new status for cd
        if new_status == Character.MOVING:
            self.move_cd = 3
            self.move_speed = Character.all_data[self.vocation]['move']

        elif new_status == Character.DEAD:
            self.move_cd = 0
            self.shoot_cd = 0

        elif new_status == Character.REAL_DEAD:
            self.move_cd = 0
            self.shoot_cd = 0

        elif new_status == Character.PICKING:
            self.move_cd = 0

        # consider different current status
        if self.status == Character.RELAX:
            pass

        elif self.status == Character.MOVING:
            if new_status == Character.SHOOTING:
                new_status = Character.MOVING_SHOOTING

        elif self.status == Character.SHOOTING:
            if new_status == Character.MOVING:
                new_status = Character.MOVING_SHOOTING

        elif self.status == Character.MOVING_SHOOTING:
            if new_status == Character.RELAX:
                if self.move_cd:
                    new_status = Character.MOVING
                elif self.shoot_cd:
                    new_status = Character.SHOOTING
            elif new_status == Character.MOVING:
                new_status = Character.MOVING_SHOOTING

        elif self.status == Character.PICKING:
            assert self.move_cd == 0
            if self.shoot_cd:
                new_status = Character.SHOOTING

        self.status = new_status
        return True

    def can_make_footsteps(self):
        return not (self.is_jumping() or self.is_flying())

    def get_damage(self, damage, hitter=-1, parameter=None):
        vests = [
            Item.all_data['VEST_1']['number'],
            Item.all_data['VEST_2']['number'],
            Item.all_data["VEST_3"]['number']
        ]
        if self.can_be_healed():
            reduce = 0
            if damage > 0 and parameter != 'ARMOR_PIERCING':
                # here we're supposed to consider vest
                for vest in vests:
                    vest_durability = self.bag.get(vest, 0)
                    if vest_durability:
                        reduce_param = Item.all_data[vest]['reduce']
                        reduce += reduce_param * (1 - exp(- vest_durability / Item.all_data[vest]['durability']))
                        new_durability = self.bag[vest] - reduce_param * damage
                        self.bag[vest] = new_durability if new_durability > 0 else 0
            real_damage = damage - reduce
            self.health_point -= real_damage
            if real_damage > self.most_damage:
                # update the player who give this player most damage in this frame
                self.most_damage = real_damage
                self.killer = hitter
            return real_damage
        else:
            return False

    def equip_scope(self, times):
        self.view_angle = Character.all_data[self.vocation]['angle'] / times
        self.view_distance = Character.all_data[self.vocation]['distance'] / times
        return True

    def get_height(self):
        if not self.is_jumping():
            return 0.
        return 1 - self.move_cd / self.move_cd_max

    def pick_accessible(self, other):
        return self.position.distance(other) <= Character.PICKUP_DISTANCE


if __name__ == '__main__':
    # if necessary, test here
    pass
