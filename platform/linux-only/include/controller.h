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
#include <sys/shm.h>
#include <sys/ipc.h>
#include <sys/time.h>
#include "comm.pb.h"
#include "comm_block.h"
#include <filesystem>
#include <dlfcn.h>
#include <regex>
#include <fstream>

#define manager (Controller::get_instance())

void notify_child_finish(int, siginfo_t *info, void *);

class Controller
{
private:
  enum class AI_STATE
  {
    UNUSED,
    SUSPENDED,
    ACTIVE,
    DEAD
  };

  const int CHECK_INTERVAL = 10; //before TIMEOUT, check if all finish per CHECK_INTERVAl(ms);

  struct AI_INFO
  {
    int team;
    void *lib = nullptr;
    pid_t pid = 0;
    AI_STATE state = AI_STATE::UNUSED;
    int frame = -1; //frame of game
    int shmid;
    COMM_BLOCK *shm = nullptr;
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
  void init(const std::filesystem::path &path, std::ofstream& filename2id, long used_core_count = 0);

private:
  bool _check_init();

  //childprocess control
public:
  void run();
  void notify_one_finish(pid_t pid);
  bool has_living_player();

private:
  void _run_player();
  void _kill_one(int playerID);

  //communication
public:
  //only work in client
  bool send_to_server(const std::string &data);

private:
  void _receive_from_client(int playerID); //assume that the lock is locked
  void _send_to_client(int playerID, const std::string &data);
  void _receive_from_server(); //assume that the lock is locked
  //return true on success.
  bool _parse(const std::string &data, int playerID);

public:
  //always choose the lastest command
  std::map<int, COMMAND_PARACHUTE> get_parachute_commands();
  std::map<int, std::vector<COMMAND_ACTION>> get_action_commands();

private:
  std::string _serialize_route(int playerID);
  std::string _serialize_infos(int playerID);

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
  int _playerID = -1; //just for childprocess
  std::vector<int> _batch;
  int _frame = 0;

  //communication
  std::vector<COMMAND_PARACHUTE> _command_parachute[MAX_PLAYER];
  std::vector<COMMAND_ACTION> _command_action[MAX_PLAYER];
  std::vector<int> _team[MAX_TEAM];

public: //comm with pycalling
  ROUTE_T route;
  std::map<int, std::string> player_infos;
  std::vector<int> dead;

public:
  friend void controller_update(int);
};

bool controller_receive(const std::string data);
//send data to player immediately
void controller_update(int);

#endif // !CONTROLLER_H