#include "controller.h"

Controller Controller::_instance;

void Controller::init(const std::string &path, DWORD used_core_count)
{
    using namespace std::filesystem;
    auto PAT = std::regex(R"((AI_(\d*)_(\d*)).dll)", std::regex_constants::ECMAScript | std::regex_constants::icase);
    std::smatch m;
    int player_count = 0;
    for (const auto &entry : directory_iterator(path))
    {
        if (entry.is_regular_file())
        {
            auto name = entry.path().filename().string();
            if (std::regex_match(name, m, PAT) && m.size() == 4)
            {
                int team = atoi(m[2].str().c_str());
                int number = atoi(m[3].str().c_str());
                if (0 <= team && team <= 15 && 0 <= number && number <= 3)
                {
                    _info[player_count].team = team;
                    std::string fullpath = entry.path().root_directory().string() + m[1].str();
                    _info[player_count].lib = LoadLibrary(fullpath.c_str());
                    if (_info[player_count].lib == NULL)
                    {
                        std::cerr << "LoadLibrary " + fullpath + " error:" << GetLastError() << std::endl;
                        continue;
                    }
                    else
                    {
                        auto bind_api = (void(*)(Player_Send_Func))GetProcAddress(_info[player_count].lib, "bind_api");
                        _info[player_count].player_func = (AI_Func)GetProcAddress(_info[player_count].lib, "play_game");
                        _info[player_count].recv_func = (Recv_Func)GetProcAddress(_info[player_count].lib, "player_receive");
                        if (bind_api == NULL || _info[player_count].player_func == NULL || _info[player_count].recv_func == NULL)
                        {
                            std::cerr << "Cannot Get AI API from " << _info[player_count].lib << " Error Code:" << GetLastError() << std::endl;
                            continue;
                        }
                        else
                        {
                            (*bind_api)(&controller_receive);
                            ++player_count;
                            std::cout << "Load AI " << fullpath << " as team" << team << std::endl;
                        }
                    }
                }
                else
                {
                    std::cerr << "Wrong filename:" << m[0] << std::endl;
                }
            }
        }
    }
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
            FreeLibrary(_info[i].lib);
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
            _command_action[offset + i].clear();
            //offset + i == playerID
            if (_info[offset + i].state == AI_STATE::UNUSED)
            {
                //create or recreate a subthread.
                _info[offset + i].handle = CreateThread(nullptr, 0, thread_func, nullptr, CREATE_SUSPENDED, &_info[offset + i].threadID);
                if (_info[offset + i].handle == NULL)
                {
                    std::cerr << "Cannot create thread. Error Code: " << GetLastError() << std::endl;
                    system("pause");
                    exit(1);
                }
                _info[offset + i].state = AI_STATE::SUSPENDED;
                //CPU control, choose the core which the thread uses. When the used core number is less than that CPU actually has, using core with higher ID firstly 
                if (SetThreadAffinityMask(_info[offset + i].handle, (static_cast<DWORD_PTR>(1) << ((_total_core_count - _used_core_count) + i))))
                {
                }
                else
                {
                    std::cerr << "CPU core setting fails. Error Code: " << GetLastError() << std::endl;
                }
            }
            _waiting_thread[i] = _info[offset + i].handle;    //if the player's thread is suspended, just resume it
        }
        //send route and start subthread.
        for (int i = 0; i < static_cast<int>(_used_core_count) && offset + i < _player_count; i++)
        {
            _info[offset + i].state = AI_STATE::ACTIVE;
            (*_info[offset + i].recv_func)(true, _serialize_route());
            if (ResumeThread(_info[offset + i].handle) == 0xFFFFFFFF)
            {
                std::cerr << "Cannot resume Thread" << _info[offset + i].threadID << " Error Code: " << GetLastError() << std::endl;
            }
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
                    if (SuspendThread(_info[offset + i].handle) == 0xFFFFFFFF)
                    {
                        std::cerr << "Cannot suspend Thread" << _info[offset + i].threadID << " Error Code: " << GetLastError() << std::endl;
                    }
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

bool Controller::receive(const std::string & data)
{
    if (!_check_init())
        return false;
    std::cout << "receive" << std::endl;
    return _parse(data);

}

void Controller::_send(int playerID, bool is_jumping, const std::string & data)
{
    if (!_check_init())
        return;
    _info[playerID].recv_func(is_jumping, data);
    return;
}

bool Controller::_parse(const std::string & data)
{
    comm::Command recv;
    auto playerID = _get_playerID_by_threadID();
    if (playerID >= 0 && recv.ParseFromString(data))
    {
        if (recv.command_type() != comm::CommandType::PARACHUTE)
        {
            COMMAND_ACTION c;
            switch (recv.command_type())
            {
            case comm::CommandType::MOVE:
                c.command_type = COMMAND_TYPE::MOVE;
                break;
            case comm::CommandType::SHOOT:
                c.command_type = COMMAND_TYPE::SHOOT;
                break;
            case comm::CommandType::PICKUP:
                c.command_type = COMMAND_TYPE::PICKUP;
                break;
            case comm::CommandType::RADIO:
                c.command_type = COMMAND_TYPE::RADIO;
                break;
            default:
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
            COMMAND_PARACHUTE c;
            c.landing_point.x = recv.landing_point().x();
            c.landing_point.y = recv.landing_point().y();
            c.role = static_cast<VOCATION>(recv.role());
            c.team = _info[playerID].team;
            _command_parachute[playerID].push_back(c);
            return true;
        }
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

bool controller_receive(bool unused, const std::string data)
{
    return manager.receive(data);
}

std::map<int, COMMAND_PARACHUTE> Controller::get_parachute_commands()
{
    std::map<int, COMMAND_PARACHUTE> m;
    if (!_check_init())
        return m;
    for (int i = 0; i < _player_count; ++i)
    {
        if (!_command_parachute[i].empty())
        {
            m[i] = _command_parachute[i].back();
        }
    }
    return m;
}

std::map<int, std::vector<COMMAND_ACTION>> Controller::get_action_commands()
{
    std::map<int, std::vector<COMMAND_ACTION>> m;
    if (!_check_init())
        return m;
    for (int i = 0; i < _player_count; ++i)
    {
        if (!_command_action[i].empty())
        {
            m[i] = { _command_action[i].cbegin(),_command_action[i].cend() };
        }
    }
    return m;
}

std::string Controller::_serialize_route()
{
    comm::Route sender;
    sender.mutable_start_pos()->set_x(route.first.x);
    sender.mutable_start_pos()->set_y(route.first.y);
    sender.mutable_over_pos()->set_x(route.second.x);
    sender.mutable_over_pos()->set_y(route.second.y);
    return sender.SerializeAsString();
}