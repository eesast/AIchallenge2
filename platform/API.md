# 第二届人工智能挑战赛——枪林弹雨
# 平台使用说明与开发注意事项
版本长期发布链接[清华云盘](https://cloud.tsinghua.edu.cn/d/513cdc8459f742e0980a/)
#### 版本 v1.0
------
### Update v1.0
1. 正式版发布
2. 修复了跳伞坐标值为1000时的问题
3. **调整了回放文件的格式以适应第二版界面（Beta）**

### Update v1.0rc3 Patch6

1. 修复治疗问题

### Update v1.0rc3 Patch5

1. 信号兵可以正确地发送无线电（每回合上限5条）

### Update v1.0rc3 Patch4
1. 修复了透视问题

### Update v1.0rc3 Patch3
1. 新增声音角度
2. 逻辑修正部分bug
3. 界面alpha版（使用需谨慎）
4. 更新了规则手册

### Update v1.0rc3 Patch2
修复以下bug：
1. 物品刷新可能出现在非法区域
2. 墙的坐标重叠
3. 没有医疗兵导致的彻底死亡没有给击杀者积分
4. 瞬间跳伞
5. 尸体阻挡子弹
6. 子弹飞行可能有延时
7. 友军攻击

### Update v1.0rc3

0. **调整了PoisonInfo中move_flag的作用**
1. 修改了地图，删除了部分矮墙，将部分“线”状墙修正为矩形。
2. 修正了dll文件判断逻辑在特殊情况下错误bug。
3. 逻辑修复了部分bugs。
4. 逻辑加入了对于拾取物品bug的log信息，便于差错，希望选手在看到相应输出信息及时保存并告知开发组。
5. 医疗兵最大救治距离包含在常量`PICKUP_DISTANCE`中。
6. 平台能够合理应对选手代码未进行跳伞的情况并返回分数。
7. 修改了毒圈的缩圈逻辑，圈中心不会出现在不合理的位置。
8. 调整了拳头的攻击力。

------
### Update v1.0rc2
1. 完善了API文档。
2. 更改了debug信息的选择方式，不需要自行替换文件了。
3. 在constant.h中新增了一些信息（飞机速度、跳伞速度、最大拾取距离、防具减伤系数）。
4. 修复了已知的bug。
5. 加入了所有必须的玩家手册。
6. 加入了转身/头不动的API（详见move部分）。
7. 注释了api.cpp中的所有非报错输出，有需要可以自行添加。
8. **constant.h中地形部分取消了DOT**。
9. 加入了logic部分随机数种子的设置，便于debug。
10. 加入了reduce常量的介绍。
11. 加入了对于望远镜的介绍。

---

## 平台简介
* 平台采用伪实时设计，在逻辑返回的同一时刻信息的基础上，所有AI并行运行（并行数受使用的逻辑核心数限制），多个批次之间串行运行，保证所有的AI运行相近的时间，如果在时间限制内函数没有返回，AI将被挂起，等待下一次执行。每一帧后，平台会收集AI调用API的数据反馈给逻辑更新场景信息，并反馈给平台，当AI调用update系列函数后更新信息。

------

## 平台使用说明
压缩包`TS20Platform_Win_X86_v1.0.zip`为运行平台
1. AI目录用于存放玩家AI代码生成的.dll文件，要求将.dll文件改名为`AI_${team}_${number}.dll`，其中`${team}`为队伍信息，同一值的会被归入同一队伍，取值范围为`[0,15]`，`${number}`为队伍中的编号，取值范围为`[0,3]`(例: `AI_3_2.dll`表示队伍3的2号玩家AI)。
2. `log`目录存放平台运行时自动生成的信息，用于开发组debug工作。
3. `playback`目录存放回放文件以及比赛结果(如果比赛完成)。
4. 以上3个文件夹内容可以随意删除。
5. 其余文件是平台运行的环境，不可随意更改。
6. 如果启动过程中出现缺少`MSVCP140.dll`错误，请安装提供的`vcruntime/vc_redist.x86.exe`。
7. 平台运行后会提示键入每次运行的AI程序数量，键入内容为数字，为保证不同AI同时运行时对资源占用的公平性，平台会限制每次同时运行的AI数小于等于本机逻辑核心数，并且将不同的AI分配到不同的逻辑核心上。键入0代表使用所有逻辑核心，键入其他大于0的数字代表使用相应数量的逻辑核心，超过实际核心数则会被设置为本机实际最大逻辑核心数。
8. 不要使用两个逻辑核心（或单核处理器）运行3个AI程序，达成此条件可能会触发<strong>“巨硬的愤怒”</strong>。
9. 场上至少有2支队伍，否则游戏会立即结束（因为吃鸡了）。
10. 平台运行后会提示键入debug等级，输入1平台会输出大量可用于调试的信息，例如AI发送的指令、位置、视野等等输入其他数字平台只输出少量错误提示信息，。
11. 平台运行后会提示键入seed（随机数种子），输入0（或小于0）表示不设置随机数种子，输入大于0的数表示将随机数种子设置为该值。

---
## AI编写说明
压缩包`player-project.zip`为供选手开发使用的工程（只提供vs2017）
1. 如果出现初次编译就大量错误，可能需要修改工程中`Windows SDK`至现有版本，具体修改方法如下：<br>解决方案管理器中AI项目(右键)->属性->Windows SDK版本(修改为本机已有版本)。
2. `player.cpp`文件中已经自带一个~~智障~~机器人AI，玩家可以在此基础上修改或重写。
3. 其他文件不可修改。
4. 工程将生成`AI.dll`文件，重命名移动到平台指定目录即可。
5. **务必采用Release X86模式生成AI.dll**，否则会报错。
6. 如有需要，可以通过清华云盘下载`Visual Studio 2017`离线安装包[vs_2017](https://cloud.tsinghua.edu.cn/f/711abb58c40946d7aed4/?dl=1)。

---
## AI工程架构
```
player-project
|----- api.h        API头文件
|----- api.cpp      API源文件
|----- base.h       DLL导出函数
|----- base.cpp     DLL导出函数
|----- comm.pb.h    通信协议(Google Protobuf)
|----- constant.h   常量表
|----- data.h       数据结构
|----- player.cpp   玩家AI（唯一可修改与提交的部分）
|----- comm         通信协议库
|----- google       通信协议头文件
```
---
## 数据结构
### constant.h
```cpp
struct XYPosition   //表示绝对位置的直角坐标
{
    double x, y;
};
```
```cpp
struct PolarPosition //表示相对位置的极坐标
{
    double distance;    //距离
    double angle;       //角度
};
```
### data.h
```cpp
struct Item   //物品信息
{
	int item_ID;    //物品的ID
	ITEM type;      //物品的种类（参见constant.h中的ITEM枚举）
	PolarPosition polar_pos;    //物品的坐标（如果在地上）
	int durability;             //物品的使用耐久
};
```
```cpp
struct PoisonInfo   //电圈信息
{
    XYPosition current_center;      //电圈当前中心
    XYPosition next_center;         //下一电圈中心
    double current_radius;          //电圈当前半径
    double next_radius;             //下一电圈起始半径
    int rest_frames;                //距离下一个状态的帧数，参见下方注释
    // if move_flag is 3, the poison ring won't move(has become a node)
    // if move_flag is 2, rest_frames for (wait->move)
    // if move_flag is 1, rest_frames for (move->wait)
    // if move_flag is 0, rest_frames for (no circle->the 1st circle)
    int move_flag;
    // 0 表示缩圈还没有开始（第一个圈还没出现）
    // 1 正在缩圈
    // 2 正在等待下一次缩圈
    // 3 圈已经缩成一个点
};
```
```cpp
struct SelfInfo     //本AI信息
{
    double hp;          //当前血量
    double hp_limit;    //血量上限
    double move_angle;  //当前行进的绝对角度
    double view_angle;  //当前视线的绝对角度
    double move_speed;  //当前移动速度
    VOCATION vocation;  //职业
    STATUS status;      //当前状态（参看STATUS枚举）
    int move_cd;        //距本次移动结束的帧数
    int attack_cd;      //距可发起下一次攻击的帧数
    XYPosition xy_pos;  //本AI在地图上的XY坐标
    double view_width;  //当前视角
    double view_distance;   //视野（与视角一起形成一个扇形为可见区域）
    std::vector<Item> bag;  //本AI拥有的道具（枪、防具等等）
    //注：防具自动装备
};
```
```cpp
struct OtherInfo        //视野中其他AI的信息
{
    int player_ID;      //该AI的ID
    STATUS status;      //该AI的状态
    double move_angle;  //该AI的行进的绝对角度
    double view_angle;  //该AI的视线的绝对角度
    double move_speed;  //该AI的移动速度
    VOCATION vocation;  //该AI的职业
    PolarPosition polar_pos;    //该AI的相对于自身的极坐标相对位置
};
```
```cpp
struct Sound            //无线电与声音信息
{
    int sender;         //无线电发送者ID或环境声音(为-1时)
    int delay;          //延时，用于预估距离
    SOUND type;         //声音类型（参见SOUND枚举）
    int32_t parameter;  //无线电内容
    int angle;			//声音来源的相对角度（无线电为0）
};
```
```cpp
struct PlayerInfo       //所有信息的聚合
{
    int player_ID;      //本AI的ID
    SelfInfo self;      //自身信息
    std::vector<int> landform_IDs;  //视野中的地形的ID
    std::vector<Item> items;        //视野中的物品（在地上的）
    std::vector<OtherInfo> others;  //视野中的其他AI（自行辨别敌友）
    std::vector<Sound> sounds;      //听到的声音与收到的无线电
    PoisonInfo poison;              //电圈信息
};
```
### player.cpp
```cpp
extern XYPosition start_pos, over_pos;  //航线的起点与终点的XY坐标
extern std::vector<int> teammates;      //队友ID
extern int frame;                       //当前帧数（从0开始计数）
extern PlayerInfo info;                 //所有信息的聚合
```
---
## 常量表
* **推荐对照提供的data.pdf阅读**
* **结构体数组建议视为表格阅读**
* `AIRPLANE_SPEED`:飞机速度
* `JUMPING_SPEED`:跳伞过程中人的移动速度
* `PICKUP_DISTANCE`:拾取物品的最远距离、医疗兵最大救治距离
* `NOMOVE`:表示不进行移动的宏
```cpp
enum STATUS //状态
{
    RELAX = 0,  	//无动作
    ON_PLANE = 1,   //在飞机上
    JUMPING = 2,    //正在跳伞   
    MOVING = 3,     //移动中（与move_cd相关联）
    SHOOTING = 4,   //射击中（与attack_cd相关联）
    PICKUP = 5,     //正在捡东西
    MOVING_SHOOTING = 6,    //正在移动中射击
    DEAD = 7,       //假死（可被医疗兵救活）
    REAL_DEAD = 8   //真死
};
```
```cpp
enum VOCATION		//职业
{
    MEDIC = 0,      //医疗兵
    SIGNALMAN = 1,  //通信兵
    HACK = 2,       //黑客
    SNIPER = 3,     //狙击手
    VOCATION_SZ = 4,    //便于遍历（下同）
};
```
```cpp
struct vocation_property	//职业属性
{
    int number;			//职业的编号（没用，看枚举就好，下同）
    double hp;			//职业血量上限
    double distance;	//视距
    double angle;		//视角
    double radius;		//人物半径
    double move;		//移动因数（快慢）
    double skill;		//技能因数
};
```
* `VOCATION_DATA`:职业信息表格（**建议采用VOCATION_DATA[枚举名].xxx访问，下同**）
```cpp
enum ITEM_TYPE		//物品类型
{
    WEAPON = 0,		//武器
    ARMOR = 1,		//防具
    GOODS = 2,		//道具
    ITEM_TYPE_SZ = 3,
};
```
```cpp
enum ITEM_MODE		//物品使用类型
{
    PORTABLE = 0,		//携带即生效
    SPENDABLE = 1,		//消耗品(shoot使用)
    TRIGGERED = 2,		//拾取时生效(pickup触发)
    ITEM_MODE_SZ = 3,	//无模式
};
```
* `ITEM`:道具种类枚举（太长了，自行参照`data.pdf`）
```cpp
struct item_property	//物品属性
{
    ITEM_TYPE type;		//类型
    int number;			//略
    int durability;		//耐久度
    ITEM_MODE mode;		//使用类型
    int range;			//（武器的）射程
    int cd;				//两次使用间隔帧数
    int damage;			//（武器的）伤害
    double reduce;			//防具减伤系数
    double param;//参数（武器-散射角 药品-负值-回血量 望远镜-现视野/初始视野 初始视角/现视角）
    int occur;			//出现概率因数
};
```
* `ITEM_DATA`:道具信息表格
```cpp
enum SOUND			//声音、无线电
{
    RADIO_VOICE = 0,	//无线电
    FOOTSTEP_SOUND = 1,	//脚步声
    GUN_SOUND = 2,		//枪声
    BOOM_SOUND = 3,		//炸弹声（暂无）
    SOUND_SZ = 4,
};
```
```cpp
struct sound_property	//声音、无线电属性
{
    int number;			//略
    double speed;		//每帧传播距离
    double distance;	//最远传播距离
};
```
* `SOUND_DATA`:声音/无线电信息表格
```cpp
enum BLOCK_SHAPE	//物体形状
{
    CIRCLE = 0,		//圆，提供圆心坐标与半径
    RECTANGLE = 1,	//矩形，提供左上角和右下角的坐标
    BLOCK_SHAPE_SZ = 2,
};
```
* `BLOCK_TYPE`:地形中的物体枚举（略）
```cpp
struct block {		//物体属性
    BLOCK_SHAPE shape;		//形状
    BLOCK_TYPE type;		//类型
    int x0, y0, r, x1, y1;	//相关坐标
    //when shape == RECTANGLE, (x0, y0) and (x1, y1) are used (left-top and right-bottom)
    //when shape == CIRCLE, (x0, y0) and r are used (center and radius)
};
```
* `AREA`:地形块枚举
* `AREA_DATA`:每一个地形块的组成方式（每个地形块100×100范围上的物体，位置均为相对位置）
* `MAP_SZ`:数组`MAP`的大小
* `MAP`:描述地图的构成（由10×10个地形块构成，排序为先x轴从小到大，再y轴从小到大，整个地图为1000×1000）
```cpp
struct circle_property	//电圈属性
{
    int items;			//刷新的物品数
    int delay;			//延时（只对第一个圈有意义，在200帧前，不出现电圈）
    int wait;			//电圈移动前的静止时间
    int move;			//移动的时间
    double damage;		//每帧对电圈内的造成的伤害
    double shrink;		//电圈半径收缩的比例
};
```
* `CIRCLE_SZ`:数组`CIRCLE_DATA`大小
* `CIRCLE_DATA`:电圈数据表格

---
## 关于地形的解释
* 地形的描述方法分为三个层级：地图（1000×1000）->地形块（每个100×100）->物体（树、房子...）。
* 地形块数据`AREA_DATA`中提供的是物体在地形块的100×100区域内的坐标，具体到地图上需要根据地形块的位置加上适当的偏置。
* 已有API（`get_landform`）可以实现从地形ID到物体绝对坐标的转化，如果需要自行处理地图，可以参考其中的代码。

---
## API
* 所有的API均在命名空间ts20下，以避免与标准库冲突
```cpp
//跳伞，只能在第0帧时使用，未调用的AI将被平台自动关闭
//参数：选择的职业与跳伞地点的XY坐标
void parachute(VOCATION role, XYPosition landing_points);
```
```cpp
//射击与使用道具
//参数：使用的道具/枪的枚举，相对角度，特殊参数（医疗兵使用药品的对象ID）
void shoot(ITEM item_type, double shoot_angle, int parameter =-1);
```
```cpp
//移动
//参数：前进方向与视角的相对角度（相对于当前视角）
//parameter == NOMOVE(0)时不移动，只调整角度
void move(double move_angle, double view_angle, int parameter = -1);
```
```cpp
//拾取
//参数：地上的物品ID，需要在一定范围内才能成功（PICKUP_DISTANCE）
void pickup(int target_ID, int parameter = -1);
```
```cpp
//发送无线电
//参数：接收者ID，信息（只能使用低29位）
void radio(int target_ID, int msg);
```
```cpp
//更新信息（player.cpp中的info与frame）
//阻塞式，如果没有新的信息到来就一直等待
//play_game函数中至少出现一次，否则无法收到最新数据
void update_info();
```
```cpp
//更新信息，同上
//非阻塞式，如果没有新信息就直接返回false
//否则解析新信息并返回true
bool try_update_info();
```
```cpp
//将地形ID转换为具体物体的结构体
//返回的block中的结构中的位置信息是绝对位置
//如果解析错误会返回{ BLOCK_SHAPE_SZ,BLOCK_TYPE_SZ,0,0,0,0,0 }
block get_landform(int landform_ID);
```
---

## 名词解释
* 帧数:每个AI每次执行一定时间，称为1帧，相当于整个连续时间的离散化表示
* 绝对位置:在整个地图上的XY坐标
* 相对位置:极坐标，以当前人的视野为极坐标角度0值处，逆时针方向增大，角度取值范围在0~360（换算关系与一般的直角坐标到极坐标的换算一致）
* 绝对角度:地图对应的XY直角坐标系X轴正向为0，逆时针方向增大，取值在0~360

---

---
## 附
1. 有任何问题请联系开发组解决

最后更新于2019年3月30日
