#ifndef CONTROLLER_H
#define CONTROLLER_H

#include"platform.h"
#include<Windows.h>
#include<mutex>
#include"communication_platform.pb.h"

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
    void init(int player_count = 0, DWORD used_core_count = 0);
    void register_AI(int playerID, AI_Func pfunc, Recv_Func precv);
private:
    //if init,return true.
    bool _check_init();

    //thread control
public:
    void run();
private:
    int get_playerID_by_thread();

    //communication
public:
    bool receive(bool is_jumping, const std::string & data);
    void send(int playerID, bool is_jumping, const std::string & data);



    void parachute(VOCATION_TYPE role[MEMBER_COUNT], Position landing_points[MEMBER_COUNT]);
    std::map<int, COMMAND_PARACHUTE> get_parachute_commands();
private:
    std::string _serialize_route();


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


    //communication
    std::vector<COMMAND_PARACHUTE>_commands[MAX_PLAYER];
};

DWORD WINAPI thread_func(LPVOID lpParameter);

//not atomic, maybe cause bugs.
bool controller_receive(bool is_jumping, const std::string data);

#endif // !CONTROLLER_H
