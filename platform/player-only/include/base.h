#ifndef BASE_H
#define BASE_H

//basic tools for communication

#ifdef WIN32
#pragma warning(disable : 4251)
#pragma warning(disable : 4996)
#define PLAYERAI_API __declspec(dllexport)

#else
#define PLAYERAI_API
#endif // WIN32

#include "constant.h"
#include "data.h"
#include "comm.pb.h"
#include <iostream>

bool player_send(const std::string data);
void player_update(int local_frame);
extern "C"
{
    PLAYERAI_API void player_receive(int new_frame, const std::string data);
	PLAYERAI_API void bind_api(decltype(&player_send) func1, decltype(&player_update) func2);
	PLAYERAI_API void play_game();
}

#endif
