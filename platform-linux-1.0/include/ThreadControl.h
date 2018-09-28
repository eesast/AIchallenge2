#ifndef THREADCONTROL_H
#define THREADCONTROL_H

#include "Header.h"
#include <signal.h>
#include <sys/types.h>
#include <sched.h>
#include <unistd.h>
#include <chrono>
#include <thread>
#include <fcntl.h>
#include <vector>
#include "CState.h"
#include "CDemands.h"

class CPlayerID
{
public:
  friend class ThreadControl;
  ~CPlayerID();
  unsigned int GetID() const;

private:
  CPlayerID(unsigned int playerID = 0) noexcept;
  unsigned int m_playerID;
};

class ThreadControl
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
  ~ThreadControl();
  ThreadControl(int playerCount, CState &state, std::vector<DEMAND> allDemands[], long usedCoreNumber = 0);
  void Run();
  void NotifyOneFinish(pid_t pid);
  void SendDemand(DEMAND d);
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
  CState *pState;
  std::vector<DEMAND> *pAllDemands;
  aiFunc playerFunc[MAX_PLAYER];
};

#endif // !THREADCONTROL_H