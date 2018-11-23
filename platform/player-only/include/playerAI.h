#ifndef PLAYERAI_H
#define PLAYERAI_H

#include"./../../include/constant.h"
#include"./../../include/character.h"
#include"communication_player.pb.h"
#include"./../../include/api.h"


#include<iostream>
#include<cstdarg>

#ifdef AI_EXPORTS
#define PLAYERAI_API __declspec(dllexport)
#else
#define PLAYERAI_API __declspec(dllimport)
#endif // DLL_EXPORTS

extern "C"
{
    PLAYERAI_API void player_receive(bool is_parachute, const std::string data);
    PLAYERAI_API bool player_send(bool is_parachute, const std::string data);
    PLAYERAI_API void bind_api(decltype(&player_send) func);
    PLAYERAI_API void play_game();
}

#endif
