#include "base.h"

//player-used
XYPosition start_pos, over_pos;
std::vector<int> teammates;
int frame = -1;
PlayerInfo info;

//The newest info from platform
int _new_frame;
std::string _new_data;

static decltype(&player_send) _player_send = nullptr;
static decltype(&player_update) _player_update = nullptr;

void player_receive(int new_frame, const std::string data)
{
	_new_frame = new_frame;
	_new_data = data;
}

bool player_send(const std::string data)
{
	return (*_player_send)(data);
}

void player_update(int local_frame)
{
	(*_player_update)(local_frame);
}

void bind_api(decltype(_player_send) func1, decltype(_player_update)func2)
{
	_player_send = func1;
	_player_update = func2;
}

