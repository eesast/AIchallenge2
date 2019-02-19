#include "comm_block.h"

void COMM_BLOCK::init()
{
    is_init = false;
    infos_flag.clear();
    commands_flag.clear();
    memset(infos_buf, 0, sizeof(infos_buf));
    for (int i = 0; i < MAX_COMMAND_NUM; ++i)
    {
        commands_len[i] = 0;
        memset(commands_buf[i], 0, sizeof(commands_buf[i]));
    }
    next_command_index = 0;
    infos_len = 0;
    frame = 0;
}

void COMM_BLOCK::set_inited()
{
    is_init = true;
}

void COMM_BLOCK::lock_infos()
{
    while (infos_flag.test_and_set())
        ;
}

bool COMM_BLOCK::try_lock_infos() //return true on success
{
    return !infos_flag.test_and_set();
}

void COMM_BLOCK::unlock_infos()
{
    infos_flag.clear();
}

void COMM_BLOCK::lock_commands()
{
    while (commands_flag.test_and_set())
        ;
}

bool COMM_BLOCK::try_lock_commands() //return true on success
{
    return !commands_flag.test_and_set();
}

void COMM_BLOCK::unlock_commands()
{
    commands_flag.clear();
}

bool COMM_BLOCK::add_command(const std::string &data)
{
    if (next_command_index >= MAX_COMMAND_NUM)
    {
        return false;
    }
    else
    {
        commands_len[next_command_index] = data.length();
        memcpy(commands_buf[next_command_index], data.data(), sizeof(char) * data.length());
        ++next_command_index;
    }
    return true;
}

std::vector<std::string> COMM_BLOCK::get_commands()
{
    using std::string;
    using std::vector;
    vector<string> tmp;
    for (int i = 0; i < next_command_index; ++i)
    {
        tmp.emplace_back(commands_buf[i], commands_buf[i] + commands_len[i]);
    }
    return tmp;
}

void COMM_BLOCK::clear_commands()
{
    next_command_index = 0;
}

void COMM_BLOCK::set_infos(const std::string &data)
{
    infos_len = data.length();
    memcpy(infos_buf, data.data(), data.length() * sizeof(char));
}

std::string COMM_BLOCK::get_infos()
{
    return {infos_buf, infos_buf + infos_len};
}
