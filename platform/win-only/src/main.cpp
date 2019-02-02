#include <iostream>
#include"constant.h"
#include "controller.h"
#include "pycalling.h"

std::pair<Position, Position> route;

int main(int argc, char *argv[])
{
    //argv[1] is the number of player_count, argv[2] is the current file.
    manager.init(".");
    route = logic.init();
    for (int i = 0; i < 3; i++)
    {
        manager.run();
        logic.parachute(manager.get_parachute_commands());
    }
    getchar();
    return 0;
}
