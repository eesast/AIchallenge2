#ifndef CHARACTER_H
#define CHARACTER_H

#include "obj.h"

enum class VOCATION_TYPE
{
    MEDIC = 0,
    ENGINEER = 1,
    SIGNALMAN = 2,
    HACK = 3,
    SNIPER = 4
};

class Character : public Object
{
  public:
    Character(VOCATION_TYPE vocation);
    Character(Character &&) = default;
    Character(const Character &) = default;
    Character &operator=(Character &&) = default;
    Character &operator=(const Character &) = default;
    ~Character();

    const HP_T HP_LIMIT = 100;

  private:
    VOCATION_TYPE _vocation;
    HP_T _hp;
    CD_T _move_cd;
};

#endif // !CHARACTER_H