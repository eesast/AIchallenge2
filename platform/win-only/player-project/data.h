#ifndef DATA_H
#define DATA_H

#include "constant.h"
#include <vector>
#include <cstdint>

struct Item
{
    int item_ID;
    ITEM type;
    PolarPosition polar_pos;
    int durability;
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
    double hp;
    double hp_limit;
	double move_angle;
	double view_angle;
	double move_speed;
    VOCATION vocation;
    STATUS status;
    int move_cd;
    int attack_cd;
    XYPosition xy_pos;
	double view_width;
	double view_distance;
    std::vector<Item> bag;
};

struct OtherInfo
{
    int player_ID;
	STATUS status;     //should be ENUM
	double move_angle;
	double view_angle;
	double move_speed;
    VOCATION vocation;
    PolarPosition polar_pos;
};

struct Sound
{
    int sender;
    int delay;
	SOUND type;
    int32_t parameter;      //user-defined
};

struct PlayerInfo
{
    int player_ID;
    SelfInfo self;
    std::vector<int> landform_IDs;
    std::vector<Item> items;        //items on the ground
    std::vector<OtherInfo> others;
    std::vector<Sound> sounds;
    PoisonInfo poison;
};


#endif // !DATA_H
