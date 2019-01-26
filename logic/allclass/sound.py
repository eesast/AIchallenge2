#! /usr/bin/env python3
# -*- coding: utf-8 -*-


class Sound:
    # some static variables as enum
    FOOTSTEP_SOUND = 0
    GUN_SOUND = 1
    RADIO_VOICE = 2
    SPEED = []

    def __init__(self, sound_type, receiver, emitter=None, distance=0, data=None):
        self.sound_type = sound_type
        self.emitter = emitter
        self.receiver = receiver
        self.distance = distance
        self.__speed = self.SPEED[self.sound_type]
        self.data = data    # this is radio signal's data
        self.__delay = 0

        # manipulate the delay time
        if emitter:
            pass

    # judge if the sound has arrived at receiver now
    def arrived(self):
        if not self.__delay:
            return True
        self.__delay -= 1
        return False

    @staticmethod
    def __load_data(parent_path="./"):
        # load SPEED
        pass


if __name__ == '__main__':
    # if necessary, test here
    pass
