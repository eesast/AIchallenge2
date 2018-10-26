#ifndef PLAYERAI_H
#define PLAYERAI_H

#include"./../../../include/constant.h"
#include<iostream>

#ifdef DLL_EXPORTS
#define PLAYERAI_API __declspec(dllexport)
#else
#define PLAYERAI_API __declspec(dllimport)
#endif // DLL_EXPORTS

extern "C" 
{
    PLAYERAI_API void bind_api(void(*func)(Position));
    PLAYERAI_API void play_game(); 
}

#endif
