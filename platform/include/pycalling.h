#ifndef PYCALLING_H
#define PYCALLING_H

#ifdef WIN32
#include<Python.h>
#else
#include <python3.6m/Python.h>
#endif // WIN32

#include"platform.h"

//path for finding main.py and data.ini
const char * const LOGIC_PATH = R"(C:\\Users\\zhang\\Desktop\\AIchallenge2\\logic\\)";
const char * const DATA_PATH = R"(C:\Users\zhang\Desktop\AIchallenge2\logic\)";
const char * const MODULE_NAME = "main";
const char * const MAIN_FUNC_NAME = "game_main";
const char * const INIT_FUNC_NAME = "game_init";
const char * const PARACHUTE_FUNC_NAME = "parachute";

#define logic (Pycalling::get_instance())

class Pycalling
{
public:
    static Pycalling &get_instance()
    {
        return _instance;
    }
    ~Pycalling();
    Pycalling(const Pycalling &) = delete;
    Pycalling(Pycalling &&) = delete;
    Pycalling &operator=(const Pycalling &) = delete;
    Pycalling &operator=(Pycalling &&) = delete;
    std::pair<Position, Position> init();
    void parachute(std::map<int, COMMAND_PARACHUTE>m);
    void do_loop();


private:
    Pycalling();
    bool _is_init = false;
    static Pycalling _instance;

    //PYTHON API
    PyObject *_game_init = nullptr;
    PyObject *_game_main = nullptr;
    PyObject *_parachute = nullptr;

};

#endif //!PYCALLING_H