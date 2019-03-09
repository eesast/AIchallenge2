#ifndef CONSTANT_H
#define CONSTANT_H

struct XYPosition
{
    double x, y;
};

struct PolarPosition
{
    double distance;
    double angle;
};

const double AIRPLANE_SPEED = 5;
const double JUMPING_SPEED = 1;

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

enum VOCATION
{
    MEDIC = 0,
    SIGNALMAN = 1,
    HACK = 2,
    SNIPER = 3,
    VOCATION_NB = 4,
};

struct vocation_property
{
    int number;
    double hp;
    double distance;
    double angle;
    double radius;
    double move;
    double skill;
};

const vocation_property VOCATION_DATA[4] = 
{ //     number        hp  distance     angle    radius      move     skill
    {        0,   120.00,   200.00,   124.00,     0.50,     1.80,     0.50},    // MEDIC
    {        1,   100.00,   200.00,   124.00,     0.45,     1.60,     2.00},    // SIGNALMAN
    {        2,    90.00,   200.00,   124.00,     0.43,     1.20,     1.00},    // HACK
    {        3,    80.00,   250.00,   115.00,     0.40,     1.00,     1.50},    // SNIPER
};

enum ITEM_TYPE
{
    WEAPON = 0,
    ARMOR = 1,
    GOODS = 2,
    ITEM_TYPE_NB = 3,
};

enum ITEM_MODE
{
    PORTABLE = 0,
    SPENDABLE = 1,
    TRIGGERED = 2,
    ITEM_MODE_NB = 3,
};

enum ITEM
{
    FIST = 0,
    HAND_GUN = 1,
    SUBMACHINE_GUN = 2,
    SEMI_AUTOMATIC_RILE = 3,
    ASSAULT_RIFLE = 4,
    MACHINE_GUN = 5,
    SNIPER_RILFE = 6,
    SNIPER_BARRETT = 7,
    TIGER_BILLOW_HAMMER = 8,
    CROSSBOW = 9,
    VEST_1 = 10,
    VEST_2 = 11,
    VEST_3 = 12,
    MUFFLER = 13,
    BONDAGE = 14,
    FIRST_AID_CASE = 15,
    CODE_CASE = 16,
    ITEM_NB = 17,
};

struct item_property
{
    ITEM_TYPE type;
    int number;
    int durability;
    int range;
    int cd;
    int damage;
    int occur;
    int reduce;
    double param;
    ITEM_MODE mode;
};

const item_property ITEM_DATA[17] = 
{ //        type     number durability      range         cd     damage      occur     reduce      param       mode
    {    WEAPON,         0,      9999,         1,        30,         4,        30,         0,      0.00,ITEM_MODE_NB},    // FIST
    {    WEAPON,         1,         8,        80,         2,         4,        25,         0,      0.00,ITEM_MODE_NB},    // HAND_GUN
    {    WEAPON,         2,        20,       100,         2,         1,        25,         0,      0.00,ITEM_MODE_NB},    // SUBMACHINE_GUN
    {    WEAPON,         3,        15,       150,         1,         3,        30,         0,      0.00,ITEM_MODE_NB},    // SEMI_AUTOMATIC_RILE
    {    WEAPON,         4,        20,       150,         2,         2,        40,         0,      0.00,ITEM_MODE_NB},    // ASSAULT_RIFLE
    {    WEAPON,         5,        50,       100,         3,         1,        40,         0,      0.00,ITEM_MODE_NB},    // MACHINE_GUN
    {    WEAPON,         6,         8,       600,         0,         8,       100,         0,      0.00,ITEM_MODE_NB},    // SNIPER_RILFE
    {    WEAPON,         7,         5,      1000,         0,        10,       150,         0,      0.00,ITEM_MODE_NB},    // SNIPER_BARRETT
    {    WEAPON,         8,        20,         2,        60,         5,        50,         0,      0.00,ITEM_MODE_NB},    // TIGER_BILLOW_HAMMER
    {    WEAPON,         9,        10,       100,         1,         6,        30,         0,      0.00,ITEM_MODE_NB},    // CROSSBOW
    {     ARMOR,        13,       100,         0,         0,         0,        50,         0,      0.00,ITEM_MODE_NB},    // VEST_1
    {     ARMOR,        14,       150,         0,         0,         0,        25,         0,      0.00,ITEM_MODE_NB},    // VEST_2
    {     ARMOR,        15,       200,         0,         0,         0,        10,         0,      0.00,ITEM_MODE_NB},    // VEST_3
    {     GOODS,        21,         0,         0,         0,         0,         0,         0,      0.30,  PORTABLE},    // MUFFLER
    {     GOODS,        22,         0,         0,         0,         0,         5,         0,    -20.00, SPENDABLE},    // BONDAGE
    {     GOODS,        23,         0,         0,         0,         0,         8,         0,   -100.00, SPENDABLE},    // FIRST_AID_CASE
    {     GOODS,        24,         0,         0,         0,         0,         0,         0,      0.00, TRIGGERED},    // CODE_CASE
};

enum SOUND
{
    RADIO_VOICE = 0,
    FOOTSTEP_SOUND = 1,
    GUN_SOUND = 2,
    BOOM_SOUND = 3,
    SOUND_NB = 4,
};

struct sound_property
{
    int number;
    double speed;
    double distance;
};

const sound_property SOUND_DATA[4] = 
{ //     number     speed  distance
    {        0,   500.00,  3000.00},    // RADIO_VOICE
    {        1,    50.00,   100.00},    // FOOTSTEP_SOUND
    {        2,   100.00,   300.00},    // GUN_SOUND
    {        3,   200.00,   600.00},    // BOOM_SOUND
};

#endif