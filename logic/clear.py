#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import os


def main():
    if os.path.exists('playback'):
        if os.path.isdir('playback'):
            os.chdir('playback')
            for file_name in os.listdir('./'):
                if file_name[-3:] == '.pb':
                    os.remove(file_name)
        else:
            print('error! "playback" should be a directory!')
            print('press enter to exit')
            input()
    else:
        os.makedirs('playback')


if __name__ == '__main__':
    main()
