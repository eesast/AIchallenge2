#ifndef PYCALLING_H
#define PYCALLING_H

#include <python3.6m/Python.h>
#include <iostream>
#include <cstdlib>

class Pycalling
{
  public:
    Pycalling(const char *moduleName, const char *mainFuncName);
    ~Pycalling();
    void DoLoop();

  private:
    PyObject *pFunc_game_main;
};

#endif //!PYCALLING_H
