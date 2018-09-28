#ifndef PYCALLING_H
#define PYCALLING_H

#include "Header.h"
#include "CState.h"
#include "CDemands.h"

#ifdef PLATFORM_DEBUG
const unsigned int MAX_STRING = 2000000;
#endif

class PyCalling
{
  public:
    PyCalling(const char *moduleName, const char *initFuncName, const char *mainFuncName, CState &state, CDemands &demands, std::vector<DEMAND> allDemands[], unsigned int count);
    ~PyCalling();
    void DoLoop();

  private:
#ifdef PLATFORM_DEBUG
    const char *PYFUNCNAME_TO_STRING = "change_to_string";
    const char *FILENAME_LOG = "log.txt";
    std::wfstream file;
    std::wstreambuf *backup; //for wclog redirection
    PyObject *pFunc_change_to_string;
    wchar_t buffer[MAX_STRING];
#endif
    PyObject *pFunc_game_main;
    CState *pState = nullptr;
    CDemands *pDemands = nullptr;
    std::vector<DEMAND> *pAllDemands = nullptr;
    unsigned int playerCount;
};

#endif //!PYCALLING_H
