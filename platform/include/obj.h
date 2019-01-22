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
    Object(SHAPE_TYPE shape = CIRCLE);
    Object(Object &&) = default;
    Object(const Object &) = default;
    Object &operator=(Object &&) = default;
    Object &operator=(const Object &) = default;
    ~Object();

  private:
    Position _position;
    SHAPE_TYPE _shape;
    BASE_T _move_speed;
    BASE_T _move_direction;     //need check DataType
    BASE_T _face_direction;     //need check DataType
    BASE_T _radius;
    BASE_T _angle;
};

#endif // !OBJECT_H