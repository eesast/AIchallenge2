#include"base.h"
#include"./../../include/api.h"

void parachute(VOCATION_TYPE role[MEMBER_COUNT], Position landing_points[MEMBER_COUNT])
{
    comm_player::Parachute sender;
    for (int i = 0; i < MEMBER_COUNT; i++)
    {
        switch (role[i])
        {
        case VOCATION_TYPE::MEDIC:
            sender.add_types(comm_player::Vocation::MEDIC);
            break;
        case VOCATION_TYPE::ENGINEER:
            sender.add_types(comm_player::Vocation::ENGINEER);
            break;
        case VOCATION_TYPE::SIGNALMAN:
            sender.add_types(comm_player::Vocation::SIGNALMAN);
            break;
        case VOCATION_TYPE::HACK:
            sender.add_types(comm_player::Vocation::HACK);
            break;
        case VOCATION_TYPE::SNIPER:
            sender.add_types(comm_player::Vocation::SNIPER);
            break;
        }
        auto pos = sender.add_landing_points();
        pos->set_x(landing_points[i].x);
        pos->set_y(landing_points[i].y);
    }
    std::cout << "AI:" << sender.DebugString() << std::endl;
    player_send(true, sender.SerializeAsString());
}
void shoot(int player_ID, int weapon_ID, double shoot_angle, int parameter)
{
    comm_player::Command sender;
    sender.set_command_type(comm_player::CommandType::SHOOT);
    sender.set_player_id(player_ID);
    sender.set_target_id(weapon_ID);
    sender.set_view_angle(shoot_angle);
    sender.set_parameter(parameter);
    player_send(false, sender.SerializeAsString());
}
void move(int player_ID, double move_angle, double view_angle, int parameter)
{
    comm_player::Command sender;
    sender.set_command_type(comm_player::CommandType::MOVE);
    sender.set_player_id(player_ID);
    sender.set_move_angle(move_angle);
    sender.set_view_angle(view_angle);
    sender.set_parameter(parameter);
    player_send(false, sender.SerializeAsString());
}
void pickup(int player_ID, int target_ID, int parameter)
{
    comm_player::Command sender;
    sender.set_command_type(comm_player::CommandType::PICKUP);
    sender.set_player_id(player_ID);
    sender.set_target_id(target_ID);
    sender.set_parameter(parameter);
    player_send(false, sender.SerializeAsString());
}
void radio(int player_ID, int target_ID, int msg)
{
    comm_player::Command sender;
    sender.set_command_type(comm_player::CommandType::RADIO);
    sender.set_player_id(player_ID);
    sender.set_target_id(target_ID);
    sender.set_parameter(msg);
    player_send(false, sender.SerializeAsString());
}