#include "CDemands.h"

CDemands::CDemands() noexcept : m_pList_demands(nullptr)
{
}

CDemands::~CDemands()
{
}

void CDemands::SetFromPyList(PyObject *pList_demands)
{
    //change Ptr and do something necessary about GC
    if (m_pList_demands != nullptr)
        Py_DECREF(m_pList_demands);
    //get ownership
    Py_INCREF(pList_demands);
    m_pList_demands = pList_demands;
    Py_ssize_t size = PyList_Size(pList_demands);
    m_vDemands.clear();
    m_vDemands.reserve(size);
    for (Py_ssize_t i = 0; i < size; i++)
    {
        DEMAND tmp;
        tmp.cd = PyLong_AsLong(PyDict_GetItemString(PyList_GetItem(pList_demands, i), CD_STRING));
        tmp.order = PyLong_AsLong(PyDict_GetItemString(PyList_GetItem(pList_demands, i), ORDER_STRING));
        m_vDemands.push_back(tmp);
    }
}

void CDemands::AppendDemand(const DEMAND &demand)
{
    PyObject *pDict_demand = Py_BuildValue("{s:i,s:i}", CD_STRING, demand.cd, ORDER_STRING, demand.order);
    PyList_Append(m_pList_demands, pDict_demand);
    m_vDemands.push_back(demand);
    Py_DECREF(pDict_demand);
}

PyObject *CDemands::ChangeToPyObject() const
{
    return m_pList_demands;
}

void CDemands::MergeDemands(const std::vector<DEMAND> playersDemands[], unsigned int playerCount)
{
    for (size_t i = 0; i < playerCount; i++)
    {
        for (const auto &demand : playersDemands[i])
        {
            AppendDemand(demand);
        }
    }
}
