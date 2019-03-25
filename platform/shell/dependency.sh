#!/bin/bash
if [ $(id -u) -ne 0 ]
then
    echo "sudo needed"
    exit 1
fi

echo "install gcc/g++/python3"
apt update
apt install g++-8 gcc-8 python3 python3-pip autoconf automake libtool curl make unzip
ln -sf /usr/bin/g++-8 /usr/bin/g++
ln -sf /usr/bin/gcc-8 /usr/bin/gcc

echo "install protouf3.6.1"
wget https://github.com/protocolbuffers/protobuf/releases/download/v3.6.1/protobuf-all-3.6.1.tar.gz
tar -zxf protobuf-all-3.6.1.tar.gz
cd ./protobuf-3.6.1
./autogen.sh
./configure
make
if [ $? -ne 0 ]
then
    echo "make failed"
    exit 1
fi
make check
if [ $? -ne 0 ]
then
    echo "make test failed"
    exit 1
fi
make install
ldconfig

cd ./python
python3 setup.py build --cpp_implementation
python3 setup.py test --cpp_implementation
python3 setup.py install --cpp_implementation
cd ../../

echo "install cmake"
wget https://github.com/Kitware/CMake/releases/download/v3.14.0/cmake-3.14.0-Linux-x86_64.tar.gz
tar -zxf cmake-3.14.0-Linux-x86_64.tar.gz
cd ./cmake-3.14.0-Linux-x86_64
mv ./bin/* /usr/local/bin
mv ./man/* /usr/local/man
mv ./share/* /usr/local/share
mv ./doc /usr/local