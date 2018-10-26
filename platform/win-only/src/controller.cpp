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
    for (int i = 0; i < MAX_PLAYER; i++)
    {
        _player_func[i] = nullptr;
        _recv_func[i] = nullptr;
    }
    _is_init = true;
}

Controller::~Controller()
{
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
    if (!_is_init)
        return;
    for (int offset = 0; offset < _player_count; offset += _used_core_count)
    {
        _now_offset = offset;
        //execute some players each loop. The number is equal to the number of core(_used_core_count) 
        for (int i = 0; i < static_cast<int>(_used_core_count) && offset + i < _player_count; i++)
        {
            //clear commands vector
            _commands[offset + i].clear();
            //offset + i == playerID
            if (_info[offset + i].state == AI_STATE::UNUSED)
            {
                _info[offset + i].handle = CreateThread(nullptr, 0, thread_func, nullptr, CREATE_SUSPENDED, &_info[offset + i].threadID);
                if (_info[offset + i].handle == NULL)
                {
                    DWORD errorCode = GetLastError();
                    std::cerr << "Cannot create thread. Error Code: " << errorCode << std::endl;
                    system("pause");
                    exit(1);
                }
                _info[offset + i].mtx.lock();
                _info[offset + i].state = AI_STATE::SUSPENDED;
                //CPU control, choose the core which the thread uses. When the used core number is less than that CPU actually has, using core with higher ID firstly 
                SetThreadAffinityMask(_info[offset + i].handle, (static_cast<DWORD_PTR>(1) << ((_total_core_count - _used_core_count) + i)));
            }
            _waiting_thread[i] = _info[offset + i].handle;    //if the player's thread is suspended, just resume it
        }
        for (int i = 0; i < static_cast<int>(_used_core_count) && offset + i < _player_count; i++)
        {
            _info[offset + i].mtx.unlock();
            _info[offset + i].state = AI_STATE::ACTIVE;
            (*_recv_func[offset + i])(true, 2, route.first, route.second);
            ResumeThread(_info[offset + i].handle);
        }
        DWORD threadNumber = (_player_count - offset >= static_cast<int>(_used_core_count) ? _used_core_count : static_cast<DWORD>(_player_count - offset));
        if (WaitForMultipleObjects(threadNumber, _waiting_thread, true, TIMEOUT) == WAIT_TIMEOUT)
        {    //if one thread does not exit 
            DWORD exitCode;
            for (int i = 0; i < static_cast<int>(_used_core_count) && offset + i < _player_count; i++)
            {    //look out still active thread and suspend it forcefully
                GetExitCodeThread(_info[offset + i].handle, &exitCode);
                if (exitCode == STILL_ACTIVE)
                {
                    _info[offset + i].mtx.lock();
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

void Controller::parachute(VOCATION_TYPE role[4], Position landing_points[4])
{
    if (!_is_init)
        return;
    auto playerID = get_playerID_by_thread();
    COMMAND_PARACHUTE c;
    for (int i = 0; i < MEMBER_COUNT; i++)
    {
        c.role[i] = role[i];
        c.landing_points[i] = landing_points[i];
    }
    _commands[playerID].push_back(c);
    return;
}


void Controller::register_AI(int playerID, AI_Func pfunc,Recv_Func precv)
{
    if (!_is_init)
        return;
    _player_func[playerID] = pfunc;
    _recv_func[playerID] = precv;
}

int Controller::get_playerID_by_thread()
{
    if (!_is_init)
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
    auto playerID = manager.get_playerID_by_thread();
    if (manager._player_func[playerID] != nullptr)
    {
        (*manager._player_func[playerID])();
    }
    return 0;
}

std::map<int,COMMAND_PARACHUTE> Controller::get_parachute_commands()
{
    std::map<int, COMMAND_PARACHUTE> c;
    for (int i = 0; i < MAX_PLAYER; i++)
    {
        if (!_commands[i].empty())
        {
            c[i] = _commands[i].front();
        }
    }
    return c;
}
