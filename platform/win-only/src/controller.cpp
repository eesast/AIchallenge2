#include "controller.h"

extern std::ofstream mylog;

Controller Controller::_instance;

void Controller::init(const std::filesystem::path &path, DWORD used_core_count)
{
	using namespace std::filesystem;
	auto PAT = std::regex(R"((AI_(\d+)_(\d+)).dll)", std::regex_constants::ECMAScript | std::regex_constants::icase);
	std::smatch m;
	int player_count = 0;
	_frame = 0;
	for (const auto &entry : directory_iterator(path))
	{
		if (entry.is_regular_file())
		{
			auto name = entry.path().filename().string();
			if (std::regex_match(name, m, PAT) && m.size() == 4)
			{
				int team = atoi(m[2].str().c_str());
				int number = atoi(m[3].str().c_str());
				if (0 <= team && team < MAX_TEAM && 0 <= number && number <= MEMBER_COUNT)
				{
					auto fullpath = entry.path().string();
					_info[player_count].team = team;
					_info[player_count].lib = LoadLibrary(fullpath.c_str());
					if (_info[player_count].lib == NULL)
					{
						mylog << "LoadLibrary " + fullpath + " error:" << GetLastError() << std::endl;
						continue;
					}
					else
					{
						auto bind_api = (void(*)(Player_Send_Func, Player_Update))GetProcAddress(_info[player_count].lib, "bind_api");
						_info[player_count].player_func = (AI_Func)GetProcAddress(_info[player_count].lib, "play_game");
						_info[player_count].recv_func = (Recv_Func)GetProcAddress(_info[player_count].lib, "player_receive");
						if (bind_api == NULL || _info[player_count].player_func == NULL || _info[player_count].recv_func == NULL)
						{
							mylog << " Cannot Get AI API from " << _info[player_count].lib << " Error Code:" << GetLastError() << std::endl;
							continue;
						}
						else
						{
							_team[team].push_back(player_count);
							(*bind_api)(&controller_receive, &controller_update);
							++player_count;
							std::cout << "Load AI " << fullpath << " as team" << team << std::endl;
							mylog << "Load AI " << fullpath << " as team" << team << std::endl;
						}
					}
				}
				else
				{
					mylog << "Wrong filename:" << m[0] << std::endl;
				}
			}
		}
	}
	_timer = CreateWaitableTimer(NULL, FALSE, NULL);
	if (_timer == NULL)
	{
		mylog << "CreateWaitableTimer fails" << std::endl;
		std::cout << "CreateWaitableTimer fails" << std::endl;
		system("pause");
		exit(1);
	}
	_player_count = player_count;
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
	for (int i = 0; i < _player_count; i++)
	{
		_info[i].cpuID = i % _used_core_count;
	}
	for (int i = 0; i < _used_core_count; i++)
	{
		_cpu_batchs.emplace_back(std::vector<int>());
	}
	mylog << "total core = " << _total_core_count << " used core = " << _used_core_count << std::endl;
	_is_init = true;
}

bool Controller::_check_init()
{
	if (!_is_init)
	{
		mylog << "Manager is not initialised, please check codes." << std::endl;
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
		FreeLibrary(_info[i].lib);
	}
	CloseHandle(_timer);
}

void Controller::_kill_one(int playerID)
{
	if (_info[playerID].state != AI_STATE::DEAD)
	{
		_info[playerID].state = AI_STATE::DEAD;
		mylog << "kill player: " << playerID << std::endl;
	}
}

bool Controller::has_living_player()
{
	for (int i = 0; i < _player_count; i++)
	{
		if (_info[i].state != AI_STATE::DEAD)
		{
			return true;
		}
	}
	return false;
}

void Controller::run()
{
	if (!_check_init())
		return;
	mylog << "\nrun frame: " << _frame << std::endl;
	for (int playerID : dead)
	{
		_kill_one(playerID);
	}
	//clear something
	for (int i = 0; i < _player_count; ++i)
	{
		_command_parachute[i].clear();
		_command_action[i].clear();
	}
	for (int i = 0; i < _used_core_count; ++i)
	{
		_cpu_batchs[i].clear();
	}
	for (int i = _player_count - 1; i >= 0; --i)
	{
		if (_info[i].state != AI_STATE::DEAD)
		{
			_cpu_batchs[_info[i].cpuID].push_back(i);
		}
	}
	//main_loop
	while (true)
	{
		//set batch
		_batch.clear();
		for (int i = 0; i < _used_core_count; ++i)
		{
			if (!_cpu_batchs[i].empty())
			{
				_batch.push_back(_cpu_batchs[i].back());
				_cpu_batchs[i].pop_back();
			}
		}
		if (_batch.empty())
			break;
		mylog << "batch: ";
		for (const auto i : _batch)
		{
			mylog << i << ' ';
		}
		mylog << std::endl;
		//execute some players each loop. The number is equal to the number of core(_used_core_count) 
		for (int i : _batch)
		{
			//  i == playerID
			if (_info[i].state == AI_STATE::UNUSED)
			{
				//create or recreate a subthread.
				_info[i].handle = CreateThread(nullptr, 0, thread_func, reinterpret_cast<LPVOID>(i), 0, &_info[i].threadID);
				if (_info[i].handle == NULL)
				{
					mylog << "player: " << i << " Cannot create thread. Error Code: " << GetLastError() << std::endl;
					std::cout << "platform error" << std::endl;
					system("pause");
					exit(1);
				}
				_info[i].state = AI_STATE::SUSPENDED;
				//CPU control, choose the core which the thread uses. When the used core number is less than that CPU actually has, using core with higher ID firstly 
				if (!SetThreadAffinityMask(_info[i].handle, (static_cast<DWORD_PTR>(1) << (_info[i].cpuID + _total_core_count - _used_core_count))))
				{
					mylog << "player: " << i << " CPU core setting fails. Error Code: " << GetLastError() << std::endl;
				}
			}
		}
		//send route
		for (int i : _batch)
		{
			if (_frame > 0)
			{
				_send(i, _frame, _serialize_info(i));
			}
			else
			{
				_send(i, _frame, _serialize_route(i));
			}
			if (ResumeThread(_info[i].handle) == 0xFFFFFFFF)
			{
				mylog << "player: " << i << " Cannot resume Thread" << _info[i].threadID << " Error Code: " << GetLastError() << std::endl;
			}
		}
		//start subthreads
		bool allstarted;
		do
		{
			allstarted = true;
			for (int i : _batch)
			{
				if (!_info[i].started)
				{
					allstarted = false;
					break;
				}
			}
		} while (!allstarted);
		{
			std::vector<std::unique_lock<std::mutex>> lks;
			for (int i : _batch)
			{
				lks.emplace_back(_info[i].run_mtx);
				_info[i].next.store(true);
			}
			assert(_cv.native_handle() != nullptr);
			_cv.notify_all();
			lks.empty();
		}
		//let sunthreads run timeout ms.
		int timeout = TIMEOUT;
		if (_frame == 0)
		{
			timeout = START_TIMEOUT;
		}
		LARGE_INTEGER DueTime;
		DueTime.QuadPart = -timeout * 1000'0;
		SetWaitableTimer(_timer, &DueTime, 0, NULL, NULL, FALSE);
		WaitForSingleObject(_timer, INFINITE);
		for (int i : _batch)
		{
			_info[i].comm_mtx.lock();
			if (SuspendThread(_info[i].handle) == 0xFFFFFFFF)
			{
				mylog << "player: " << i << " Cannot suspend Thread" << _info[i].threadID << " Error Code: " << GetLastError() << std::endl;
			}
			_info[i].comm_mtx.unlock();
			_info[i].state = AI_STATE::SUSPENDED;
		}
	}
	//kill AI who sended nothing when parachuting
	if (_frame == 0)
	{
		for (int i = 0; i < _player_count; ++i)
		{
			_info[i].comm_mtx.lock();
			bool isempty = _command_parachute[i].empty();
			_info[i].comm_mtx.unlock();
			if (isempty)
			{
				_kill_one(i);
				mylog << "player: " << i << " is killed because of sending nothing when parachuting" << std::endl;
				COMMAND_PARACHUTE c;
				c.role = -1;
				c.team = _info[i].team;
				c.landing_point = { 0,0 };
				_command_parachute[i].push_back(c);
			}
		}
	}
	++_frame;
}

bool Controller::receive(const std::string & data)
{
	if (!_check_init())
		return false;
	return _parse(data);

}

void Controller::_send(int playerID, int new_frame, const std::string & data)
{
	if (!_check_init())
		return;
	_info[playerID].recv_func(new_frame, data);
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
			_info[playerID].comm_mtx.lock();
			_command_action[playerID].push_back(c);
			_info[playerID].comm_mtx.unlock();
			return true;
		}
		else
		{
			COMMAND_PARACHUTE c;
			c.landing_point.x = recv.landing_point().x();
			c.landing_point.y = recv.landing_point().y();
			c.role = recv.role();
			c.team = _info[playerID].team;
			_info[playerID].comm_mtx.lock();
			_command_parachute[playerID].push_back(c);
			_info[playerID].comm_mtx.unlock();
			return true;
		}
	}
	else
	{
		return false;
	}
}

void Controller::_run_player(int playerID)
{
	if (_info[playerID].player_func == nullptr)
		return;
	_info[playerID].started = true;
	while (true)
	{
		{
			auto lk = std::unique_lock<std::mutex>(_info[playerID].run_mtx);
			_info[playerID].next.store(false);
			_cv.wait(lk, [&] {return _info[playerID].next.load(); });
		}
		(*_info[playerID].player_func)();
	}
	return;
}

int Controller::_get_playerID_by_threadID()
{
	if (!_check_init())
		return -1;
	auto threadID = GetCurrentThreadId();
	for (int i : _batch)
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
	int playerID = reinterpret_cast<int>(lpParameter);
	manager._run_player(playerID);
	return 0;
}

bool controller_receive(const std::string data)
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
		if (!_command_action[i].empty() && _info[i].state != AI_STATE::DEAD)
		{
			m[i] = { _command_action[i].cbegin(),_command_action[i].cend() };
		}
	}
	return m;
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

std::string Controller::_serialize_info(int playerID)
{
	return player_infos[playerID];
}

void controller_update(int player_frame)
{
	if (player_frame != manager._frame)
	{
		int playerID = manager._get_playerID_by_threadID();
		manager._send(playerID, manager._frame, manager.player_infos[playerID]);
	}
}