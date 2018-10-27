#include"playerAI.h"

Position start_pos, over_pos;

void(*parachute)(VOCATION_TYPE[MEMBER_COUNT], Position[MEMBER_COUNT]) = nullptr;

void receive(bool is_parachute, int num, ...)
{
    va_list valist;
    va_start(valist, num);
    if (is_parachute)
    {
        start_pos = va_arg(valist, Position);
        over_pos = va_arg(valist, Position);
    }
    else
    {

    }
    va_end(valist);
}


void bind_api(decltype(parachute) func)
{
    parachute = func;
}
void play_game()
{
    using namespace std;
    cout << "player" << endl;
    VOCATION_TYPE role[MEMBER_COUNT] = { VOCATION_TYPE::ENGINEER, VOCATION_TYPE::HACK, VOCATION_TYPE::MEDIC, VOCATION_TYPE::SNIPER };
    Position landing_points[MEMBER_COUNT] = { over_pos,start_pos,over_pos,start_pos };
    parachute(role, landing_points);
    return;
}
