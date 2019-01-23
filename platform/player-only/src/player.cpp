#include "player.h"
#include <thread>
#include <chrono>
#include <cstdlib>
#include <ctime>

extern Position start_pos, over_pos;

void play_game()
{
    srand(time(nullptr));
    int delay = rand() % 1000;

    using namespace std;
    cout << "playeraaaa" << endl;
    VOCATION_TYPE role = VOCATION_TYPE::ENGINEER;
    Position landing_point = { (over_pos.x + start_pos.x) / 2, (over_pos.y + start_pos.y) / 2 };
    std::this_thread::sleep_for(std::chrono::milliseconds(delay));
    parachute(role, landing_point);
    return;
}