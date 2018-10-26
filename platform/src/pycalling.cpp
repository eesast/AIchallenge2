#include "pycalling.h"

Pycalling Pycalling::_instance;

void Pycalling::init(const char *module_name, const char *main_func_name)
{
    Py_Initialize();
    //add cwd into path
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("import os");
    PyRun_SimpleString("sys.path.insert(0,os.getcwd())");
    PyObject *mod = PyImport_ImportModule(module_name);
    //get function object
    if (mod == NULL)
    {
        std::cerr << "Cannot import module. Please check module name and module file." << std::endl;
        PyObject *type, *value, *traceback;
        PyObject *pystr;
        PyErr_Fetch(&type, &value, &traceback);
        pystr = PyObject_Str(value);
        Py_ssize_t tmp;
        std::wcout << PyUnicode_AsWideCharString(pystr, &tmp) << std::endl;
        std::cin.get();
        std::cin.get();
        exit(1);
    }
    _game_main = PyObject_GetAttrString(mod, main_func_name);
    if (_game_main == NULL)
    {
        std::cerr << "Cannot get game_main function. Please check game_main funcion name in C++ code or python code." << std::endl;
        PyObject *type, *value, *traceback;
        PyObject *pystr;
        PyErr_Fetch(&type, &value, &traceback);
        pystr = PyObject_Str(value);
        Py_ssize_t tmp;
        std::wcout << PyUnicode_AsWideCharString(pystr, &tmp) << std::endl;
        std::cin.get();
        std::cin.get();
        exit(1);
    }
    Py_DECREF(mod);

    _is_init = true;
}

Pycalling::~Pycalling()
{
    Py_Finalize();
}
Pycalling::Pycalling()
{
}
void Pycalling::do_loop()
{
    if (!_is_init)
        return;
}
