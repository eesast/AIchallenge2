#include"base.h"
#include"./../../include/api.h"

void parachute(VOCATION role, Position landing_points)
{
    comm::Command sender;
    sender.set_command_type(comm::CommandType::PARACHUTE);
    sender.set_role(role);
    auto pos = sender.mutable_landing_point();
    pos->set_x(landing_points.x);
    pos->set_y(landing_points.y);
    std::cout << "AI:" << sender.DebugString() << std::endl;
    player_send(true, sender.SerializeAsString());
}
void shoot(int weapon_ID, double shoot_angle, int parameter)
{
    comm::Command sender;
    sender.set_command_type(comm::CommandType::SHOOT);
    sender.set_target_id(weapon_ID);
    sender.set_view_angle(shoot_angle);
    sender.set_parameter(parameter);
    player_send(false, sender.SerializeAsString());
}
void move(double move_angle, double view_angle, int parameter)
{
    comm::Command sender;
    sender.set_command_type(comm::CommandType::MOVE);
    sender.set_move_angle(move_angle);
    sender.set_view_angle(view_angle);
    sender.set_parameter(parameter);
    player_send(false, sender.SerializeAsString());
}
void pickup(int target_ID, int parameter)
{
    comm::Command sender;
    sender.set_command_type(comm::CommandType::PICKUP);
    sender.set_target_id(target_ID);
    sender.set_parameter(parameter);
    player_send(false, sender.SerializeAsString());
}
void radio(int target_ID, int msg)
{
    comm::Command sender;
    sender.set_command_type(comm::CommandType::RADIO);
    sender.set_target_id(target_ID);
    sender.set_parameter(msg);
    player_send(false, sender.SerializeAsString());
}