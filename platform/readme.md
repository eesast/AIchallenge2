# 平台简介
---
### 文件夹

1. include: 存放两个平台共用的头文件
2. src: 存放两个平台共用的源文件
3. win-only: 存放用于Win平台的线程控制文件与主程序
4. linux-only: 存放用于linux平台的进程控制文件与主程序
5. player-only: 目前存放玩家AI测试程序的代码
6. proto: 存放通信过程使用的proto文件
---
## 平台现状

* Win与Linux均采用protocol buffer作为序列化工具，两个平台上均完成了大部分工作。
* 目前可以正常地向AI程序发送航线信息，AI程序返回跳伞坐标
---
## Win平台现状

1. Win平台采用多线程进行选手AI管控。
2. Win平台将选手程序生成为DLL文件，由主程序进行显式调用来访问AI程序。
3. Win平台目前也采用CMake进行工程创建，需注意生成的目标工程必须与python的位数相对应(X86 X64)，否则会出现无法编译的问题。
4. 若Win平台生成为Visual Studio工程，需将python的include目录与libs目录添加至工程包含目录与引用目录中。
5. 为方便起见，建议调整选手AI的dll生成目录与平台程序一致。
6. 选手AI通过给定的API进行操作，API中会调用序列化工具并将指令传递至Controller进行处理。
7. Controller也通过相应DLL中相应的接口进行序列化后的信息传递。

## Linux平台现状

1. Linux平台采用多进程进行选手AI管控。
2. 选手程序生成.so文件。
3. Linux平台下，选手进程与主进程都包含类Controller，可以被认为是C-S结构，两者之间通过共享内存通信。
4. client中的Controller会完成与选手AI的信息交互。
5. Server采用近似忙等待的方法检查client是否执行结束，以加快整体速度，具体而言，server每隔CHECK_INTERVAL(Controller中的常量，ms)检查一次client状况并决定是否继续，**这可能会影响同一核心下的AI程序，暂未做核心区分**

---
## 问题

1. 还没有解决多个玩家的情况，计划根据动态链接库的名称进行载入以及队伍的区分。
2. 缺少队伍信息。
3. 暂未设置玩家主动更新信息的API。
4. 需要逻辑提供比赛时信息以进一步测试。
5. 没有处理玩家死亡后的进程资源释放操作。
6. 计划取消is_jumping变量，仅采用turn作为当前传输内容是否为跳伞信息。
7. Win平台没有跟进Linux上最新的修改。

### Important

Linux上修改了Controller中send/receive系列函数名，使之更容易理解，**暂未同步到Win**
