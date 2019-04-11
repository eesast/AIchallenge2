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
    // if move_flag is 3, the poison ring won't move(has become a node)
    // if move_flag is 2, rest_frames for (wait->move)
    // if move_flag is 1, rest_frames for (move->wait)
    // if move_flag is 0, rest_frames for (no circle->the 1st circle)
    int move_flag;
    //  0 means hasn't started, 1 means moving
    //  2 means waiting, 3 means over
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
	int angle;		//the relative direction of sound (not radio)
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
