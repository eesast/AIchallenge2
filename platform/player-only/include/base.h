#ifndef BASE_H
#define BASE_H

//basic tools for communication

#ifdef WIN32
#pragma warning(disable : 4251)
#pragma warning(disable : 4996)

#ifdef AI_EXPORTS
#define PLAYERAI_API __declspec(dllexport)
#else
#define PLAYERAI_API __declspec(dllimport)
#endif // DLL_EXPORTS

#else
#define PLAYERAI_API
#ifndef AI_EXPORTS
#define AI_EXPORTS
#endif // !AI_EXPORTS
#endif // WIN32

#include "./../../include/constant.h"
#include "data.h"
#include "comm.pb.h"
#include <iostream>

extern "C"
{
    PLAYERAI_API void player_receive(bool is_jumping, const std::string data);
    PLAYERAI_API bool player_send(bool is_jumping, const std::string data);
    PLAYERAI_API void bind_api(decltype(&player_send) func);
}

#endif
