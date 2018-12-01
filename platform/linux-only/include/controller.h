#ifndef CONTROLLER_H
#define CONTROLLER_H

#include "platform.h"
#include <signal.h>
#include <sys/types.h>
#include <sched.h>
#include <unistd.h>
#include <chrono>
#include <thread>
#include <fcntl.h>
#include "communication_platform.pb.h"

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

    AI_Func player_func = nullptr;
    Recv_Func recv_func = nullptr;
  };

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
  //manager init
public:
  void init(int player_count = 0, long used_core_count = 0);
  void register_AI(int playerID, AI_Func pfunc, Recv_Func precv);

private:
  bool _check_init();

  //childprocess control
public:
  void run();
  void notify_one_finish(pid_t pid);

private:
  void _run_player();

  //communication
public:
  bool receive(bool is_jumping, const std::string &data);

private:
  void _send(int playerID, bool is_jumping, const std::string &data);
  //return true on success.
  bool _parse_parachute(const std::string &data);
  bool _parse_commands(const std::string &data);

public:
  //always choose the lastest command
  std::map<int, COMMAND_PARACHUTE> get_parachute_commands();

private:
  std::string _serialize_route();

private:
  //singleton
  static Controller _instance;
  Controller();
  bool _is_init = false;
  //data
  AI_INFO _info[MAX_PLAYER];
  int _player_count;
  long _used_core_count;
  long _total_core_count;
  long _used_cpuID;
  int _now_offset;
  int _playerID = -1; //just for childprocess

  //communication
  std::vector<COMMAND_PARACHUTE> _command_parachute[MAX_PLAYER];
  std::vector<COMMAND_ACTION> _command_action[MAX_PLAYER];
};

bool controller_receive(bool is_jumping, const std::string data);

#endif // !CONTROLLER_H