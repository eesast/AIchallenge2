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

const double a[3][4] = {
    {1,2,3,4,},
    {5,6,7,8,},
    {9,0,5,3,},
};

#endif // !CONSTANT_H