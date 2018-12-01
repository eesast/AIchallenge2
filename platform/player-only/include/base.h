#ifndef BASE_H
#define BASE_H

//basic tools for communication 

#include"./../../include/constant.h"
#include"./../../include/character.h"

#pragma warning(disable:4251)
#include"communication_player.pb.h"

#include<iostream>

#ifdef AI_EXPORTS
#define PLAYERAI_API __declspec(dllexport)
#else
#define PLAYERAI_API __declspec(dllimport)
#endif // DLL_EXPORTS

extern "C"
{
    PLAYERAI_API void player_receive(bool is_jumping, const std::string data);
    PLAYERAI_API bool player_send(bool is_jumping, const std::string data);
    PLAYERAI_API void bind_api(decltype(&player_send) func);  
}

#endif
