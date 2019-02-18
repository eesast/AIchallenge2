#ifndef CONSTANT_H
#define CONSTANT_H

using BASE_T = double;
using HP_T = double;
using CD_T = int;
using DURABILITY_T = int;

struct XYPosition
{
    double x, y;
};

struct PolarPosition
{
    double distance;
    double angle;
};

const int MAX_PLAYER = 64;
const int TIMEOUT = 50;
const int MAX_TURN = 100;
const int MEMBER_COUNT = 4;

const BASE_T AIRPLANE_SPEED = 5;
const BASE_T JUMPING_SPEED = 1;

enum VOCATION
{
    MEDIC = 0,
    ENGINEER = 1,
    SIGNALMAN = 2,
    HACK = 3,
    SNIPER = 4,
};

enum STATUS
{
    RELAX = 0,
    ON_PLANE = 1,
    JUMPING = 2,
    MOVING = 3,
    SHOOTING = 4,
    PICKUP = 5,
    MOVING_SHOOTING = 6,
    DEAD = 7,
    REAL_DEAD = 8
};

#endif // !CONSTANT_H