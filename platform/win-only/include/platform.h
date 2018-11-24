#ifndef PLATFORM_H
#define PLATFORM_H

//struct, header, constant that platform needs

#include"constant.h"
#include"character.h"
#include<map>
#include<vector>
#include <iostream>
#include <string>
#include <cstdlib>

struct COMMAND_PARACHUTE
{
    VOCATION_TYPE role[MEMBER_COUNT];
    Position landing_points[MEMBER_COUNT];
    COMMAND_PARACHUTE() {}
    COMMAND_PARACHUTE(const COMMAND_PARACHUTE &other)
    {
        for (int i = 0; i < MEMBER_COUNT; i++)
        {
            role[i] = other.role[i];
            landing_points[i] = other.landing_points[i];
        }
    }
};

//type of "player_receive" in AI.dll 
using Recv_Func = void(*)(bool, const std::string);
//type of "play_game" in AI.dll 
using AI_Func = void(*)();
//type of "player_send" in AI.dll 
using Player_Send_Func = bool(*)(bool, const std::string);

#endif