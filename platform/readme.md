# 平台简介

**编译时请开启C++17支持**
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
8. 平台将自动扫描**当前工作目录下**的所有命名合法的DLL文件，作为AI程序载入。

## Linux平台现状

1. Linux平台采用多进程进行选手AI管控。
2. 选手程序生成.so文件。
3. Linux平台下，选手进程与主进程都包含类Controller，可以被认为是C-S结构，两者之间通过共享内存通信。
4. client中的Controller会完成与选手AI的信息交互。
5. Server采用近似忙等待的方法检查client是否执行结束，以加快整体速度，具体而言，server每隔CHECK_INTERVAL(Controller中的常量，ms)检查一次client状况并决定是否继续，**这可能会影响同一核心下的AI程序，暂未做核心区分**
6. 平台将自动扫描**指定目录下**（通过平台程序的第一个参数传入）的所有命名合法的so文件，作为AI程序载入。

---
## 问题

1. 暂未设置玩家主动更新信息的API。
2. 需要逻辑提供比赛时信息以进一步测试。
3. 没有处理玩家死亡后的进程资源释放操作。
4. 计划取消is_jumping变量，仅采用turn作为当前传输内容是否为跳伞信息。
5. 对于每个不同的AI需要include不同包名的proto，这需要依赖自动构建程序。
6. 对于logic与platform中的所有proto文件，为避免出现问题，需要全部采用相同版本的protoc与libprotobuf进行处理，dev-platform中暂时采用3.7rc2版本，与master分支中不同，**请勿将dev-platform合并入master分支**。

## 多个玩家的动态链接库命名

1. 命名规则为： [lib]AI_${team}_${number}.dll/.so (linux下带有前缀lib)
2. ${team}为队伍信息，同一值的会被归入同一队伍，取值范围为[0,15]，
3. ${number}为队伍中的编号，取值范围为[0,3]
4. ${team}与${number}值只要不重复即可，无特殊要求，这两个值与AI实际执行顺序无关
5. 所有的AI文件需与platform位于同一目录下（暂时
6. 例: *AI_3_2.dll* 表示队伍3的2号玩家AI