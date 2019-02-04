
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import sys
import os

with open("./data/character.json",'r',encoding="utf-8") as f:
    cha=json.load(f)

print('''
#ifndef CONSTANT_H
#define CONSTANT_H

using BASE_T = double;
using HP_T = double;
using CD_T = int;
using DURABILITY_T = int;

struct Position
{
    double x, y;
};

const int MAX_PLAYER = 64;
const int TIMEOUT = 50;
const int MAX_TURN = 100;
const int MEMBER_COUNT = 4;

const BASE_T AIRPLANE_SPEED = 5;
const BASE_T JUMPING_SPEED = 1;
''')
cnum=len(cha)
attrnum=len(cha[list(cha.keys())[0]])
print('enum VOCATION\n{')
for key,val in cha.items():
    print('  ',key,'=',val['number'],',')
print('};\n')
print('enum VOCATION_ATTR\n{')
for i, key in enumerate(cha[list(cha.keys())[0]].keys()):
    print('  ',key,'=',i,',')
print('};\n')

print('const double CHARACTER_ATTR[%d][%d] =\n{' % (cnum,attrnum))
print('  //    ',end='')
for key in cha[list(cha.keys())[0]].keys():
    print(key,end='       ')
print()
for voc, data in cha.items():
    print('  {',end='')
    for val in data.values():
        print("%10.3f" % (val),end=',')
    print('},')
print('};')
print('#endif // !CONSTANT_H')

