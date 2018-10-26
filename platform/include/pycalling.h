#ifndef PYCALLING_H
#define PYCALLING_H

#ifdef WIN32
#include<Python.h>
#else
#include <python3.6m/Python.h>
#endif // WIN32

#include"platform.h"



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

    //path for finding main.py
    const char *LOGIC_PATH = R"(C:\\Users\\zhang\\Desktop\\AIchallenge2\\logic)";

    const char *MODULE_NAME = "main";
    const char *MAIN_FUNC_NAME = "game_main";
    const char *INIT_FUNC_NAME = "game_init";
    const char *PARACHUTE_FUNC_NAME = "parachute";
private:
    Pycalling();
    bool _is_init = false;
    static Pycalling _instance;

    //PYTHON API
    PyObject *_game_init;
    PyObject *_game_main;
    PyObject *_parachute;

};

#endif //!PYCALLING_H
