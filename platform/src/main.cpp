#include "controller.h"
#include "pycalling.h"
#include <filesystem>
#include <ctime>
#include <iostream>
#include <fstream>

#pragma warning(disable : 4996)

std::ofstream mylog;

std::string get_date_string(bool filename)
{
	std::time_t t = std::time(NULL);
	char mbstr[100];
	if (std::strftime(mbstr, sizeof(mbstr), (filename ? "%F_%H-%M-%S" : "%c"), std::localtime(&t)))
	{
		return { mbstr };
	}
	return {};
}

int main()
{
	int debug_level = 100;
	int batch_size = 0;
#ifdef WIN32
	int debug_flag;
	std::cout << "Choose batch size( <= core number in your computer, input 0 for using all core):";
	std::cin >> batch_size;
	std::cout << "Choose debug level (1: lots of output, other: few output)";
	std::cin >> debug_flag;
	if (debug_flag != 1)
	{
		debug_level = 5;
	}
#endif
	namespace fs = std::filesystem;
	std::cout << fs::current_path() << std::endl;
	fs::create_directory(fs::current_path() / fs::path(L"AI/"));
	std::string path_str = "./AI/";
	fs::path path(path_str);
	path = fs::current_path() / path;

	//log system
	auto time_str = get_date_string(true);
	fs::create_directory(fs::current_path() / fs::path(L"log/"));
	mylog.open("./log/log" + time_str + ".txt");
	mylog << get_date_string(false) << std::endl;

	// init
	manager.route = logic.init(debug_level);
	manager.init(path, static_cast<DWORD>(batch_size));

	//run
	std::pair<std::map<int, std::string>, std::vector<int>> state_c;
	manager.run();
	if (manager.has_living_player())
	{
		state_c = logic.parachute(manager.get_parachute_commands());
		manager.player_infos = state_c.first;
		manager.dead = state_c.second;
		while (true)
		{
			manager.run();
			mylog.flush();
			if (!manager.has_living_player())
			{
				break;
			}
			state_c = logic.do_loop(manager.get_action_commands());
			manager.player_infos = state_c.first;
			manager.dead = state_c.second;
		}
	}
	logic.~Pycalling(); //avoid SEGFAULT about Protobuf when calling Py_Finalize() after "return 0"
	mylog << "exit normally" << std::endl;
	mylog.close();
#ifdef WIN32
	system("pause");
#endif
	return 0;
}
