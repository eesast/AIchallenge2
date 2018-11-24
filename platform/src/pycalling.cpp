#include "pycalling.h"

Pycalling Pycalling::_instance;

std::pair<Position, Position> Pycalling::init()
{
    Py_Initialize();
    //add cwd into path
    PyRun_SimpleString("import sys");
    PyRun_SimpleString("import os");
    PyRun_SimpleString("sys.path.insert(0,os.getcwd())");
    PyRun_SimpleString(("sys.path.insert(0,\"" + std::string(LOGIC_PATH) + "\")").c_str());
    PyObject *mod = PyImport_ImportModule(MODULE_NAME);
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
    _game_main = PyObject_GetAttrString(mod, MAIN_FUNC_NAME);
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
    _game_init = PyObject_GetAttrString(mod, INIT_FUNC_NAME);
    if (_game_init == NULL)
    {
        std::cerr << "Cannot get game_init function. Please check game_init funcion name in C++ code or python code." << std::endl;
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
    _parachute = PyObject_GetAttrString(mod, PARACHUTE_FUNC_NAME);
    if (_parachute == NULL)
    {
        std::cerr << "Cannot get parachute function. Please check parachute funcion name in C++ code or python code." << std::endl;
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
    Py_XDECREF(mod);

    //parachute
    auto data_dir = Py_BuildValue("(s)", DATA_PATH);
    auto route = PyObject_CallObject(_game_init, data_dir);
    auto start_pos = PyTuple_GetItem(route, 0);
    auto over_pos = PyTuple_GetItem(route, 1);
    auto route_c = std::make_pair(
        Position{ PyFloat_AsDouble(PyObject_GetAttrString(start_pos,"x")),PyFloat_AsDouble(PyObject_GetAttrString(start_pos,"y")) },
        Position{ PyFloat_AsDouble(PyObject_GetAttrString(over_pos,"x")),PyFloat_AsDouble(PyObject_GetAttrString(over_pos,"y")) }); //memory leak in PyObject_GetAttrString

    Py_XDECREF(route);
    Py_XDECREF(data_dir);
    _is_init = true;
    return route_c;
}

void Pycalling::parachute(std::map<int, COMMAND_PARACHUTE> m)
{
    if (!_check_init())
        return;
    //package:{0:{"role":[0,1,2,3],"landing_points":(x,y)},1:...}
    auto all = PyDict_New();
    for (auto& var : m)
    {
        auto each = Py_BuildValue("{s:i,s:(f,f)}", "vocation", var.second.role, "position", var.second.landing_point.x, var.second.landing_point.y);
        auto player_ID = PyLong_FromLong(var.first);
        PyDict_SetItem(all, player_ID, each);
        Py_XDECREF(player_ID);
        Py_XDECREF(each);
    }
    auto arg = PyTuple_Pack(1, all);
    auto state = PyObject_CallObject(_parachute, arg);
    Py_XDECREF(arg);
    Py_XDECREF(all);
    return; //waiting for logic
}

bool Pycalling::_check_init()
{
    if (!_is_init)
    {
        std::cerr << "Logic is not initialised,please check codes." << std::endl;
    }
    return _is_init;
}

Pycalling::~Pycalling()
{
    if (!_check_init())
        return;
    Py_XDECREF(_game_main);
    Py_XDECREF(_game_init);
    Py_XDECREF(_parachute);
    Py_Finalize();
}
Pycalling::Pycalling()
{
}
void Pycalling::do_loop()
{
    if (!_check_init())
        return;
}
