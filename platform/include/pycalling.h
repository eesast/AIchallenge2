#ifndef PYCALLING_H
#define PYCALLING_H

#include <python3.6m/Python.h>
#include <iostream>
#include <cstdlib>

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
  void init(const char *module_name, const char *main_func_name);
  void do_loop();

private:
  Pycalling();
  bool _is_init = false;
  static Pycalling _instance;
  PyObject *_game_main;
};

#endif //!PYCALLING_H
