此处给出用于回放文件的`protobuf`的相关文件，包括`proto`文件和转换后的python脚本。

### 文件列表

`logic.proto`:文件规定了所有要写入回放文件的数据内容。

`logic_pb2.py`:由`proto`文件转化得到的脚本，提供相关数据类型和接口。

### 使用说明

##### 格式

回放文件保存为`时间.pb`的文件名，其中时间取自python的`strftime("%Y%m%d_%H'%M'%S")`，`pb`是playback的简写。每个message写入回放文件时先写入一个`int`(4字节，小端对齐)表示该对象的长度，接下来才是整个message转换为二进制的数据。

##### 写入

在生成的回放文件中，最前面会写入一个`InitialInfo`，然后每帧写入一个`Frame`。