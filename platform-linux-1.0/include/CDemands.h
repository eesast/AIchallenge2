#ifndef CDEMANDS_H
#define CDEMANDS_H

#include "Header.h"
#include <vector>

struct DEMAND
{
    int cd;
    int order;
    DEMAND()
    noexcept {}
    DEMAND(int cd, int order)
    noexcept : cd(cd), order(order)
    {
    }
};

class CDemands
{
  public:
    CDemands() noexcept;
    ~CDemands();

  private:
    std::vector<DEMAND> m_vDemands;
    PyObject *m_pList_demands;

    const char *CD_STRING = "cd";
    const char *ORDER_STRING = "order";
    //used in MergeDemands
    void AppendDemand(const DEMAND &demand);

  public:
    //Platform only
    void SetFromPyList(PyObject *pList_demands);
    PyObject *ChangeToPyObject() const;
    //designed for multithread, merge all players' demands into CDemands
    void MergeDemands(const std::vector<DEMAND> playersDemands[], unsigned int playerCount);
};

#endif // !CDEMANDS_H
