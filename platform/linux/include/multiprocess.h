#ifndef MULTIPROCESS_H
#define MULTIPROCESS_H

#include <iostream>
#include <signal.h>
#include <sys/types.h>
#include <sched.h>
#include <unistd.h>
#include <chrono>
#include <thread>
#include <fcntl.h>

const int TIMEOUT = 50;
const int MAX_PLAYER = 10;

class Multiprocess
{
  private:
    enum PROCESS_STATE
    {
        PROCESS_UNUSED,
        PROCESS_SUSPENDED,
        PROCESS_ACTIVE,
        PROCESS_STATE_MAX
    };

    struct PROCESS_INFO
    {
        pid_t pid = 0;
        PROCESS_STATE state = PROCESS_UNUSED;
        // pipe pipe[0] for reading pipe[1] for writing
        int sender[2] = {0, 0};   //server->client
        int receiver[2] = {0, 0}; //client->server
    };

    using aiFunc = void (*)();

  public:
    ~Multiprocess();
    Multiprocess(int playerCount,long usedCoreNumber = 0);
    void Run();
    void NotifyOneFinish(pid_t pid);
    void SendDemand();
    void Register(int playerID, aiFunc pfunc);

  private:
    void RunPlayer();
    PROCESS_INFO m_processInfo[MAX_PLAYER];
    int m_playerCount;
    long m_usedCoreNumber;
    long m_totalCoreNumber;
    long m_usedCpuID;
    int m_nowOffset;
    int m_playerID = 0; //just for childprocess
    aiFunc playerFunc[MAX_PLAYER];
};

#endif // !MULTIPROCESS_H