#ifndef VISION_H
#define VISION_H

#include "obj.h"

enum class LANDFORM_TYPE
{
    WALL = 1,
    TREE = 2
};

class LandForm : public Object
{
  public:
    LandForm(LANDFORM_TYPE land_type);
    LandForm(LandForm &&) = default;
    LandForm(const LandForm &) = default;
    LandForm &operator=(LandForm &&) = default;
    LandForm &operator=(const LandForm &) = default;
    ~LandForm();

  private:
    LANDFORM_TYPE _land_type;
};

class Vision
{
  public:
    Vision(int id, BASE_T distance, BASE_T angle);
    Vision(Vision &&) = default;
    Vision(const Vision &) = default;
    Vision &operator=(Vision &&) = default;
    Vision &operator=(const Vision &) = default;
    ~Vision();

  private:
    int _id;
    BASE_T _distance;
    BASE_T _angle;
};

#endif // !VISION_H