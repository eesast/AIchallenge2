#include <iostream>
#include"constant.h"
#include "controller.h"
#include "pycalling.h"

std::pair<Position, Position> route;

int main(int argc, char *argv[])
{
    std::string path = ".";
    if (argc > 1)
        path = argv[1];
    manager.init(path);
    route = logic.init();
    for (int i = 0; i < 3; i++)
    {
        manager.run();
        logic.parachute(manager.get_parachute_commands());
    }
    getchar();
    return 0;
}
