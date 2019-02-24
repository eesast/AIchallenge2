#include "controller.h"

Controller Controller::_instance;

void Controller::init(const std::string &path, DWORD used_core_count)
{
	using namespace std::filesystem;
	auto PAT = std::regex(R"((AI_(\d*)_(\d*)).dll)", std::regex_constants::ECMAScript | std::regex_constants::icase);
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
						auto bind_api = (void(*)(Player_Send_Func, Player_Update))GetProcAddress(_info[player_count].lib, "bind_api");
						_info[player_count].player_func = (AI_Func)GetProcAddress(_info[player_count].lib, "play_game");
						_info[player_count].recv_func = (Recv_Func)GetProcAddress(_info[player_count].lib, "player_receive");
						if (bind_api == NULL || _info[player_count].player_func == NULL || _info[player_count].recv_func == NULL)
						{
							std::cerr << "Cannot Get AI API from " << _info[player_count].lib << " Error Code:" << GetLastError() << std::endl;
							continue;
						}
						else
						{
							_team[team].push_back(player_count);
							(*bind_api)(&controller_receive, &controller_update);
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
		_kill_one(i);
	}
	delete _waiting_thread;
	_waiting_thread = nullptr;
}

void Controller::_kill_one(int playerID)
{
	if (_info[playerID].state != AI_STATE::DEAD)
	{
		if (_info[playerID].state != AI_STATE::UNUSED)
		{
			TerminateThread(_info[playerID].handle, 0);
			CloseHandle(_info[playerID].handle);
		}
		FreeLibrary(_info[playerID].lib);
		_info[playerID].state = AI_STATE::DEAD;
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
	int now = 0;
	//main_loop
	while (now < _player_count)
	{
		//set batch
		_batch.clear();
		for (int i = 0; i < static_cast<int>(_used_core_count); )
		{
			if (now >= _player_count)
			{
				break;
			}
			else if (_info[now].state != AI_STATE::DEAD)
			{
				_batch.push_back(now);
				++now;
				++i;
			}
			else
			{
				++now;
			}
		}
		//execute some players each loop. The number is equal to the number of core(_used_core_count) 
		int core_num = _total_core_count - _used_core_count;
		for (int i : _batch)
		{
			//  i == playerID
			if (_info[i].state == AI_STATE::UNUSED)
			{
				//create or recreate a subthread.
				_info[i].handle = CreateThread(nullptr, 0, thread_func, nullptr, CREATE_SUSPENDED, &_info[i].threadID);
				if (_info[i].handle == NULL)
				{
					std::cerr << "Cannot create thread. Error Code: " << GetLastError() << std::endl;
					system("pause");
					exit(1);
				}
				_info[i].state = AI_STATE::SUSPENDED;
				//CPU control, choose the core which the thread uses. When the used core number is less than that CPU actually has, using core with higher ID firstly 
				if (SetThreadAffinityMask(_info[i].handle, (static_cast<DWORD_PTR>(1) << core_num)))
				{
					++core_num;
				}
				else
				{
					std::cerr << "CPU core setting fails. Error Code: " << GetLastError() << std::endl;
				}
			}
			_waiting_thread[i] = _info[i].handle;    //if the player's thread is suspended, just resume it
		}
		//send route and start subthread.
		for (int i : _batch)
		{
			_info[i].state = AI_STATE::ACTIVE;
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
				std::cerr << "Cannot resume Thread" << _info[i].threadID << " Error Code: " << GetLastError() << std::endl;
			}
		}
		DWORD threadNumber = static_cast<DWORD>(_batch.size());
		//let sunthreads run TIMEOUT ms.
		if (WaitForMultipleObjects(threadNumber, _waiting_thread, true, TIMEOUT) == WAIT_TIMEOUT)
		{    //if one thread does not exit 
			DWORD exitCode;
			for (int i : _batch)
			{    //look out still active thread and suspend it forcefully
				GetExitCodeThread(_info[i].handle, &exitCode);
				if (exitCode == STILL_ACTIVE)
				{
					_info[i].state = AI_STATE::SUSPENDED;
					if (SuspendThread(_info[i].handle) == 0xFFFFFFFF)
					{
						std::cerr << "Cannot suspend Thread" << _info[i].threadID << " Error Code: " << GetLastError() << std::endl;
					}
				}
				else
				{
					_info[i].state = AI_STATE::UNUSED;
					CloseHandle(_info[i].handle);
				}
			}
		}
		else
		{
			for (int i : _batch)
			{
				_info[i].state = AI_STATE::UNUSED;
				CloseHandle(_info[i].handle);
			}
		}
	}
	++_frame;
}

bool Controller::receive(const std::string & data)
{
	if (!_check_init())
		return false;
	std::cout << "receive" << std::endl;
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
	auto playerID = manager._get_playerID_by_threadID();
	if (manager._info[playerID].player_func != nullptr)
	{
		(*manager._info[playerID].player_func)();
	}
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
		if (!_command_action[i].empty())
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