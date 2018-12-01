#include "controller.h"

extern std::pair<Position, Position> route;

Controller Controller::_instance;

void Controller::init(int player_count, DWORD used_core_count)
{
    _player_count = player_count;
    _waiting_thread = nullptr;
    //get core number
    SYSTEM_INFO systemInfo;
    GetSystemInfo(&systemInfo);
    _total_core_count = systemInfo.dwNumberOfProcessors;
    if (used_core_count == 0 || used_core_count > _total_core_count)
    {
        _used_core_count = _total_core_count;
    }
    else
    {
        _used_core_count = used_core_count;
    }
    _waiting_thread = new HANDLE[_used_core_count];
    _is_init = true;
}

bool Controller::_check_init()
{
    if (!_is_init)
    {
        std::cerr << "Manager is not initialised,please check codes." << std::endl;
    }
    return _is_init;
}

Controller::~Controller()
{
    if (!_check_init())
        return;
    for (int i = 0; i < _player_count; i++)
    {
        if (_info[i].state != AI_STATE::UNUSED)
        {
            TerminateThread(_info[i].handle, 0);
            CloseHandle(_info[i].handle);
        }
    }
    delete _waiting_thread;
    _waiting_thread = nullptr;
}

void Controller::run()
{
    if (!_check_init())
        return;
    for (int offset = 0; offset < _player_count; offset += _used_core_count)
    {
        _now_offset = offset;
        //execute some players each loop. The number is equal to the number of core(_used_core_count) 
        for (int i = 0; i < static_cast<int>(_used_core_count) && offset + i < _player_count; i++)
        {
            //clear commands vector
            _command_parachute[offset + i].clear();
            //offset + i == playerID
            if (_info[offset + i].state == AI_STATE::UNUSED)
            {
                //create or recreate a subthread.
                _info[offset + i].handle = CreateThread(nullptr, 0, thread_func, nullptr, CREATE_SUSPENDED, &_info[offset + i].threadID);
                if (_info[offset + i].handle == NULL)
                {
                    DWORD errorCode = GetLastError();
                    std::cerr << "Cannot create thread. Error Code: " << errorCode << std::endl;
                    system("pause");
                    exit(1);
                }
                _info[offset + i].state = AI_STATE::SUSPENDED;
                //CPU control, choose the core which the thread uses. When the used core number is less than that CPU actually has, using core with higher ID firstly 
                SetThreadAffinityMask(_info[offset + i].handle, (static_cast<DWORD_PTR>(1) << ((_total_core_count - _used_core_count) + i)));
            }
            _waiting_thread[i] = _info[offset + i].handle;    //if the player's thread is suspended, just resume it
        }
        //send route and start subthread.
        for (int i = 0; i < static_cast<int>(_used_core_count) && offset + i < _player_count; i++)
        {
            _info[offset + i].state = AI_STATE::ACTIVE;
            (*_info[offset + i].recv_func)(true, _serialize_route());
            ResumeThread(_info[offset + i].handle);
        }
        DWORD threadNumber = (_player_count - offset >= static_cast<int>(_used_core_count) ? _used_core_count : static_cast<DWORD>(_player_count - offset));
        //let sunthreads run TIMEOUT ms.
        if (WaitForMultipleObjects(threadNumber, _waiting_thread, true, TIMEOUT) == WAIT_TIMEOUT)
        {    //if one thread does not exit 
            DWORD exitCode;
            for (int i = 0; i < static_cast<int>(_used_core_count) && offset + i < _player_count; i++)
            {    //look out still active thread and suspend it forcefully
                GetExitCodeThread(_info[offset + i].handle, &exitCode);
                if (exitCode == STILL_ACTIVE)
                {
                    _info[offset + i].state = AI_STATE::SUSPENDED;
                    SuspendThread(_info[offset + i].handle);
                }
                else
                {
                    _info[offset + i].state = AI_STATE::UNUSED;
                    CloseHandle(_info[offset + i].handle);
                }
            }
        }
        else
        {
            for (int i = 0; i < static_cast<int>(_used_core_count) && offset + i < _player_count; i++)
            {
                _info[offset + i].state = AI_STATE::UNUSED;
                CloseHandle(_info[offset + i].handle);
            }
        }
    }
}

bool Controller::receive(bool is_jumping, const std::string & data)
{
    if (!_check_init())
        return false;
    if (is_jumping)
    {
        return _parse_parachute(data);
    }
    else
    {
        return _parse_commands(data);
    }
}

void Controller::_send(int playerID, bool is_jumping, const std::string & data)
{
    if (!_check_init())
        return;
    _info[playerID].recv_func(is_jumping, data);
    return;
}

bool Controller::_parse_parachute(const std::string & data)
{
    comm_platform::Parachute recv;
    auto playerID = _get_playerID_by_threadID();
    if (playerID >= 0 && recv.ParseFromString(data))
    {
        COMMAND_PARACHUTE c;
        c.landing_point.x = recv.landing_point().x();
        c.landing_point.y = recv.landing_point().y();
        switch (recv.role())
        {
        case comm_platform::Vocation::MEDIC:
            c.role = VOCATION_TYPE::MEDIC;
            break;
        case comm_platform::Vocation::ENGINEER:
            c.role = VOCATION_TYPE::ENGINEER;
            break;
        case comm_platform::Vocation::SIGNALMAN:
            c.role = VOCATION_TYPE::SIGNALMAN;
            break;
        case comm_platform::Vocation::HACK:
            c.role = VOCATION_TYPE::HACK;
            break;
        case comm_platform::Vocation::SNIPER:
            c.role = VOCATION_TYPE::SNIPER;
            break;
        }
        _command_parachute[playerID].push_back(c);
        return true;
    }
    else
    {
        return false;
    }
}

bool Controller::_parse_commands(const std::string & data)
{
    comm_platform::Command recv;
    auto playerID = _get_playerID_by_threadID();
    if (playerID >= 0 && recv.ParseFromString(data))
    {
        COMMAND_ACTION c;
        switch (recv.command_type())
        {
        case comm_platform::CommandType::MOVE:
            c.command_type = COMMAND_TYPE::MOVE;
            break;
        case comm_platform::CommandType::SHOOT:
            c.command_type = COMMAND_TYPE::SHOOT;
            break;
        case comm_platform::CommandType::PICKUP:
            c.command_type = COMMAND_TYPE::PICKUP;
            break;
        case comm_platform::CommandType::RADIO:
            c.command_type = COMMAND_TYPE::RADIO;
            break;
        }
        c.move_angle = recv.move_angle();
        c.view_angle = recv.view_angle();
        c.target_ID = recv.target_id();
        c.parameter = recv.parameter();

        _command_action[playerID].push_back(c);
        return true;
    }
    else
    {
        return false;
    }
}

void Controller::register_AI(int playerID, AI_Func pfunc, Recv_Func precv)
{
    if (!_check_init())
        return;
    _info[playerID].player_func = pfunc;
    _info[playerID].recv_func = precv;
}

int Controller::_get_playerID_by_threadID()
{
    if (!_check_init())
        return -1;
    auto threadID = GetCurrentThreadId();
    for (int i = _now_offset; i < _now_offset + static_cast<int>(_used_core_count) && i < _player_count; i++)
    {
        if (_info[i].threadID == threadID)
        {
            return i;
        }
    }
    for (int i = 0; i < _player_count; i++)
    {
        if (_info[i].threadID == threadID)
        {
            return i;
        }
    }
    return -1;
}

Controller::Controller()
{
}

DWORD WINAPI thread_func(LPVOID lpParameter)
{
    auto playerID = manager._get_playerID_by_threadID();
    if (manager._info[playerID].player_func != nullptr)
    {
        (*manager._info[playerID].player_func)();
    }
    return 0;
}

bool controller_receive(bool is_jumping, const std::string data)
{
    return manager.receive(is_jumping, data);
}

std::map<int, COMMAND_PARACHUTE> Controller::get_parachute_commands()
{
    std::map<int, COMMAND_PARACHUTE> m;
    if (!_check_init())
        return m;
    for (int i = 0; i < _player_count; i++)
    {
        if (!_command_parachute[i].empty())
        {
            m[i] = _command_parachute[i].back();
        }
    }
    return m;
}

std::string Controller::_serialize_route()
{
    comm_platform::Route sender;
    sender.mutable_start_pos()->set_x(route.first.x);
    sender.mutable_start_pos()->set_y(route.first.y);
    sender.mutable_over_pos()->set_x(route.second.x);
    sender.mutable_over_pos()->set_y(route.second.y);
    return sender.SerializeAsString();
}