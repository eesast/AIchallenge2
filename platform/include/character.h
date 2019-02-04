#ifndef CHARACTER_H
#define CHARACTER_H

#include "obj.h"


class Character : public Object
{
public:
  enum class STATUS
  {
    RELAX = 0,
    ON_PLANE = 1,
    JUMPING = 2,
    MOVING = 3,
    SHOOTING = 4,
    PICKUP = 5,
    MOVING_SHOOTING = 6,
    DEAD = 7,
    REAL_DEAD = 8
  };

  Character(VOCATION vocation);
  Character(Character &&) = default;
  Character(const Character &) = default;
  Character &operator=(Character &&) = default;
  Character &operator=(const Character &) = default;
  ~Character();

  const HP_T HP_LIMIT = 100;

private:
  VOCATION _vocation;
  HP_T _hp;
  CD_T _move_cd;
  STATUS _status;
};

#endif // !CHARACTER_H