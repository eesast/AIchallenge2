#ifndef CSTATE_H
#define CSTATE_H

#include "Header.h"

class CState
{
  public:
    CState(int turn = 0, int test = 0) noexcept;
    ~CState();

  private:
    int m_turn;
    int m_test;
    PyObject *m_pDict_state = nullptr;
    const char *TURN_STRING = "turn";
    const char *SCORE_STRING = "test";

  public:
    //player API
    int GetTurn() const;
    int GetTest() const;
    //Platform only
    void SetFromPyDict(PyObject *pDict_state);
    PyObject *ChangeToPyObject() const;
};

#endif // !CSTATE_H
