#include "controller.h"

extern std::pair<Position, Position> route;

Controller Controller::_instance;

void notify_child_finish(int, siginfo_t *info, void *)
{
    pid_t sender = info->si_pid;
    manager.notify_one_finish(sender);
}

Controller::~Controller()
{
    if (!_check_init())
        return;
    for (int i = 0; i < _player_count; i++)
    {
        if (_info[i].state != AI_STATE::UNUSED)
        {
            kill(_info[i].pid, SIGKILL);
            close(_info[i].sender[1]);
            close(_info[i].receiver[0]);
        }
    }
}

bool Controller::_check_init()
{
    if (!_is_init)
    {
        std::cerr << "Manager is not initialised,please check codes." << std::endl;
    }
    return _is_init;
}

void Controller::init(int playerCount, long used_core_count)
{
    _player_count = playerCount;
    _used_core_count = used_core_count;
    //set CPU
    _total_core_count = sysconf(_SC_NPROCESSORS_ONLN);
    if (used_core_count == 0 || used_core_count > _total_core_count)
    {
        _used_core_count = _total_core_count;
    }
    else
    {
        _used_core_count = used_core_count;
    }
    _is_init = true;
}

Controller::Controller()
{
    //set SIGUSR1
    struct sigaction act;
    act.sa_sigaction = notify_child_finish;
    act.sa_flags = SA_SIGINFO;
    sigemptyset(&act.sa_mask);
    sigaction(SIGUSR1, &act, nullptr);
}

void Controller::run()
{
    if (!_check_init())
        return;
    for (int offset = 0; offset < _player_count; offset += _used_core_count)
    {
        _now_offset = offset;
        //execute some players each loop. The number is equal to the number of core(_used_core_count)
        for (int i = 0; i < _used_core_count && offset + i < _player_count; i++)
        {
            switch (_info[offset + i].state)
            {
            case AI_STATE::UNUSED: //only first time
                _used_cpuID = _total_core_count - _used_core_count + i;
                if (pipe(_info[offset + i].sender) == -1 || pipe(_info[offset + i].receiver) == -1)
                {
                    std::cerr << "cannot create pipe";
                    std::cin.get();
                    std::cin.get();
                    exit(1);
                }
                else
                {
                    fcntl(_info[offset + i].receiver[0], F_SETFL, O_NONBLOCK);
                }
                _info[offset + i].pid = fork();
                if (_info[offset + i].pid > 0) //manager
                {
                    _info[offset + i].state = AI_STATE::ACTIVE;
                    close(_info[offset + i].sender[0]);
                    close(_info[offset + i].receiver[1]);
                    _send_for_server(offset + i, _serialize_route());
                }
                else if (_info[offset + i].pid == 0) //player AI
                {
                    _playerID = offset + i;
                    close(_info[offset + i].sender[1]);
                    close(_info[offset + i].receiver[0]);
                    _run_player();
                    return;
                }
                else //error
                {
                    std::cerr << "Controller error" << std::endl;
                    std::cin.get();
                    std::cin.get();
                    exit(1);
                }
                break;
            case AI_STATE::SUSPENDED:
                kill(_info[offset + i].pid, SIGCONT);
                // write(_info[offset + i].sender[1], pState, sizeof(CState));
                _info[offset + i].state = AI_STATE::ACTIVE;
                break;
            default:
                std::cerr << "process state error" << std::endl;
                std::cin.get();
                std::cin.get();
                exit(1);
                break;
            }
        }
        //std::this_thread::sleep_for(std::chrono::milliseconds(TIMEOUT));
        for (int i = 0; i < _used_core_count && offset + i < _player_count; i++)
        {

            while (_info[offset + i].state == AI_STATE::ACTIVE)
            {
                sleep(10);
                // kill(_info[offset + i].pid, SIGSTOP);
                // _info[offset + i].state = AI_STATE::SUSPENDED;
            }
        }
        for (int i = 0; i < _used_core_count && offset + i < _player_count; i++)
        {
            _receive_for_server(offset + i);
            ++_info[offset + i].turn;
        }
    }
}
void Controller::_run_player()
{
    if (!_check_init())
        return;
    //set CPU affinity
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(_used_cpuID, &cpuset);
    sched_setaffinity(0, sizeof(cpuset), &cpuset);
    //player AI
    while (true)
    {
        _send_for_client();
        if (_playerID >= 0 && _info[_playerID].player_func != nullptr)
        {
            (*_info[_playerID].player_func)();
        }
        kill(getppid(), SIGUSR1);
        raise(SIGSTOP);
    }
}

void Controller::notify_one_finish(pid_t pid)
{
    if (!_check_init())
        return;
    for (int i = _now_offset; i < _now_offset + _used_core_count && i < _player_count; i++)
    {
        if (_info[i].pid == pid)
        {
            _info[i].state = AI_STATE::SUSPENDED;
            return;
        }
    }
    for (int i = 0; i < _player_count; i++)
    {
        if (_info[i].pid == pid)
        {
            _info[i].state = AI_STATE::SUSPENDED;
            return;
        }
    }
}

void Controller::register_AI(int playerID, AI_Func pfunc, Recv_Func precv)
{
    if (!_check_init())
        return;
    _info[playerID].player_func = pfunc;
    _info[playerID].recv_func = precv;
}

bool Controller::receive_for_client(bool is_jumping, const std::string &data)
{
    if (!_check_init())
        return false;
    if (is_jumping && _info[_playerID].turn != 0)
    {
        return false;
    }
    else if (is_jumping)
    {
        ++_info[_playerID].turn;
    }
    //send data to server
    int size = data.size();
    char *buffer = new char[size];
    memcpy(buffer, data.data(), size);
    if (write(_info[_playerID].receiver[1], &size, sizeof(size)) != sizeof(size))
    {
        delete[] buffer;
        return false;
    }
    if (write(_info[_playerID].receiver[1], buffer, sizeof(char) * size) != sizeof(char) * size)
    {
        delete[] buffer;
        return false;
    }
    delete[] buffer;
    return true;
}

void Controller::_receive_for_server(int playerID)
{
    int size = 0;
    int recv_size;
    do
    {
        recv_size = read(_info[playerID].receiver[0], &size, sizeof(size));
        if (recv_size <= 0)
            break;
        char *buffer = new char[size];
        //assume that it always read completely.
        recv_size = read(_info[playerID].receiver[0], buffer, sizeof(char) * size);
        if (recv_size <= 0)
        {
            delete[] buffer;
            break;
        }
        std::string s;
        s.append(buffer, size);
        if (_info[playerID].turn == 0)
        {
            _parse_parachute(s, playerID);
        }
        else
        {
            _parse_commands(s, playerID);
        }
        delete[] buffer;
    } while (recv_size > 0);
}

void Controller::_send_for_server(int playerID, const std::string &data)
{
    if (!_check_init())
        return;
    //send data to server
    int size = data.size();
    char *buffer = new char[size];
    memcpy(buffer, data.data(), size);
    if (write(_info[playerID].sender[1], &size, sizeof(size)) != sizeof(size))
    {
        delete[] buffer;
        return;
    }
    if (write(_info[playerID].sender[1], buffer, sizeof(char) * size) != sizeof(char) * size)
    {
        delete[] buffer;
        return;
    }
    delete[] buffer;
    return;
}

void Controller::_send_for_client()
{
    int size = 0;
    int recv_size;
    recv_size = read(_info[_playerID].sender[0], &size, sizeof(size));
    if (recv_size <= 0)
        return;
    char *buffer = new char[size];
    //assume that it always read completely.
    recv_size = read(_info[_playerID].sender[0], buffer, sizeof(char) * size);
    if (recv_size <= 0)
    {
        delete[] buffer;
        return;
    }
    std::string s;
    s.append(buffer, size);
    (*_info[_playerID].recv_func)(_info[_playerID].turn == 0, s);
    delete[] buffer;
}

bool Controller::_parse_parachute(const std::string &data, int playerID)
{
    comm_platform::Parachute recv;
    if (playerID >= 0 && recv.ParseFromString(data))
    {
        std::cout << recv.DebugString() << std::endl;
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

bool Controller::_parse_commands(const std::string &data, int playerID)
{
    comm_platform::Command recv;
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

std::string Controller::_serialize_route()
{
    comm_platform::Route sender;
    sender.mutable_start_pos()->set_x(route.first.x);
    sender.mutable_start_pos()->set_y(route.first.y);
    sender.mutable_over_pos()->set_x(route.second.x);
    sender.mutable_over_pos()->set_y(route.second.y);
    return sender.SerializeAsString();
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

bool controller_receive(bool is_jumping, const std::string data)
{
    std::cout << "client recvive" << data << std::endl;
    return manager.receive_for_client(is_jumping, data);
}
