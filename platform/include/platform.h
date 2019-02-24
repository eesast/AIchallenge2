#ifndef PLATFORM_H
#define PLATFORM_H

//struct, header, constant that platform needs

#include "constant.h"
#include <map>
#include <vector>
#include <iostream>
#include <string>
#include <cstdlib>

struct COMMAND_PARACHUTE
{
    VOCATION role;
    XYPosition landing_point;
    int team;
};

enum class COMMAND_TYPE
{
    MOVE = 0,
    SHOOT = 1,
    PICKUP = 2,
    RADIO = 3
};

struct COMMAND_ACTION
{
    COMMAND_TYPE command_type;
    int target_ID;
    double move_angle;
    double view_angle;
    int parameter;
};

using ROUTE_T = std::pair<XYPosition, XYPosition>;


//type of "player_receive" in AI.dll/so
using Recv_Func = void(*)(int, const std::string);
//type of "play_game" in AI.dll/so
using AI_Func = void(*)();
//type of "player_send" in AI.dll/so
using Player_Send_Func = bool(*)(const std::string);
//type of "player_update" in AI.dll/so
using Player_Update = void(*)(int);

#endif