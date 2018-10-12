#include <iostream>
#include "multiprocess.h"
#include "pycalling.h"
#include "item.h"
#include "character.h"

const int MAX_TURN = 100;

Multiprocess *pMultiprocess = nullptr;

Pycalling *pGameLogic = nullptr;

void PlayGame()
{
}

void NotifyChildFinish(int, siginfo_t *info, void *)
{
    pid_t sender = info->si_pid;
    if (pMultiprocess != nullptr)
    {
        pMultiprocess->NotifyOneFinish(sender);
    }
}

int main()
{
    int playerCount;
    int turn = 0;
    struct sigaction act;
    act.sa_sigaction = NotifyChildFinish;
    act.sa_flags = SA_SIGINFO;
    sigemptyset(&act.sa_mask);
    sigaction(SIGUSR1, &act, nullptr);
    std::cout << "input the number of players:";
    std::cin >> playerCount;
    if (playerCount > MAX_PLAYER)
    {
        playerCount = MAX_PLAYER;
        std::cerr << "The maxinum number of players is " << MAX_PLAYER << ".Will use " << MAX_PLAYER << " instead." << std::endl;
    }
    pMultiprocess = new Multiprocess(playerCount);
    for (int i = 0; i < playerCount; i++)
    {
        pMultiprocess->Register(i, &PlayGame);
    }
    for (pGameLogic = new Pycalling("GameLogic", "game_main"); turn++ < MAX_TURN; pGameLogic->DoLoop())
    {
        pMultiprocess->Run();
    }
    delete pGameLogic;
    delete pMultiprocess;
    return 0;
}
