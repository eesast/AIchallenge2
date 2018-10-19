#ifndef CONTROLLER_H
#define CONTROLLER_H

#include"constant.h"
#include<Windows.h>
#include<iostream>
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
    using AI_Func = void(*)();

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

    void send_demand();

    void register_AI(int playerID, AI_Func pfunc);
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
};

DWORD WINAPI thread_func(LPVOID lpParameter);

#endif // !CONTROLLER_H
