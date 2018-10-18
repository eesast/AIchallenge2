#include "controller.h"

Controller Controller::_instance;

void notify_child_finish(int, siginfo_t *info, void *)
{
    pid_t sender = info->si_pid;
    manager.notify_one_finish(sender);
}

Controller::~Controller()
{
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
    for (int i = 0; i < MAX_PLAYER; i++)
    {
        _player_func[i] = nullptr;
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
    if(!_is_init)
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
                    close(_info[offset + i].sender[0]);
                    close(_info[offset + i].receiver[1]);
                    // write(_info[offset + i].sender[1], pState, sizeof(CState));
                    _info[offset + i].state = AI_STATE::ACTIVE;
                }
                else if (_info[offset + i].pid == 0) //player AI
                {
                    _playerID = offset + i;
                    close(_info[offset + i].sender[1]);
                    close(_info[offset + i].receiver[0]);
                    run_player();
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
        std::this_thread::sleep_for(std::chrono::milliseconds(TIMEOUT));
        for (int i = 0; i < _used_core_count && offset + i < _player_count; i++)
        {
            if (_info[offset + i].state == AI_STATE::ACTIVE)
            {
                kill(_info[offset + i].pid, SIGSTOP);
                _info[offset + i].state = AI_STATE::SUSPENDED;
            }
        }
        for (int i = 0; i < _used_core_count && offset + i < _player_count; i++)
        {
            // DEMAND d;
            // while (read(_info[offset + i].receiver[0], &d, sizeof(d)) > 0)
            // {
            //     std::cout << "id" << offset + i << "cd:" << d.cd << "order:" << d.order << std::endl;
            //     pAllDemands[offset + i].push_back(d);
            // }
        }
    }
}
void Controller::run_player()
{
    if (!_is_init)
        return;
    //set CPU affinity
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(_used_cpuID, &cpuset);
    sched_setaffinity(0, sizeof(cpuset), &cpuset);
    //player AI
    while (true)
    {
        //receive data from server
        // read(_info[_playerID].sender[0], pState, sizeof(CState));
        //not send demands because of laziness
        // std::cout << "get state" << pState->GetTurn() << ' ' << pState->GetTest() << std::endl;
        if (_player_func[_playerID] != nullptr)
        {
            (*_player_func[_playerID])();
        }
        kill(getppid(), SIGUSR1);
        raise(SIGSTOP);
    }
}

void Controller::notify_one_finish(pid_t pid)
{
    if (!_is_init)
        return;
    for (int i = _now_offset; i < _now_offset + _used_core_count && i < _player_count; i++)
    {
        if (_info[i].pid == pid)
        {
            _info[i].state = AI_STATE::SUSPENDED;
            break;
        }
    }
}

void Controller::send_demand()
{
    if (!_is_init)
        return;
    // write(_info[_playerID].receiver[1], &d, sizeof(d));
}

void Controller::register_AI(int playerID, AI_Func pfunc)
{
    if (!_is_init)
        return;
    _player_func[playerID] = pfunc;
}