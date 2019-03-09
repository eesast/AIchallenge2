#ifndef PLATFORM_H
#define PLATFORM_H

//struct, header, constant that platform needs
#include <cstdint>
#include <string>
#include <utility>

struct XYPosition
{
	double x, y;
};

struct PolarPosition
{
	double distance;
	double angle;
};

const int TIMEOUT = 50;
const int MEMBER_COUNT = 4;
const int MAX_TEAM = 16;
const int MAX_PLAYER = MEMBER_COUNT * MAX_TEAM;

struct COMMAND_PARACHUTE
{
    int32_t role;
    int team;
    XYPosition landing_point;
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
	int32_t target_ID;
    double move_angle;
    double view_angle;
	int32_t parameter;
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