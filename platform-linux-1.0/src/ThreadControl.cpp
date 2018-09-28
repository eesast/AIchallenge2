#include "ThreadControl.h"

CPlayerID::CPlayerID(unsigned int playerID) noexcept : m_playerID(playerID)
{
}

CPlayerID::~CPlayerID()
{
}

unsigned int CPlayerID::GetID() const
{
    return m_playerID;
}
ThreadControl::~ThreadControl()
{
    for (int i = 0; i < m_playerCount; i++)
    {
        if (m_processInfo[i].state != PROCESS_UNUSED)
        {
            kill(m_processInfo[i].pid, SIGKILL);
            close(m_processInfo[i].sender[1]);
            close(m_processInfo[i].receiver[0]);
        }
    }
}

ThreadControl::ThreadControl(int playerCount, CState &state, std::vector<DEMAND> allDemands[], long usedCoreNumber) : m_playerCount(playerCount), m_usedCoreNumber(usedCoreNumber), pState(&state), pAllDemands(allDemands)
{
    m_totalCoreNumber = sysconf(_SC_NPROCESSORS_ONLN);
    if (usedCoreNumber == 0 || usedCoreNumber > m_totalCoreNumber)
    {
        m_usedCoreNumber = m_totalCoreNumber;
    }
    else
    {
        m_usedCoreNumber = usedCoreNumber;
    }
    for (int i = 0; i < MAX_PLAYER; i++)
    {
        playerFunc[i] = nullptr;
    }
}

void ThreadControl::Run()
{
    for (int offset = 0; offset < m_playerCount; offset += m_usedCoreNumber)
    {
        m_nowOffset = offset;
        //execute some players each loop. The number is equal to the number of core(m_usedCoreNumber)
        for (int i = 0; i < m_usedCoreNumber && offset + i < m_playerCount; i++)
        {
            switch (m_processInfo[offset + i].state)
            {
            case PROCESS_UNUSED: //only first time
                m_usedCpuID = m_totalCoreNumber - m_usedCoreNumber + i;
                if (pipe(m_processInfo[offset + i].sender) == -1 || pipe(m_processInfo[offset + i].receiver) == -1)
                {
                    std::cerr << "cannot create pipe";
                    std::cin.get();
                    std::cin.get();
                    exit(1);
                }
                else
                {
                    fcntl(m_processInfo[offset + i].receiver[0], F_SETFL, O_NONBLOCK);
                }
                m_processInfo[offset + i].pid = fork();
                if (m_processInfo[offset + i].pid > 0) //manager
                {
                    close(m_processInfo[offset + i].sender[0]);
                    close(m_processInfo[offset + i].receiver[1]);
                    write(m_processInfo[offset + i].sender[1], pState, sizeof(CState));
                    m_processInfo[offset + i].state = PROCESS_ACTIVE;
                }
                else if (m_processInfo[offset + i].pid == 0) //player AI
                {
                    m_playerID = offset + i;
                    close(m_processInfo[offset + i].sender[1]);
                    close(m_processInfo[offset + i].receiver[0]);
                    RunPlayer();
                    return;
                }
                else //error
                {
                    std::cerr << "multiprocess error" << std::endl;
                    std::cin.get();
                    std::cin.get();
                    exit(1);
                }
                break;
            case PROCESS_SUSPENDED:
                kill(m_processInfo[offset + i].pid, SIGCONT);
                write(m_processInfo[offset + i].sender[1], pState, sizeof(CState));
                m_processInfo[offset + i].state = PROCESS_ACTIVE;
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
        for (int i = 0; i < m_usedCoreNumber && offset + i < m_playerCount; i++)
        {
            if (m_processInfo[offset + i].state == PROCESS_ACTIVE)
            {
                kill(m_processInfo[offset + i].pid, SIGSTOP);
                m_processInfo[offset + i].state = PROCESS_SUSPENDED;
            }
        }
        for (int i = 0; i < m_usedCoreNumber && offset + i < m_playerCount; i++)
        {
            DEMAND d;
            while (read(m_processInfo[offset + i].receiver[0], &d, sizeof(d)) > 0)
            {
                std::cout << "id" << offset + i << "cd:" << d.cd << "order:" << d.order << std::endl;
                pAllDemands[offset + i].push_back(d);
            }
        }
    }
}
void ThreadControl::RunPlayer()
{
    //set CPU affinity
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(m_usedCpuID, &cpuset);
    sched_setaffinity(0, sizeof(cpuset), &cpuset);
    //player AI
    while (true)
    {
        //receive data from server
        read(m_processInfo[m_playerID].sender[0], pState, sizeof(CState));
        //not send demands because of laziness
        std::cout << "get state" << pState->GetTurn() << ' ' << pState->GetTest() << std::endl;
        if (playerFunc[m_playerID] != nullptr)
        {
            (*playerFunc[m_playerID])();
        }
        kill(getppid(), SIGUSR1);
        raise(SIGSTOP);
    }
}

void ThreadControl::NotifyOneFinish(pid_t pid)
{

    for (int i = m_nowOffset; i < m_nowOffset + m_usedCoreNumber && i < m_playerCount; i++)
    {
        if (m_processInfo[i].pid == pid)
        {
            m_processInfo[i].state = PROCESS_SUSPENDED;
            break;
        }
    }
}

void ThreadControl::SendDemand(DEMAND d)
{
    write(m_processInfo[m_playerID].receiver[1], &d, sizeof(d));
}

void ThreadControl::Register(int playerID, aiFunc pfunc)
{
    playerFunc[playerID] = pfunc;
}