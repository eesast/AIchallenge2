#include "controller.h"
#include "pycalling.h"

std::pair<Position, Position> route;

int main(int argc, char *argv[])
{
    std::string path = ".";
    if(argc>1)
        path = argv[1];
    manager.init(path);
    route = logic.init();
    for (size_t i = 0; i < 5; i++)
    {
        /* code */
        manager.run();
    }

    logic.parachute(manager.get_parachute_commands());
    return 0;
}
