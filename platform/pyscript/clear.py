#!/usr/bin/env python3
import os
rootdir='/ts20'


def main():
    files = os.listdir(rootdir)
    for file in files:
        file = os.path.join(rootdir, file)
        if(os.path.isfile(file) and os.path.basename(file) != 'platform'):
            os.remove(file)
    
if __name__ == '__main__':
    main()
