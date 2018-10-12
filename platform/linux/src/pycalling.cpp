#include "pycalling.h"

Pycalling::Pycalling(const char *moduleName, const char *mainFuncName)
{
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
    Py_DECREF(pMod);
}

Pycalling::~Pycalling()
{
    Py_Finalize();
}

void Pycalling::DoLoop()
{
}
