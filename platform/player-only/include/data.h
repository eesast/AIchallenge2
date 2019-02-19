#ifndef DATA_H
#define DATA_H

#include "./../../include/constant.h"
#include <vector>

struct Item
{
    int item_ID;
    int type;       //should be ENUM
    PolarPosition pos;
    DURABILITY_T durability;
};

struct PoisonInfo
{
    XYPosition current_center;
    XYPosition next_center;
    double current_radius;
    double next_radius;
    int rest_frames;
    // if it's 1, rest_frames means rest frames to move to next status
    // if it's 0, rest_frames means rest frames to start to move
    // if it's -1, the poison ring won't move(has become a node)
    int move_flag;
};

struct SelfInfo
{
    HP_T hp;
    HP_T hp_limit;
    BASE_T move_angle;
    BASE_T view_angle;
    BASE_T move_speed;
    VOCATION vocation;
    int status;     //should be ENUM
    CD_T move_cd;
    CD_T attack_cd;
    XYPosition xy_pos;
    BASE_T view_width;
    BASE_T view_distance;
    std::vector<Item> bag;
};

struct OtherInfo
{
    int player_ID;
    int status;     //should be ENUM
    BASE_T move_angle;
    BASE_T view_angle;
    BASE_T move_speed;
    VOCATION vocation;
    PolarPosition polar_pos;
};

struct Sound
{
    int sender;
    int delay;
    int parameter;      //user-defined
};

struct PlayerInfo
{
    int player_ID;
    SelfInfo self;
    std::vector<int> landform_IDs;
    std::vector<Item> items;        //MAYBE items on the ground
    std::vector<OtherInfo> others;
    std::vector<Sound> sounds;
    PoisonInfo poison;
};


#endif // !DATA_H
