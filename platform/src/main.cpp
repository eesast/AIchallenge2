#include "controller.h"
#include "pycalling.h"


int main(int argc, char *argv[])
{
	std::pair<std::map<int, std::string>, std::vector<int>> state_c;
    std::string path = ".";
    if (argc > 1)
        path = argv[1];
    manager.init(path);
    manager.route = logic.init();
	if (manager.has_living_player())
	{
		manager.run();
		state_c = logic.parachute(manager.get_parachute_commands());
		manager.player_infos = state_c.first;
		manager.dead = state_c.second;
	}
	while(manager.has_living_player())
	{
        manager.run();
		state_c = logic.do_loop(manager.get_action_commands());
		manager.player_infos = state_c.first;
		manager.dead = state_c.second;
    }
	logic.~Pycalling();		//avoid SEGFAULT about Protobuf when calling Py_Finalize() after "return 0"
    getchar();
    return 0;
}
