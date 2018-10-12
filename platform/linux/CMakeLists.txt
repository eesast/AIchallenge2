cmake_minimum_required(VERSION 3.0.0)
project(platform-linux)
set(CMAKE_MAJOR_VERSION 0)
set(CMAKE_MINOR_VERSION 1)
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -o0 -Wall -Wextra -g -ggdb")
set(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -o3 -Wall -Wextra")

find_package(PythonLibs 3 REQUIRED)

include_directories(${PYTHON_INCLUDE_DIRS})
include_directories(./include)
aux_source_directory(./src DIR_SRC)


add_executable(platform-linux ${DIR_SRC})
target_link_libraries(platform-linux ${PYTHON_LIBRARIES})

