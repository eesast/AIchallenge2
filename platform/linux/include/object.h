#ifndef OBJECT_H
#define OBJECT_H

#include "constant.h"

class Object
{
  public:


    enum SHAPE_TYPE
    {
        CIRCLE = 0,
        RECTANGLE = 1
    };
    Object(SHAPE_TYPE shape_type = CIRCLE);
    Object(Object &&) = default;
    Object(const Object &) = default;
    Object &operator=(Object &&) = default;
    Object &operator=(const Object &) = default;
    ~Object();

  private:
    Position _position;
    SHAPE_TYPE _shape_type;
    BASE_T _move_speed;
    BASE_T _move_direction;
    BASE_T _face_direction;
    BASE_T _radius;
    BASE_T _angle;
};

#endif // !OBJECT_H