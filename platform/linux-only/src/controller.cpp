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
            shmdt(_info[i].shm);
            shmctl(_info[i].shmid, IPC_RMID, nullptr);
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
            std::cout << "enter run" << std::endl;
            _command_action[offset + i].clear();
            _command_parachute[offset + i].clear();
            switch (_info[offset + i].state)
            {
            case AI_STATE::UNUSED: //only first time
                _used_cpuID = _total_core_count - _used_core_count + i;
                _info[offset + i].shmid = shmget(IPC_PRIVATE, sizeof(COMM_BLOCK), IPC_CREAT | 0600);
                _info[offset + i].pid = fork();
                if (_info[offset + i].pid > 0) //manager
                {
                    std::cout << "manager report" << std::endl;
                    _info[offset + i].state = AI_STATE::ACTIVE;
                    _info[offset + i].shm = reinterpret_cast<COMM_BLOCK *>(shmat(_info[offset + i].shmid, nullptr, 0));
                    _info[offset + i].shm->init();
                    std::cout << "start send" << std::endl;
                    _send_to_client(offset + i, _serialize_route());
                    _info[offset + i].shm->set_inited();
                }
                else if (_info[offset + i].pid == 0) //player AI
                {
                    std::cout << "client report" << std::endl;
                    _playerID = offset + i;
                    _info[offset + i].shm = reinterpret_cast<COMM_BLOCK *>(shmat(_info[offset + i].shmid, nullptr, 0));
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
                _send_to_client(offset + i, _serialize_infos(offset + i));
                _send_to_client(offset + i, _serialize_route());

                kill(_info[offset + i].pid, SIGCONT);
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
        std::cout << "enter waiting" << std::endl;

        bool all_finish = true;
        timeval start, now;
        gettimeofday(&start, nullptr);
        do
        {
            std::this_thread::sleep_for(std::chrono::milliseconds(CHECK_INTERVAL));
            gettimeofday(&now, nullptr);
            if (now.tv_sec > start.tv_sec || now.tv_usec - start.tv_usec > 1000 * TIMEOUT)
            {
                std::cout << "TIMEOUT LOOP!!!!!" << std::endl;
                break;
            }
            all_finish = true;
            for (int i = 0; i < _used_core_count && offset + i < _player_count; ++i)
            {
                if (_info[offset + i].state == AI_STATE::ACTIVE)
                {
                    all_finish = false;
                    break;
                }
            }
        } while (!all_finish);
        std::cout << "TIMEOUT!!!!!\n";
        if (!all_finish)
        {
            for (int i = 0; i < _used_core_count && offset + i < _player_count; ++i)
            {
                if (_info[offset + i].state == AI_STATE::ACTIVE)
                {
                    //get all locks before stopping clients, avoid deadlocks(if the client has locked it but stopped)
                    _info[offset + i].shm->lock_commands();
                    _info[offset + i].shm->lock_infos();
                    kill(_info[offset + i].pid, SIGSTOP);
                    _info[offset + i].state = AI_STATE::SUSPENDED;
                    _info[offset + i].shm->unlock_infos();
                    _info[offset + i].shm->unlock_commands();
                }
            }
        }
        for (int i = 0; i < _used_core_count && offset + i < _player_count; i++)
        {
            _info[offset + i].shm->lock_commands();
            _receive_from_client(offset + i);
            _info[offset + i].shm->clear_commands();
            _info[offset + i].shm->unlock_commands();
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
    while (!_info[_playerID].shm->is_init)
        ;
    //player AI
    while (true)
    {
        _info[_playerID].shm->lock_infos();
        _receive_from_server();
        _info[_playerID].shm->unlock_infos();
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

bool Controller::send_to_server(bool is_jumping, const std::string &data)
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
    _info[_playerID].shm->lock_commands();
    _info[_playerID].shm->add_command(data);
    _info[_playerID].shm->unlock_commands();
    return true;
}

void Controller::_receive_from_client(int playerID)
{
    if (!_check_init())
        return;
    auto all = _info[playerID].shm->get_commands();
    if (_info[playerID].turn == 0)
    {
        for (auto &s : all)
        {
            _parse_parachute(s, playerID);
        }
    }
    else
    {
        for (auto &s : all)
        {
            _parse_commands(s, playerID);
        }
    }
}

void Controller::_send_to_client(int playerID, const std::string &data)
{
    if (!_check_init())
        return;
    //send data to server
    _info[playerID].shm->lock_infos();
    _info[playerID].shm->set_infos(data);
    _info[playerID].shm->turn = _info[playerID].turn;
    _info[playerID].shm->unlock_infos();
    return;
}

void Controller::_receive_from_server()
{
    _info[_playerID].turn = _info[_playerID].shm->turn;
    (*_info[_playerID].recv_func)(_info[_playerID].turn == 0, _info[_playerID].shm->get_infos());
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

std::string Controller::_serialize_infos(int playerID)
{
    comm_platform::PlayerInfo sender;
    sender.set_player_id(playerID);
    //........
    //
    //
    // L O G I C
    //
    //
    //.......
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
    std::cout << "client receive" << data << std::endl;
    return manager.send_to_server(is_jumping, data);
}
