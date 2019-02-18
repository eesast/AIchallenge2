#include "controller.h"

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
            dlclose(_info[i].lib);
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

void Controller::init(const std::string &path, long used_core_count)
{
    using namespace std::filesystem;
    auto PAT = std::regex(R"((libAI_(\d*)_(\d*)).so)", std::regex_constants::ECMAScript | std::regex_constants::icase);
    std::smatch m;
    int player_count = 0;
    for (const auto &entry : directory_iterator(path))
    {

        if (is_regular_file(entry))
        {
            auto name = entry.path().filename().string();
            if (std::regex_match(name, m, PAT) && m.size() == 4)
            {
                int team = atoi(m[2].str().c_str());
                int number = atoi(m[3].str().c_str());
                if (0 <= team && team <= 15 && 0 <= number && number <= 3)
                {
                    _info[player_count].team = team;
                    std::string fullpath = entry.path();
                    std::cerr << "try to load " << fullpath << std::endl;
                    _info[player_count].lib = dlopen(fullpath.c_str(), RTLD_NOW);
                    if (_info[player_count].lib == NULL)
                    {
                        std::cerr << "LoadLibrary " + fullpath + " error" << std::endl;
                        continue;
                    }
                    else
                    {
                        auto bind_api = (void (*)(Player_Send_Func))dlsym(_info[player_count].lib, "bind_api");
                        _info[player_count].player_func = (AI_Func)dlsym(_info[player_count].lib, "play_game");
                        _info[player_count].recv_func = (Recv_Func)dlsym(_info[player_count].lib, "player_receive");
                        if (bind_api == NULL || _info[player_count].player_func == NULL || _info[player_count].recv_func == NULL)
                        {
                            std::cerr << "Cannot Get AI API from " << std::endl;
                            continue;
                        }
                        else
                        {
                            (*bind_api)(&controller_receive);
                            _team[team].push_back(player_count);
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
                    _send_to_client(offset + i, _serialize_route(offset + i));
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
            ++_info[offset + i].frame;
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
    if (is_jumping && _info[_playerID].frame != 0)
    {
        return false;
    }
    else if (is_jumping)
    {
        ++_info[_playerID].frame;
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
    for (auto &s : all)
    {
        _parse(s, playerID);
    }
}

void Controller::_send_to_client(int playerID, const std::string &data)
{
    if (!_check_init())
        return;
    //send data to server
    _info[playerID].shm->lock_infos();
    _info[playerID].shm->set_infos(data);
    _info[playerID].shm->frame = _info[playerID].frame;
    _info[playerID].shm->unlock_infos();
    return;
}

void Controller::_receive_from_server()
{
    _info[_playerID].frame = _info[_playerID].shm->frame;
    (*_info[_playerID].recv_func)(_info[_playerID].frame == 0, _info[_playerID].shm->get_infos());
}

bool Controller::_parse(const std::string &data, int playerID)
{
    comm::Command recv;
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
            std::cout << recv.DebugString() << std::endl;
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

std::string Controller::_serialize_route(int playerID)
{
    comm::Route sender;
    sender.mutable_start_pos()->set_x(route.first.x);
    sender.mutable_start_pos()->set_y(route.first.y);
    sender.mutable_over_pos()->set_x(route.second.x);
    sender.mutable_over_pos()->set_y(route.second.y);
    for (auto teammate : _team[_info[playerID].team])
    {
        sender.add_teammates(teammate);
    }
    return sender.SerializeAsString();
}

std::string Controller::_serialize_infos(int playerID)
{
    comm::PlayerInfo sender;
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

std::map<int, std::vector<COMMAND_ACTION>> Controller::get_action_commands()
{
    std::map<int, std::vector<COMMAND_ACTION>> m;
    if (!_check_init())
        return m;
    for (int i = 0; i < _player_count; ++i)
    {
        if (!_command_action[i].empty())
        {
            m[i] = {_command_action[i].cbegin(), _command_action[i].cend()};
        }
    }
    return m;
}

bool controller_receive(bool is_jumping, const std::string data)
{
    std::cout << "client receive" << data << std::endl;
    return manager.send_to_server(is_jumping, data);
}
