#include "player.h"
#include <thread>
#include <chrono>
#include <cstdlib>
#include <ctime>

extern XYPosition start_pos, over_pos;
extern std::vector<int> teammates;
extern int frame;
extern PlayerInfo info;

void play_game()
{
    srand(time(nullptr));
    int delay = rand() % 1000;
    std::cout << "playeraaaa:frame" << frame << std::endl;
    VOCATION role = VOCATION::ENGINEER;
    XYPosition landing_point = { (over_pos.x + start_pos.x) / 2, (over_pos.y + start_pos.y) / 2 };
    //std::this_thread::sleep_for(std::chrono::milliseconds(delay));
    parachute(role, landing_point);
    move(12, 23, 0);
    return;
}