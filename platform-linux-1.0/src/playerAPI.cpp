#include "playerAPI.h"

extern ThreadControl *pThreadController;

void SendDemand(int cd, int order)
{
    DEMAND tmp{cd, order};
    pThreadController->SendDemand(tmp);
}