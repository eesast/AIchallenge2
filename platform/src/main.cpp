#include "controller.h"
#include "pycalling.h"
#include <filesystem>
#include <ctime>
#include <iostream>
#include <fstream>

#pragma warning(disable:4996)

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

int main(int argc, char *argv[])
{
	namespace fs = std::filesystem;
	std::cout << fs::current_path() << std::endl;
	fs::create_directory(fs::current_path() / fs::path::path(L"AI/"));
	std::string path_str = "./AI/";
	fs::path path(path_str);
	path = fs::current_path() / path;
	if (argc > 1)
	{
		path_str = argv[1];
		path = fs::path(path_str);
	}

	//log system
	fs::create_directory(fs::current_path() / fs::path::path(L"log/"));
	mylog.open("./log/log" + get_date_string(true) + ".txt");
	mylog << get_date_string(false) << std::endl;

	// init
	manager.route = logic.init();
	manager.init(path);

	//run
	std::pair<std::map<int, std::string>, std::vector<int>> state_c;
	if (manager.has_living_player())
	{
		manager.run();
		state_c = logic.parachute(manager.get_parachute_commands());
		manager.player_infos = state_c.first;
		manager.dead = state_c.second;
	}
	while (manager.has_living_player())
	{
		manager.run();
		state_c = logic.do_loop(manager.get_action_commands());
		manager.player_infos = state_c.first;
		manager.dead = state_c.second;
		mylog.flush();
	}
	logic.~Pycalling();		//avoid SEGFAULT about Protobuf when calling Py_Finalize() after "return 0"
	mylog << "exit normally" << std::endl;
	mylog.close();
	getchar();
	return 0;
}
