#ifndef PLAYERAI_H
#define PLAYERAI_H

#include"./../../../include/constant.h"
#include"./../../../include/character.h"

#include<iostream>
#include<cstdarg>

#ifdef DLL_EXPORTS
#define PLAYERAI_API __declspec(dllexport)
#else
#define PLAYERAI_API __declspec(dllimport)
#endif // DLL_EXPORTS

extern "C"
{
    PLAYERAI_API void __cdecl receive(bool is_parachute, int num, ...);
    PLAYERAI_API void bind_api(void(*func)(VOCATION_TYPE[4], Position[4]));
    PLAYERAI_API void play_game();
}

#endif
