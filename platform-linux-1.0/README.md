# FlatformDemo for TS20(AMD64, Linux)

* 平台版本: 1.0 for Linux
* Python3版本: 3.6.5 AMD64 for Linux
* C++版本: C++11及以上
* g++版本: 7.3.0
* Linux版本: 4.15.0-34-generic
* Ubuntu版本: 18.04

## Update 1.0 for Linux

1. 使用多进程技术重构了平台。

## 简介

* 本项目采用C\+\+与Python3混合编程的方式来实现平台功能，其中游戏逻辑完全放置在python3脚本文件(位于 当前工作目录/GameLogic.py)中，c\+\+部分提供数据的导入与导出，从而方便选手使用C\+\+编写AI。
* 本项目主要包含2个游戏逻辑相关类`CState`，`CDemands`，1个线程控制类`ThreadControl`，Python3交互相关的`PyCalling`，游戏API相关的`playerAPI`，游戏AI代码`player`与通用的头文件`Header.h`几部分组成。
* 目前用于测试的“游戏”主要逻辑为: 根据指令信息中的`cd`延后一定回合执行，根据指令信息中的`order`决定对`state`中的`test`进行操作如下：

|order|操作|
|-|-|
|1|`test`加1|
|2|`test`整除2|
|其他|无操作|

## 平台设计

### 主要思想

* 平台通过Python3的C API与逻辑进行交互，实现游戏的初始化与运行(结束暂时以回合上限代替)。
* 在回合循环中，平台将按照指定的并发量(期望的核心数)以子进程调用的方式顺序的执行所有玩家的AI函数，在同一次执行的AI函数中，当所有函数返回或超时，通过发送Linux信号`SIGSTOP`方式强制暂停线程的执行，进入下一批玩家AI函数的运行。当完成一轮循环后，再次发送Linux信号`SIGCONT`重启暂停的线程或创建新的线程(如果线程正常退出)。以此来实现大量玩家AI函数的(伪)并行与CPU时间片分配。
* 玩家调用playerAPI执行相关操作。

### 目前问题

* 对于不同玩家使用不同的PlayGame函数，目前设计中还没有对此作出处理，可以考虑将所有玩家AI文件并入同一工程，通过命名空间区分后在`ThreadFunc`中利用函数指针进行调用。
* 目前平台相关代码是直接暴露的，需要采用dll进行处理。
* 游戏逻辑相关Python3代码是直接暴露的，需要用.pyc文件替换。

## 类

### `CState`

用于与选手AI交互的类，存储从Python3脚本返回的游戏状态。

* 类成员常量

|成员常量|类型|属性|备注|
|-|-|-|-|
|`TURN_STRING`|`const char*`|`private`|存储解析回合数所使用的索引值|
|`SCORE_STRING`|`const char*`|`private`|存储解析游戏关键值所使用的索引值|

* 类成员变量

|成员变量|类型|属性|备注|
|-|-|-|-|
|`m_turn`|`int`|`private`|存储当前回合数|
|`m_test`|`int`|`private`|存储当前游戏关键参数|
|`m_pDict_state`|`PyObject*`|`private`|存储从Python3脚本返回的游戏状态字典|

* 类成员函数

|成员函数|参数|返回值|属性|备注|
|-|-|-|-|-|
|`GetTurn`|`void`|`int`|`const` `public`|_(player API)_获取当前回合数|
|`GetTest`|`void`|`int`|`const` `public`|_(player API)_获取当前游戏关键参数|
|`SetFromPyDict`|`PyObject*`|`void`|`public`|将Python3脚本返回的游戏状态导入类中|
|`ChangeToPyObject`|`void`|`PyObject*`|`const` `public`|将类中存储的游戏状态导出为`PyObject*`|

### `CDemands`

用于与选手AI交互的类，存储游戏指令。

* 结构体`DEMAND`，存储指令延后回合数`cd`与指令`order`

```cpp
struct DEMAND {
    int cd;
    int order;
};
```

* 类成员常量

|成员常量|类型|属性|备注|
|-|-|-|-|
|`CD_STRING`|`const char*`|`private`|存储解析指令延后回合数所使用的索引值|
|`ORDER_STRING`|`const char*`|`private`|存储解析指令所使用的索引值|

* 类成员变量

|成员变量|类型|属性|备注|
|-|-|-|-|
|`m_vDemands`|`vector<DEMAND>`|`private`|存储当前未被处理的指令信息|
|`m_pList_demands`|`PyObject*`|`private`|存储从Python3脚本返回的游戏剩余指令列表|

* 类成员函数

|成员函数|参数|返回值|属性|备注|
|-|-|-|-|-|
|`AppendDemand`|`const DEMAND&`|`void`|`private`|将指令信息加入`vector`与Python3列表|
|`SetFromPyList`|`PyObject*`|`void`|`public`|将Python3脚本返回的游戏剩余指令列表导入类中|
|`ChangeToPyObject`|`void`|`PyObject*`|`const` `public`|将类中存储的游戏剩余指令列表导出为`PyObject*`|
|`MergeDemands`|`const vector<DEMAND>[]` `unsigned int`|`void`|`public`|将指令信息向量数组中的所有指令合并到类中|

### `ThreadControl`

包装了线程控制相关代码，提供自定义并行核心数，目前只支持windows平台。

* **警告：该类不允许复制。**

* 枚举类型`PROCESS_STATE`， 用于标记线程状态。
* 结构体`PROCESS_INFO`，存储进程PID、状态以及与子进程通信的管道句柄。

```cpp
struct THREAD_INFO {
    pid_t pid = 0;
    PROCESS_STATE state = PROCESS_UNUSED;
    int sender[2];
    int receiver[2];
};
```

* 类成员变量

|成员变量|类型|属性|备注|
|-|-|-|-|
|`m_usedCoreNumber`|`long`|`private`|存储期望使用的CPU核心数|
|`m_totalCoreNumber`|`long`|`private`|存储CPU实际逻辑核心数|
|`m_processInfo`|`PROCESS_INFO[]`|`private`|存储子进程信息|
|`m_usedCpuID`|`long`|`private`|用于向子进程传递使用的CPU核心编号|
|`m_nowOffset`|`int`|`private`|用于加快`NotifyOneFinish`查找的临时量|
|`m_playerID`|`int`|`private`|用于向子进程传递其对于的玩家ID|
|`pState`|`CState*`|`private`|指向游戏状态导出类的指针|
|`pAllDemands`|`vector<DEMAND>*`|`private`|指向存储用户发出指令的向量数组的指针|
|`playerFunc`|`void (*)()`|`private`|存储要调用的AI函数指针|

* 类成员函数

|成员函数|参数|返回值|属性|备注|
|-|-|-|-|-|
|`ThreadControl`|`int` `CState` `std::vector<DEMAND>[], long`|无|`constructor` `public`|构造函数，第一个参数指定玩家数，第二个参数指定全局使用的`CState`，第三个参数指定存储当回合全部指令的向量，第四个参数为期望使用的CPU核心数(0为默认值，0与大于实际最大值均视为使用全部核心，使用其他合理的值时，将会**优先使用核心ID较大的CPU核心**)|
|`Run`|`void`|`void`|`public`|启动一回合的玩家AI调用|
|`NotifyOneFinish`|`pid_t`|`void`|`public`|用于通知pid对应的进程中断执行|
|`SendDemand`|`DEMAND`|`void`|`public`|用于子进程向父进程发送指令|
|`Register`|`int` `void(*)()`|`void`|`public`|用于注册回调函数|
|`RunPlayer`|`void`|`void`|`private`|用于使子进程不断循环调用AI函数|

### `PyCalling`

包装了将与Python3脚本交互的部分。

* 类成员常量

|成员常量|类型|属性|备注|
|-|-|-|-|
|`PYFUNCNAME_TO_STRING`|`const char*`|`private`|(_PLATFORM_DEBUG_)用于获取log内容的Python3函数名|
|`FILENAME_LOG`|`const char*`|`private`|(_PLATFORM_DEBUG_)log文件名|

* 类成员变量

|成员变量|类型|属性|备注|
|-|-|-|-|
|`file`|`wfstream`|`private`|(_PLATFORM_DEBUG_)用于重定向`wclog`到`FILENAME_LOG`指定的log文件|
|`backup`|`wstreambuf*`|`private`|(_PLATFORM_DEBUG_)暂存`wclog`的缓冲区，用于后续恢复|
|`pFunc_change_to_string`|`PyObject*`|`private`|(_PLATFORM_DEBUG_)用于存储Python3脚本中将游戏状况转换为字符串的函数|
|`buffer`|`wchar_t[MAX_STRING]`|`private`|(_PLATFORM_DEBUG_)log字符串暂存|
|`pFunc_game_main`|`PyObject*`|`private`|存储Python3脚本中游戏主循环函数|
|`pState`|`CState*`|`private`|指向游戏状态导出类的指针|
|`pDemands`|`CDemands*`|`private`|指向游戏指令导出类的指针|
|`pAllDemands`|`vector<DEMAND>*`|`private`|指向存储用户发出指令的向量数组的指针|
|`playerCount`|`unsigned int`|`private`|游戏玩家数|

* 类成员函数

|成员函数|备注|
|-|-|
|`PyCalling`|参数从左到右依次为调用的Python3脚本模块名，游戏初始化函数名，游戏处理函数名，游戏状态导出类，游戏指令导出类，函数将完成所有必要的准备工作，包括获取函数对象与游戏状态、指令相关初始化工作|
|`DoLoop`|将玩家指令导入到Python3脚本中计算出下回合状态与指令，并更新导出类|

* 常量

|常量|类型|备注|
|-|-|-|
|`MAX_STRING`|`const unsigned int`|(_PLATFORM_DEBUG_)输出log时单行最大长度|

## 其他模块

### `playerAPI`

提供给玩家使用的游戏接口，目前只有一个指令发送函数。

```cpp
void SendDemand(int cd, int order);
```

函数传入参数从左向右为调用方ID，指令延迟回合数`cd`与指令`order`，表示发送该指令，指令调用者ID由`ThreadControl`检测，指令合法性由Python3脚本进行处理。

### `player`

游戏AI，其中的`void PlayGame()`作为AI主函数将被不断调用。

### `Header.h`

* 宏

|宏|备注|
|-|-|
|`PLATFORM_DEBUG`|控制平台**Debug**相关代码，目前主要功能为输出每回合log|
|`CHEAT_OUTPUT`| 控制是否在`cerr`流中输出使用非法ID调用playerAPI的实际玩家ID|

* 常量

|常量名|类型|备注|
|-|-|-|
|`MAX_PLAYER`|`const int`|支持的最大玩家数|
|`TIMEOUT`|`const int`|回合时长(单位:ms)|
|`MAX_TURN`|`const int`|最大回合数|
