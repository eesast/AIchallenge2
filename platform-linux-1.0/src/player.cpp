#include "player.h"

extern CState state;
// extern CDemands demands;    //unused

void PlayGame()
{
    int timeDelay = rand() % 100; //the time that each call uses
    auto start = clock();
    int count = rand() % 3;
    while (clock() - start < timeDelay)
        ;
    for (int i = 0; i < count; i++)
    {
        int cd = rand() % 3 + 1;
        int order = rand() % 3;
        //std::cout << "cd:" << cd << "order:" << order << std::endl;
        //send demand
        SendDemand(cd, order);
    }
    return;
}