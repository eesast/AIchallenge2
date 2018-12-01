#ifndef CONTROLLER_H
#define CONTROLLER_H

#include"platform.h"
#include<Windows.h>
#include<mutex>

#define manager (Controller::get_instance())

class Controller
{
    enum class AI_STATE
    {
        UNUSED,
        SUSPENDED,
        ACTIVE
    };

    struct AI_INFO
    {
        DWORD threadID = 0;
        HANDLE handle = nullptr;
        AI_STATE state = AI_STATE::UNUSED;
        std::mutex mtx;    //guarantee security of STL used in playerAPI
    };
    


public:

    friend DWORD WINAPI thread_func(LPVOID lpParameter);

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

    void init(int player_count = 0, DWORD used_core_count = 0);
    //parameter is the same as WINAPI CreateThread
    void run();

    void parachute(VOCATION_TYPE role[MEMBER_COUNT], Position landing_points[MEMBER_COUNT]);
    std::map<int, COMMAND_PARACHUTE> get_parachute_commands();
    void register_AI(int playerID, AI_Func pfunc, Recv_Func precv);
private:
    int get_playerID_by_thread();

    //singleton
    Controller();
    static Controller _instance;
    bool _is_init = false;

    DWORD _used_core_count;
    DWORD _total_core_count;
    AI_INFO _info[MAX_PLAYER];
    HANDLE* _waiting_thread;    //size == _used_core_count
    int _now_offset;
    int _player_count;
    AI_Func _player_func[MAX_PLAYER];
    Recv_Func _recv_func[MAX_PLAYER];

    //communication
    std::vector<COMMAND_PARACHUTE>_commands[MAX_PLAYER];
};

DWORD WINAPI thread_func(LPVOID lpParameter);

#endif // !CONTROLLER_H
