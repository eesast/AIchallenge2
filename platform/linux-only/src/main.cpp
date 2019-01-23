#include "controller.h"
#include "pycalling.h"
#include <dlfcn.h>

std::pair<Position, Position> route;

int main(int argc, char *argv[])
{
    if (argc <= 1)
    {
        std::cerr << "Please enter the number of players" << std::endl;
        return 0;
    }
    int player_count = atoi(argv[1]);
    if (player_count > MAX_PLAYER)
    {
        player_count = MAX_PLAYER;
        std::cerr << "The maxinum number of players is " << MAX_PLAYER << ".Will use " << MAX_PLAYER << " instead." << std::endl;
    }
    auto h = dlopen("./libAI.so", RTLD_NOW);
    manager.init(player_count);
    for (int i = 0; i < player_count; i++)
    {
        auto play_game = (AI_Func)dlsym(h, "play_game");
        auto bind_api = (void (*)(Player_Send_Func))dlsym(h, "bind_api");
        auto player_receive = (Recv_Func)dlsym(h, "player_receive");
        bind_api(&controller_receive);
        manager.register_AI(i, play_game, player_receive);
    }
    route = logic.init();

    for (size_t i = 0; i < 5; i++)
    {
        /* code */
        manager.run();
    }

    logic.parachute(manager.get_parachute_commands());
    dlclose(h);
    return 0;
}
