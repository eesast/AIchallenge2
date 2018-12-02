#include "player.h"

extern Position start_pos, over_pos;

void play_game()
{
    using namespace std;
    cout << "playeraaaa" << endl;
    VOCATION_TYPE role = VOCATION_TYPE::ENGINEER;
    Position landing_point = { (over_pos.x + start_pos.x) / 2, (over_pos.y + start_pos.y) / 2 };
    parachute(role, landing_point);
    return;
}