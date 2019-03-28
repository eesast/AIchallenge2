#include "api.h"
#include "base.h"
#include <cstdlib>
#include <ctime>
#include <algorithm>

using namespace ts20;

extern XYPosition start_pos, over_pos;
extern std::vector<int> teammates;
extern int frame;
extern PlayerInfo info;

void play_game()
{
	/* Your code in this function */
	/* sample AI */
	update_info();
	std::cout << "player:frame" << frame << "\nhp:" << info.self.hp << std::endl;
	std::cout << "positon" << info.self.xy_pos.x << ' ' << info.self.xy_pos.y << std::endl;
	if (!info.self.bag.empty())
		std::cout << "pick succeed" << std::endl;
	if (frame == 0)
	{
		srand(time(nullptr) + teammates[0]);
		XYPosition landing_point = { 150 + rand() % 100, 150 + rand() % 100 };
		parachute(HACK, landing_point);
		return;
	}
	else
	{
		srand(time(nullptr) + info.player_ID*frame);
	}
	if (info.self.status == ON_PLANE || info.self.status == JUMPING)
	{
		std::cout << "jumping" << std::endl;
		return;
	}
	if (info.others.empty())
	{
		std::cout << "no others" << std::endl;
		if (info.items.empty())
		{
			//see nothing
			double move_angle = 0;
			double view_angle = move_angle;
			move(move_angle, view_angle);
			std::cout << "move" << move_angle << std::endl;
		}
		else
		{
			Item closest_item;
			closest_item.polar_pos.distance = 100000;
			for (int i = 0; i < info.items.size(); ++i)
			{
				if (info.items[i].polar_pos.distance < closest_item.polar_pos.distance)
				{
					closest_item = info.items[i];
				}
			}
			std::cout << "status" << info.self.status << std::endl;
			std::cout << "**closest item angle" << closest_item.polar_pos.angle << "distance" << closest_item.polar_pos.distance << "**" << std::endl;
			if (closest_item.polar_pos.distance < 1)
			{
				pickup(closest_item.item_ID);
				std::cout << "try pickup" << closest_item.item_ID << std::endl;
			}
			else
			{
				move(closest_item.polar_pos.angle, closest_item.polar_pos.angle);
				std::cout << "move" << closest_item.polar_pos.angle << std::endl;
			}
		}
	}
	else
	{
		bool has_enemy = false;
		OtherInfo closest_enemy;
		closest_enemy.polar_pos.distance = 100000;
		//check teammate
		for (int i = 0; i < info.others.size(); ++i)
		{
			bool is_friend = false;
			for (int teammate = 0; teammate < teammates.size(); ++teammate)
			{
				if (info.others[i].player_ID == teammates[teammate])
				{
					is_friend = true;
					break;
				}
			}
			if (!is_friend && info.others[i].polar_pos.distance < closest_enemy.polar_pos.distance)
			{
				closest_enemy = info.others[i];
				has_enemy = true;
			}
		}
		if (has_enemy)
		{
			ITEM weapon = FIST;
			for (int i = 0; i < info.self.bag.size(); ++i)
			{
				if (ITEM_DATA[info.self.bag[i].type].type == WEAPON && info.self.bag[i].durability > 0)
				{
					weapon = info.self.bag[i].type;
					break;
				}
			}
			if (closest_enemy.polar_pos.distance > ITEM_DATA[weapon].range)
			{
				move(closest_enemy.polar_pos.angle, closest_enemy.polar_pos.angle);
			}
			else
			{
				shoot(weapon, closest_enemy.polar_pos.angle);
			}
		}
	}
	return;
}