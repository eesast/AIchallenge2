#include"playerAI.h"

Position start_pos, over_pos;

decltype(&player_send) _player_send = nullptr;

void player_receive(bool is_parachute, const std::string data)
{
    //if jumping, data is platform::parachute, else data is teaminfo.
    if (is_parachute)
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

bool player_send(bool is_parachute, const std::string data)
{
    return (*_player_send)(is_parachute, data);
}

void bind_api(decltype(_player_send) func)
{
    _player_send = func;
}
void play_game()
{
    using namespace std;
    cout << "player" << endl;
    VOCATION_TYPE role[MEMBER_COUNT] = { VOCATION_TYPE::ENGINEER, VOCATION_TYPE::HACK, VOCATION_TYPE::MEDIC, VOCATION_TYPE::SNIPER };
    Position landing_points[MEMBER_COUNT] = { over_pos,start_pos,over_pos,start_pos };
    parachute(role, landing_points);
    return;
}
