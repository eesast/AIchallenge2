#include "Header.h"
#include "CState.h"

CState::CState(int turn, int test) noexcept : m_turn(turn), m_test(test), m_pDict_state(nullptr)
{
}

CState::~CState()
{
}

int CState::GetTurn() const
{
    return m_turn;
}

int CState::GetTest() const
{
    return m_test;
}

void CState::SetFromPyDict(PyObject *pDict_state)
{
    //change Ptr and do something necessary about GC
    if (m_pDict_state != nullptr)
        Py_DECREF(m_pDict_state);
    //get ownership
    Py_INCREF(pDict_state);
    m_pDict_state = pDict_state;
    m_turn = static_cast<int>(PyLong_AsLong((PyDict_GetItemString(pDict_state, TURN_STRING))));
    m_test = static_cast<int>(PyLong_AsLong((PyDict_GetItemString(pDict_state, SCORE_STRING))));
}

PyObject *CState::ChangeToPyObject() const
{
    return m_pDict_state;
}
