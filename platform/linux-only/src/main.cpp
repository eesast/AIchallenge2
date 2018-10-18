#include <iostream>
#include "controller.h"
#include "pycalling.h"
#include "item.h"
#include "character.h"

Pycalling *pGameLogic = nullptr;

void PlayGame()
{
}



int main()
{
    int playerCount;
    int turn = 0;

    std::cout << "input the number of players:";
    std::cin >> playerCount;
    if (playerCount > MAX_PLAYER)
    {
        playerCount = MAX_PLAYER;
        std::cerr << "The maxinum number of players is " << MAX_PLAYER << ".Will use " << MAX_PLAYER << " instead." << std::endl;
    }
    manager.init(playerCount);
    for (int i = 0; i < playerCount; i++)
    {
        manager.register_AI(i, &PlayGame);
    }
    for (pGameLogic = new Pycalling("GameLogic", "game_main"); turn++ < MAX_TURN; pGameLogic->DoLoop())
    {
        manager.run();
    }
    delete pGameLogic;
    return 0;
}
