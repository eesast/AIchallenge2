#ifndef API_H
#define API_H

#include"constant.h"
namespace ts20
{
	void parachute(VOCATION role, XYPosition landing_points);
	void shoot(ITEM item_type, double shoot_angle, int parameter = -1);
	void move(double move_angle, double view_angle);
	void pickup(int target_ID, int parameter = -1);
	void radio(int target_ID, int msg);
	void update_info();
	bool try_update_info();
	block get_landform(int landform_ID);
}
#endif