#include "vision.h"

LandForm::LandForm(LANDFORM_TYPE land_type) : _land_type(land_type)
{
}

LandForm::~LandForm()
{
}

Vision::Vision(int id, BASE_T distance, BASE_T angle) : _id(id), _distance(distance), _angle(angle)
{
}

Vision::~Vision()
{
}
