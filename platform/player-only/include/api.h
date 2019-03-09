#ifndef API_H
#define API_H

#include"constant.h"

void parachute(VOCATION role, XYPosition landing_points);
void shoot(ITEM item_type, double shoot_angle,  int parameter);
void move(double move_angle, double view_angle, int parameter);
void pickup(int target_ID, int parameter);
void radio(int target_ID, int msg);
void update_info();
bool try_update_info();

#endif