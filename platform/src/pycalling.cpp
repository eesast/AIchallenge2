#include "pycalling.h"

extern std::ofstream mylog;

Pycalling Pycalling::_instance;

ROUTE_T Pycalling::init()
{
#ifdef WIN32
	Py_SetPath(L".\\python");
	Py_SetProgramName(L"logic");
#endif
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
		_traceback("Cannot import module. Please check module name and module file.");
	}
	_game_main = PyObject_GetAttrString(mod, MAIN_FUNC_NAME);
	if (_game_main == NULL)
	{
		_traceback("Cannot get game_main function. Please check game_main funcion name in C++ code or python code.");
	}
	_game_init = PyObject_GetAttrString(mod, INIT_FUNC_NAME);
	if (_game_init == NULL)
	{
		_traceback("Cannot get game_init function. Please check game_init funcion name in C++ code or python code.");
	}
	_parachute = PyObject_GetAttrString(mod, PARACHUTE_FUNC_NAME);
	if (_parachute == NULL)
	{
		_traceback("Cannot get parachute function. Please check parachute funcion name in C++ code or python code.");
	}
	Py_XDECREF(mod);
	//fix a possible bug that rls does not want to fix.
	PyRun_SimpleString(("os.makedirs(r\"" + std::string(DATA_PATH) + "../playback/\",exist_ok=True)").c_str());
	//parachute
	auto data_dir = Py_BuildValue("(s)", DATA_PATH);
	auto route = PyObject_CallObject(_game_init, data_dir);
	auto start_pos = PyTuple_GetItem(route, 0);
	auto over_pos = PyTuple_GetItem(route, 1);
	auto start_pos_x = PyObject_GetAttrString(start_pos, "x");
	auto start_pos_y = PyObject_GetAttrString(start_pos, "y");
	auto over_pos_x = PyObject_GetAttrString(over_pos, "x");
	auto over_pos_y = PyObject_GetAttrString(over_pos, "y");
	auto route_c = ROUTE_T{{PyFloat_AsDouble(start_pos_x), PyFloat_AsDouble(start_pos_y)}, {PyFloat_AsDouble(over_pos_x), PyFloat_AsDouble(over_pos_y)}};
	Py_XDECREF(over_pos_y);
	Py_XDECREF(over_pos_x);
	Py_XDECREF(start_pos_y);
	Py_XDECREF(start_pos_x);
	Py_XDECREF(route);
	Py_XDECREF(data_dir);
	_is_init = true;
	return route_c;
}

std::pair<std::map<int, std::string>, std::vector<int>> Pycalling::parachute(const std::map<int, COMMAND_PARACHUTE> &m)
{
	if (!_check_init(true))
		return {};
	//package:{0:{"role":0,"landing_points":(x,y),'team':team_id},1:...}
	auto all = PyDict_New();
	for (const auto &var : m)
	{
		auto each = Py_BuildValue("{s:i,s:(f,f),s:i}", "vocation", var.second.role, "position", var.second.landing_point.x, var.second.landing_point.y, "team", var.second.team);
		auto player_ID = PyLong_FromLong(var.first);
		PyDict_SetItem(all, player_ID, each);
		Py_XDECREF(player_ID);
		Py_XDECREF(each);
	}
	auto arg = PyTuple_Pack(1, all);
	auto state = PyObject_CallObject(_parachute, arg);
	Py_XDECREF(arg);
	Py_XDECREF(all);
	return _parse_dict(state);
}

std::pair<std::map<int, std::string>, std::vector<int>> Pycalling::do_loop(const std::map<int, std::vector<COMMAND_ACTION>> &m)
{
	if (!_check_init(true))
		return {};
	auto all = PyDict_New();
	for (const auto &per : m)
	{
		auto lst = PyList_New(0);
		for (const auto &command : per.second)
		{
			auto dct = Py_BuildValue("{s:i,s:i,s:f,s:f,s:i}", "command_type", command.command_type,
									 "target", command.target_ID, "move_angle", command.move_angle,
									 "view_angle", command.view_angle, "other", command.parameter);
			PyList_Append(lst, dct);
			Py_XDECREF(dct);
		}
		auto player_ID = PyLong_FromLong(per.first);
		PyDict_SetItem(all, player_ID, lst);
		Py_XDECREF(player_ID);
		Py_XDECREF(lst);
	}
	auto arg = PyTuple_Pack(1, all);
	auto state = PyObject_CallObject(_game_main, arg);
	Py_XDECREF(arg);
	Py_XDECREF(all);
	return _parse_dict(state);
}

std::pair<std::map<int, std::string>, std::vector<int>> Pycalling::_parse_dict(PyObject *state)
{
	if (state == NULL)
		_traceback("no return");
	PyObject *key, *value;
	Py_ssize_t pos = 0;
	std::map<int, std::string> player_infos;
	std::vector<int> dead;
	while (PyDict_Next(state, &pos, &key, &value))
	{
		if (PyLong_Check(key))
		{
			player_infos[PyLong_AsLong(key)] = {PyBytes_AsString(value), PyBytes_AsString(value) + PyBytes_Size(value)};
		}
		else
		{
			//dead
			auto dead_list = value;
			for (Py_ssize_t i = 0; i < PyList_Size(dead_list); ++i)
			{
				dead.push_back(PyLong_AsLong(PyList_GetItem(dead_list, i)));
			}
		}
	}
	Py_XDECREF(state);
	return {player_infos, dead};
}

bool Pycalling::_check_init(bool print)
{
	if (!_is_init && print)
	{
		mylog << "Logic is not initialised,please check codes." << std::endl;
	}
	return _is_init;
}

Pycalling::~Pycalling()
{
	if (!_check_init(false))
		return;
	Py_XDECREF(_game_main);
	Py_XDECREF(_game_init);
	Py_XDECREF(_parachute);
	Py_Finalize();
	_is_init = false;
}
Pycalling::Pycalling()
{
}

void Pycalling::_traceback(const std::string &err)
{
	mylog << err << std::endl;
	PyRun_SimpleString("import traceback");
	PyRun_SimpleString("traceback.print_exc(file = sys.stdout)");
	exit(1);
}