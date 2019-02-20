#! /usr/bin/env python3
# -*- coding: utf-8 -*-
from math import ceil


class Sound:
    # some static variables as enum
    FOOTSTEP_SOUND = 0
    GUN_SOUND = 1
    RADIO_VOICE = 2
    SPEED = {}

    def __init__(self, sound_type, receiver, pos, distance, emitter=None, data=None):
        self.sound_type = sound_type
        self.emitter = emitter if emitter else -1
        self.receiver = receiver
        self.emitter_position = pos
        self.data = data    # this is radio signal's data
        self.delay = ceil(distance / Sound.SPEED[self.sound_type])
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
    def __load_data(parent_path="./"):
        # load SPEED
        pass

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
