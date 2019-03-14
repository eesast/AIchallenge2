#ifndef CONTROLLER_H
#define CONTROLLER_H

#ifdef WIN32
#pragma warning(disable : 4251)
#pragma warning(disable : 4996)
#endif

#include "platform.h"
#include <Windows.h>
#include <mutex>
#include "comm.pb.h"
#include <filesystem>
#include <regex>
#include <vector>
#include <string>
#include <map>
#include <iostream>
#include <fstream>

#define manager (Controller::get_instance())

class Controller
{
    enum class AI_STATE
    {
        UNUSED,
        SUSPENDED,
        ACTIVE,
        DEAD
    };

    //one team
    struct AI_INFO
    {
        int team;
        HMODULE lib;    //AI DLL/SO
        //thread token
        DWORD threadID = 0;
        HANDLE handle = nullptr;
        //thread state
        AI_STATE state = AI_STATE::UNUSED;
        //function pointer for callback
        AI_Func player_func = nullptr;
        Recv_Func recv_func = nullptr;
    };

public:
    //win-only, for CreateThread
    friend DWORD WINAPI thread_func(LPVOID lpParameter);
	friend void controller_update(int);
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
    //find dll in path
    void init(const std::filesystem::path &path, DWORD used_core_count = 0);
private:
    //if init,return true.
    bool _check_init();

    //thread control
public:
    void run();
	bool has_living_player();
private:
    //return -1 if failed
    int _get_playerID_by_threadID();
	void _kill_one(int playerID);

    //communication
public:
    bool receive(const std::string & data);
private:
    void _send(int playerID, int new_frame, const std::string & data);
    //return true on success.
    bool _parse(const std::string & data);

public:
    //always choose the lastest command
    std::map<int, COMMAND_PARACHUTE> get_parachute_commands();
    std::map<int, std::vector<COMMAND_ACTION>> get_action_commands();
private:
    std::string _serialize_route(int playerID);
    std::string _serialize_info(int playerID);


    //singleton
    Controller();
    static Controller _instance;
    bool _is_init = false;

    DWORD _used_core_count;
    DWORD _total_core_count;
    AI_INFO _info[MAX_PLAYER];
    HANDLE* _waiting_thread;    //size == _used_core_count
    int _player_count;
    int _frame;
	std::vector<int> _batch;

    //communication
    std::vector<COMMAND_PARACHUTE> _command_parachute[MAX_PLAYER];
    std::vector<COMMAND_ACTION> _command_action[MAX_PLAYER];
    std::vector<int> _team[MAX_TEAM];
public:     //comm with pycalling
    ROUTE_T route;
    std::map<int, std::string> player_infos;
	std::vector<int> dead;
};

DWORD WINAPI thread_func(LPVOID lpParameter);

//not atomic, maybe cause bugs.
bool controller_receive(const std::string data);
//send data to player immediately
void controller_update(int player_frame);
#endif // !CONTROLLER_H
