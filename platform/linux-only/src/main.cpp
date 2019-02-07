#include "controller.h"
#include "pycalling.h"

int main(int argc, char *argv[])
{
    std::string path = ".";
    if(argc>1)
        path = argv[1];
    manager.init(path);
    manager.route = logic.init();
    manager.run();
    manager.player_infos = logic.parachute(manager.get_parachute_commands());
    //comm_platform::PlayerInfo recv;
    //auto b=recv.ParseFromString(manager.player_infos[0]);
    //std::cout << recv.DebugString();
    for (int i = 0; i < 3; i++)
    {
        manager.run();
        manager.player_infos = logic.do_loop(manager.get_action_commands());
        comm_platform::PlayerInfo recv;
        auto b = recv.ParseFromString(manager.player_infos[0]);
        std::cout << recv.DebugString();
    }
    getchar();
    return 0;
}
