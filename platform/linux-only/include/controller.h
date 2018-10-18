#ifndef CONTROLLER_H
#define CONTROLLER_H

#include "constant.h"
#include <iostream>
#include <cstdlib>
#include <signal.h>
#include <sys/types.h>
#include <sched.h>
#include <unistd.h>
#include <chrono>
#include <thread>
#include <fcntl.h>

#define manager (Controller::get_instance())

void notify_child_finish(int, siginfo_t *info, void *);

class Controller
{
private:
  enum class AI_STATE
  {
    UNUSED,
    SUSPENDED,
    ACTIVE
  };

  struct AI_INFO
  {
    pid_t pid = 0;
    AI_STATE state = AI_STATE::UNUSED;
    // pipe pipe[0] for reading pipe[1] for writing
    int sender[2] = {0, 0};   //server->client
    int receiver[2] = {0, 0}; //client->server
  };

  using AI_Func = void (*)();

public:
  //singleton
  ~Controller();
  Controller(const Controller &) = delete;
  Controller(Controller &&) = delete;
  Controller &operator=(const Controller &) = delete;
  Controller &operator=(Controller &&) = delete;
  static Controller &get_instance()
  {
    return _instance;
  }
  //init() must be called first
  void init(int player_count, long used_core_count = 0);

  void run();
  void notify_one_finish(pid_t pid);
  void send_demand();
  void register_AI(int playerID, AI_Func pfunc);

private:
  //singleton
  static Controller _instance;
  Controller();
  bool _is_init = false;
  //function
  void run_player();
  //data
  AI_INFO _info[MAX_PLAYER];
  int _player_count;
  long _used_core_count;
  long _total_core_count;
  long _used_cpuID;
  int _now_offset;
  int _playerID = 0; //just for childprocess
  AI_Func _player_func[MAX_PLAYER];
};

#endif // !CONTROLLER_H