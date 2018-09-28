#include "CState.h"
#include "CDemands.h"
#include "PyCalling.h"
#include "ThreadControl.h"
#include "player.h"

//read only
CState state;
CDemands demands;
unsigned playerCount;

//player write by API
std::vector<DEMAND> allDemands[MAX_PLAYER];

ThreadControl *pThreadController = nullptr;

PyCalling *pGameLogic = nullptr;

void NotifyChildFinish(int , siginfo_t *info, void *)
{
    pid_t sender = info->si_pid;
    if (pThreadController != nullptr)
    {
        pThreadController->NotifyOneFinish(sender);
    }
}

int main()
{
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
    pThreadController = new ThreadControl(playerCount, state, allDemands);
    for (int i = 0; i < playerCount; i++)
    {
        pThreadController->Register(i, &PlayGame);
    }
    for (pGameLogic = new PyCalling("GameLogic", "game_init", "game_main", state, demands, allDemands, playerCount); state.GetTurn() < MAX_TURN; pGameLogic->DoLoop())
    {
        pThreadController->Run();
    }
    delete pGameLogic;
    delete pThreadController;
    return 0;
}
