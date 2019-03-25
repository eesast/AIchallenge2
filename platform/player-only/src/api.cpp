#include"base.h"
#include"api.h"

//player-used
extern XYPosition start_pos, over_pos;
extern std::vector<int> teammates;
extern int frame;
extern PlayerInfo info;

//The newest info from platform
extern int _new_frame;
extern std::string _new_data;

namespace ts20
{
	static void _parse(int new_frame, const std::string & data)
	{
		//if jumping, data is platform::parachute, else data is teaminfo.
		frame = new_frame;
		if (new_frame == 0)
		{
			comm::Route recv;
			if (recv.ParseFromString(data))
			{
				start_pos.x = recv.start_pos().x();
				start_pos.y = recv.start_pos().y();
				over_pos.x = recv.over_pos().x();
				over_pos.y = recv.over_pos().y();
				std::cout << "teammate:";
				teammates.clear();
				for (auto teammate : recv.teammates())
				{
					teammates.push_back(teammate);
					std::cout << teammate << ' ';
				}
				std::cout << std::endl;
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
			comm::PlayerInfo recv;
			if (recv.ParseFromString(data))
			{
				// SelfInfo
				const auto & self = recv.self();
				auto & self_c = info.self;
				self_c.hp = self.health_point();
				self_c.hp_limit = self.health_point_limit();
				self_c.move_angle = self.move_angle();
				self_c.view_angle = self.view_angle();
				self_c.move_angle = self.move_speed();
				self_c.vocation = static_cast<VOCATION>(self.vocation());
				self_c.status = static_cast<STATUS>(self.status());
				self_c.move_cd = self.move_cd();
				self_c.attack_cd = self.attack_cd();
				self_c.xy_pos.x = self.pos().x();
				self_c.xy_pos.y = self.pos().y();
				self_c.view_width = self.view_width();
				self_c.view_distance = self.view_distance();
				// bag
				self_c.bag.clear();
				for (const auto & item : self.bag())
				{
					Item item_c;
					item_c.item_ID = item.item_id();
					item_c.durability = item.durability();
					item_c.type = static_cast<ITEM>(item.type());
					item_c.polar_pos.angle = item.pos().angle();
					item_c.polar_pos.distance = item.pos().distance();
					self_c.bag.push_back(item_c);
				}
				// landform
				info.landform_IDs.clear();
				for (const auto & landform_id : recv.landform_id())
				{
					info.landform_IDs.push_back(landform_id);
				}
				// items
				info.items.clear();
				for (const auto & item : recv.items())
				{
					Item item_c;
					item_c.item_ID = item.item_id();
					item_c.durability = item.durability();
					item_c.type = static_cast<ITEM>(item.type());
					item_c.polar_pos.angle = item.pos().angle();
					item_c.polar_pos.distance = item.pos().distance();
					info.items.push_back(item_c);
				}
				//others
				info.others.clear();
				for (const auto & other : recv.others())
				{
					OtherInfo other_c;
					other_c.player_ID = other.player_id();
					other_c.status = static_cast<STATUS>(other.status());
					other_c.move_angle = other.move_angle();
					other_c.view_angle = other.view_angle();
					other_c.move_speed = other.move_speed();
					other_c.vocation = static_cast<VOCATION>(other.vocation());
					other_c.polar_pos.angle = other.pos().angle();
					other_c.polar_pos.distance = other.pos().distance();
					info.others.push_back(other_c);
				}
				//sound
				info.sounds.clear();
				for (const auto & sound : recv.sounds())
				{
					Sound sound_c;
					sound_c.sender = sound.sender();
					sound_c.delay = sound.delay();
					sound_c.parameter = sound.parameter();
					sound_c.type = static_cast<SOUND>((sound_c.parameter >> 29) & 0x00000007);
					sound_c.parameter &= 0x1FFFFFFF;
					info.sounds.push_back(sound_c);
				}
				//player_ID
				info.player_ID = recv.player_id();
				//poison
				const auto & poison = recv.poison();
				auto & poison_c = info.poison;
				poison_c.current_center.x = poison.current_center().x();
				poison_c.current_center.y = poison.current_center().y();
				poison_c.next_center.x = poison.next_center().x();
				poison_c.next_center.y = poison.next_center().y();
				poison_c.current_radius = poison.current_radius();
				poison_c.next_radius = poison.next_radius();
				poison_c.rest_frames = poison.rest_frames();
				poison_c.move_flag = poison.move_flag();
			}
			else
			{
				std::cerr << "fail to parse" << std::endl;
			}
		}
	}

	void parachute(VOCATION role, XYPosition landing_points)
	{
		comm::Command sender;
		sender.set_command_type(comm::CommandType::PARACHUTE);
		sender.set_role(role);
		auto pos = sender.mutable_landing_point();
		pos->set_x(landing_points.x);
		pos->set_y(landing_points.y);
		std::cout << "AI:" << sender.DebugString() << std::endl;
		player_send(sender.SerializeAsString());
	}

	void shoot(ITEM item_type, double shoot_angle, int parameter)
	{
		comm::Command sender;
		sender.set_command_type(comm::CommandType::SHOOT);
		sender.set_target_id(item_type);
		sender.set_view_angle(shoot_angle);
		sender.set_parameter(parameter);
		player_send(sender.SerializeAsString());
	}

	void move(double move_angle, double view_angle)
	{
		comm::Command sender;
		sender.set_command_type(comm::CommandType::MOVE);
		sender.set_move_angle(move_angle);
		sender.set_view_angle(view_angle);
		sender.set_parameter(-1);
		player_send(sender.SerializeAsString());
	}

	void pickup(int target_ID, int parameter)
	{
		comm::Command sender;
		sender.set_command_type(comm::CommandType::PICKUP);
		sender.set_target_id(target_ID);
		sender.set_parameter(parameter);
		player_send(sender.SerializeAsString());
	}

	void radio(int target_ID, int msg)
	{
		comm::Command sender;
		sender.set_command_type(comm::CommandType::RADIO);
		sender.set_target_id(target_ID);
		sender.set_parameter(msg);
		player_send(sender.SerializeAsString());
	}

	void update_info()
	{
		player_update(_new_frame);
		while (_new_frame == frame)
			;
		_parse(_new_frame, _new_data);
	}

	bool try_update_info()
	{
		player_update(_new_frame);
		if (_new_frame == frame)
		{
			return false;
		}
		else
		{
			_parse(_new_frame, _new_data);
			return true;
		}
	}

	block get_landform(int landform_ID)
	{
		int area_ID = (landform_ID >> 8) & 0x0000'00FF;
		int block_ID = landform_ID & 0x0000'00FF;
		if (area_ID < MAP_SZ || block_ID < AREA_DATA[MAP[area_ID]].size())
		{
			block b = AREA_DATA[MAP[area_ID]][block_ID];
			int bias_x = 100 * (area_ID % 10);
			int bias_y = 100 * (area_ID / 10);
			switch (b.shape)
			{
			case DOT:
			case CIRCLE:
				b.x0 += bias_x;
				b.y0 += bias_y;
				break;
			case RECTANGLE:
				b.x0 += bias_x;
				b.y0 += bias_y;
				b.x1 += bias_x;
				b.y1 += bias_y;
				break;
			default:
				break;
			}
			return b;
		}
		else
		{
			// wrong landform id
			return { BLOCK_SHAPE_SZ,BLOCK_TYPE_SZ,0,0,0,0,0 };
		}
	}
}