#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from math import ceil
from json import load


class Sound:
    # some static variables as enum
    RADIO_VOICE = 0
    FOOTSTEP_SOUND = 1
    GUN_SOUND = 2
    BOOM_SOUND = 3
    speed = {}
    farthest = {}

    def __init__(self, sound_type, receiver, pos, distance, emitter=None, data=None):
        self.sound_type = sound_type
        self.emitter = emitter if emitter else -1
        self.receiver = receiver
        self.emitter_position = pos
        self.data = data    # this is radio signal's data
        self.delay = ceil(distance / Sound.speed[self.sound_type])
        self.__delay = self.delay
        return

    # update the sound, turn if the sound hasn't arrived
    def update(self):
        if not self.__delay:
            return False
        self.__delay -= 1
        return True

    # judge if the sound has arrived
    def arrived(self):
        return not self.__delay

    @staticmethod
    def load_data(parent_path, sound_file_path):
        with open(parent_path + sound_file_path, "r", encoding="utf-8") as file:
            data = load(file)
        Sound.RADIO_VOICE = data['RADIO_VOICE']['number']
        Sound.FOOTSTEP_SOUND = data['FOOTSTEP_SOUND']['number']
        Sound.GUN_SOUND = data['GUN_SOUND']['number']
        Sound.BOOM_SOUND = data['BOOM_SOUND']['number']
        for key, value in data.items():
            Sound.speed[value['number']] = value['speed']
            Sound.farthest[key[0: key.find('_')].lower()] = value['distance']
        return data

    def get_data(self, position):
        if not self.data:
            # for environment voice
            # high 3 bits means type
            # low 9 bits means relative angle (int)
            # maybe other information will be added later
            data = self.sound_type << 29
            angle = int((self.emitter_position - position).get_angle())
            data |= angle
            self.data = data
        return self.data


if __name__ == '__main__':
    # if necessary, test here
    pass
