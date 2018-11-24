#ifndef API_H
#define API_H

#ifndef AI_EXPORTS
#include"controller.h"
#endif
#include"constant.h"
#include"character.h"
void parachute(VOCATION_TYPE role[MEMBER_COUNT], Position landing_points[MEMBER_COUNT]);
void shoot(int player_ID, int weapon_ID, double shoot_angle, int parameter);
void move(int player_ID, double move_angle, double view_angle, int parameter);
void pickup(int player_ID, int target_ID, int parameter);
void radio(int player_ID, int target_ID, int msg);

#endif