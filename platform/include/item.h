#ifndef ITEM_H
#define ITEM_H

#include "obj.h"

enum class ITEM_NAME
{
    WEAPON_HANDGUN = 1,
    GOODS_CHARGER = 51
};

class Item : public Object
{
  public:
    enum ITEM_TYPE
    {
        WEAPON = 0,
        GOODS = 1
    };

    Item(ITEM_TYPE item_type);
    Item(Item &&) = default;
    Item(const Item &) = default;
    Item &operator=(Item &&) = default;
    Item &operator=(const Item &) = default;
    ~Item();

  private:
    DURABILITY_T _durability;
    ITEM_TYPE _item_type;
    HP_T _damage;
};

#endif // !ITEM_H
