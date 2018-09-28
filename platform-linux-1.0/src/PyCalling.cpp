#include "PyCalling.h"

PyCalling::PyCalling(const char *moduleName, const char *initFuncName, const char *mainFuncName, CState &state, CDemands &demands, std::vector<DEMAND> allDemands[], unsigned int count)
{
    pState = &state;
    pDemands = &demands;
    pAllDemands = allDemands;
    playerCount = count;
    Py_Initialize();
    //add cwd into path
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("import os");
    PyRun_SimpleString("sys.path.insert(0,os.getcwd())");
    PyObject *pMod = PyImport_ImportModule(moduleName);
    //get function object
    if (pMod == NULL)
    {
        std::cerr << "Cannot import module. Please check module name and module file." << std::endl;
        PyObject *ptype, *pvalue, *ptraceback;
        PyObject *pystr;
        PyErr_Fetch(&ptype, &pvalue, &ptraceback);
        pystr = PyObject_Str(pvalue);
        Py_ssize_t tmp;
        std::wcout << PyUnicode_AsWideCharString(pystr, &tmp) << std::endl;
        std::cin.get();
        std::cin.get();
        exit(1);
    }
    pFunc_game_main = PyObject_GetAttrString(pMod, mainFuncName);
    if (pFunc_game_main == NULL)
    {
        std::cerr << "Cannot get game_main function. Please check game_main funcion name in C++ code or python code." << std::endl;
        PyObject *ptype, *pvalue, *ptraceback;
        PyObject *pystr;
        PyErr_Fetch(&ptype, &pvalue, &ptraceback);
        pystr = PyObject_Str(pvalue);
        Py_ssize_t tmp;
        std::wcout << PyUnicode_AsWideCharString(pystr, &tmp) << std::endl;
        std::cin.get();
        std::cin.get();
        exit(1);
    }
    PyObject *pFunc_game_init = PyObject_GetAttrString(pMod, initFuncName);
    if (pFunc_game_init == NULL)
    {
        std::cerr << "Cannot get game_init function. Please check game_init funcion name in C++ code or python code." << std::endl;
        PyObject *ptype, *pvalue, *ptraceback;
        PyObject *pystr;
        PyErr_Fetch(&ptype, &pvalue, &ptraceback);
        pystr = PyObject_Str(pvalue);
        Py_ssize_t tmp;
        std::wcout << PyUnicode_AsWideCharString(pystr, &tmp) << std::endl;
        std::cin.get();
        std::cin.get();
        exit(1);
    }
    Py_DECREF(pMod);

#ifdef PLATFORM_DEBUG
    backup = std::wclog.rdbuf();
    pFunc_change_to_string = PyObject_GetAttrString(pMod, PYFUNCNAME_TO_STRING);
    if (pFunc_change_to_string == NULL)
    {
        std::cerr << "Cannot get DEBUG function. Please check DEBUG funcion name in C++ code or python code." << std::endl;
        PyObject *ptype, *pvalue, *ptraceback;
        PyObject *pystr;
        PyErr_Fetch(&ptype, &pvalue, &ptraceback);
        pystr = PyObject_Str(pvalue);
        Py_ssize_t tmp;
        std::wcout << PyUnicode_AsWideCharString(pystr, &tmp) << std::endl;
        std::cin.get();
        std::cin.get();
        exit(1);
    }
    file.open(FILENAME_LOG, std::ios_base::out);
    if (!file.is_open())
    {
        std::cerr << "Cannot open log file. Please check your access of " << FILENAME_LOG << ". Will Use wclog instead." << std::endl;
    }
    else
    {
        std::wclog.rdbuf(file.rdbuf());
    }
#endif
    //call game_init
    PyObject *pTuple_state_and_demands = PyObject_CallObject(pFunc_game_init, nullptr);
    Py_DECREF(pFunc_game_init);
    //get dict_state and its ownership
    PyObject *pDict_state = PyTuple_GetItem(pTuple_state_and_demands, 0);
    Py_INCREF(pDict_state);
    //get list_demands and its ownership
    PyObject *pList_demands = PyTuple_GetItem(pTuple_state_and_demands, 1);
    Py_INCREF(pList_demands);
    Py_DECREF(pTuple_state_and_demands);
    //pass on them to c++ class CState and CDemands
    pState->SetFromPyDict(pDict_state);
    Py_DECREF(pDict_state);
    pDemands->SetFromPyList(pList_demands);
    Py_DECREF(pList_demands);
}

PyCalling::~PyCalling()
{
#ifdef PLATFORM_DEBUG
    if (file.is_open())
    {
        file.close();
    }
    std::wclog.rdbuf(backup);
#endif
    Py_Finalize();
}

void PyCalling::DoLoop()
{
    pDemands->MergeDemands(pAllDemands, playerCount);
    for (size_t i = 0; i < playerCount; i++)
    {
        pAllDemands[i].clear();
    }
    //get ownership temporarily for calling game_main
    PyObject *pDict_state = pState->ChangeToPyObject();
    Py_INCREF(pDict_state);
    PyObject *pList_demands = pDemands->ChangeToPyObject();
    Py_INCREF(pList_demands);
    PyObject *pArgs = PyTuple_Pack(2, pDict_state, pList_demands);
    Py_DECREF(pList_demands);
    Py_DECREF(pDict_state);
    PyObject *pTuple_state_and_demands = PyObject_CallObject(pFunc_game_main, pArgs);
    Py_DECREF(pArgs);

#ifdef PLATFORM_DEBUG
    PyObject *pString = PyObject_CallObject(pFunc_change_to_string, pTuple_state_and_demands);
    auto len = PyUnicode_AsWideChar(pString, buffer, PyUnicode_GetSize(pString));
    len = (len >= MAX_STRING ? MAX_STRING - 1 : len);
    buffer[len] = 0;
    std::wclog << buffer << std::endl;
    Py_DECREF(pString);
#endif

    //get dict_state and its ownership
    pDict_state = PyTuple_GetItem(pTuple_state_and_demands, 0);
    Py_INCREF(pDict_state);
    //get list_demands and its ownership
    pList_demands = PyTuple_GetItem(pTuple_state_and_demands, 1);
    Py_INCREF(pList_demands);
    Py_DECREF(pTuple_state_and_demands);
    //pass on them to c++ class CState and CDemands
    pState->SetFromPyDict(pDict_state);
    Py_DECREF(pDict_state);
    pDemands->SetFromPyList(pList_demands);
    Py_DECREF(pList_demands);
}
