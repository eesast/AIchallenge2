#include "player.h"

extern Position start_pos, over_pos;

void play_game()
{
    
    using namespace std;
    cout << "player" << endl;
    VOCATION_TYPE role[MEMBER_COUNT] = { VOCATION_TYPE::ENGINEER, VOCATION_TYPE::HACK, VOCATION_TYPE::MEDIC, VOCATION_TYPE::SNIPER };
    Position landing_points[MEMBER_COUNT] = { over_pos,start_pos,over_pos,start_pos };
    parachute(role, landing_points);
    return;
}