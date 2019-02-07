#ifndef API_H
#define API_H

#ifndef AI_EXPORTS
#include"controller.h"
#endif
#include"constant.h"
#include"character.h"
void parachute(VOCATION role, Position landing_points);
void shoot(int weapon_ID, double shoot_angle,  int parameter);
void move(double move_angle, double view_angle, int parameter);
void pickup(int target_ID, int parameter);
void radio(int target_ID, int msg);

#endif