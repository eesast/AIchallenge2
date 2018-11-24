#include"base.h"

Position start_pos, over_pos;

static decltype(&player_send) _player_send = nullptr;

void player_receive(bool is_jumping, const std::string data)
{
    //if jumping, data is platform::parachute, else data is teaminfo.
    if (is_jumping)
    {
        comm_player::Route recv;
        if (recv.ParseFromString(data))
        {
            start_pos.x = recv.start_pos().x();
            start_pos.y = recv.start_pos().y();
            over_pos.x = recv.over_pos().x();
            over_pos.y = recv.over_pos().y();
            std::cout << "start_pos" << start_pos.x << ' ' << start_pos.y << std::endl;
            std::cout << "over_pos" << over_pos.x << ' ' << over_pos.y << std::endl;
        }
        else
        {
            std::cerr << "fail to parse" << std::endl;
        }
    }
    else
    {
        comm_player::TeamInfo recv;
        if (recv.ParseFromString(data))
        {
            //parse data
        }
        else
        {
            std::cerr << "fail to parse" << std::endl;
        }
    }
}

bool player_send(bool is_jumping, const std::string data)
{
    return (*_player_send)(is_jumping, data);
}

void bind_api(decltype(_player_send) func)
{
    _player_send = func;
}

