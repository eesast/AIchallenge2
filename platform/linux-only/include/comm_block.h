#ifndef COMM_BLOCK_H
#define COMM_BLOCK_H

#include <atomic>
#include <memory.h>
#include <string>
#include <vector>

const int MAX_INFOS_LEN = 100000;
const int MAX_COMMAND_LEN = 10000;
const int MAX_COMMAND_NUM = 50;

struct COMM_BLOCK
{
    std::atomic_flag infos_flag, commands_flag;
    bool is_init = false;
    int frame; //for checking if it is the lastest
    int infos_len;
    char infos_buf[MAX_INFOS_LEN];
    int next_command_index;
    int commands_len[MAX_COMMAND_NUM];
    char commands_buf[MAX_COMMAND_NUM][MAX_COMMAND_LEN];

    void init();
    void set_inited();
    void lock_infos();
    bool try_lock_infos(); //return true on success
    void unlock_infos();
    void lock_commands();
    bool try_lock_commands(); //return true on success
    void unlock_commands();
    bool add_command(const std::string &data); //return true on success, do not check if len>MAX_COMMAND_LEN
    std::vector<std::string> get_commands();   //get all commands as a vector
    void clear_commands();
    void set_infos(const std::string &data);
    std::string get_infos();
};

#endif // !COMM_BLOCK_H#define COMM_BLOCK_H
