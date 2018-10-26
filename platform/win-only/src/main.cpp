#include <iostream>
#include "controller.h"
#include "pycalling.h"
#include "item.h"
#include "character.h"
#include "api.h"

int main()
{
    int player_count;
    int turn = 0;
    auto h = LoadLibrary("AI");
    auto play_game = (Controller::AI_Func)GetProcAddress(h, "play_game");
    auto bind_api = (void(*)(void(*func)(Position)))GetProcAddress(h, "bind_api");
    bind_api(jump);
    std::cout << "input the number of players:";
    std::cin >> player_count;
    if (player_count > MAX_PLAYER)
    {
        player_count = MAX_PLAYER;
        std::cerr << "The maxinum number of players is " << MAX_PLAYER << ".Will use " << MAX_PLAYER << " instead." << std::endl;
    }
    manager.init(player_count);
    for (int i = 0; i < player_count; i++)
    {
        manager.register_AI(i, play_game);
    }
    for (logic.init("GameLogic", "game_main"); turn++ < MAX_TURN; logic.do_loop())
    {
        manager.run();
    }
    FreeLibrary(h);
    return 0;
}
