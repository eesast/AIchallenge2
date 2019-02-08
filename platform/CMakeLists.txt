cmake_minimum_required(VERSION 3.0.0)
project(platform)
set(CMAKE_MAJOR_VERSION 0)
set(CMAKE_MINOR_VERSION 1)

set(CMAKE_BUILD_TYPE Debug)

set(CMAKE_CXX_STANDARD 17)

add_subdirectory(${PROJECT_SOURCE_DIR}/player-only/)
add_subdirectory(${PROJECT_SOURCE_DIR}/proto/)

IF(WIN32)
find_package (Python3 COMPONENTS Interpreter Development)
ELSEIF(UNIX)
find_package(PythonLibs 3.6 REQUIRED)
ENDIF()

include_directories(${PROJECT_SOURCE_DIR}/include)
aux_source_directory(${PROJECT_SOURCE_DIR}/src DIR_SRC)

IF(WIN32)
SET(EXECUTABLE_OUTPUT_PATH ${PROJECT_SOURCE_DIR}/win-only/build)

include_directories(${PROJECT_SOURCE_DIR}/win-only/include)
aux_source_directory(${PROJECT_SOURCE_DIR}/win-only/src DIR_SRC)

ELSEIF(UNIX)

set(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -o0 -Wall -Wextra -g -ggdb")
set(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -o3 -Wall -Wextra")
include_directories(${PROJECT_SOURCE_DIR}/linux-only/include)
aux_source_directory(${PROJECT_SOURCE_DIR}/linux-only/src DIR_SRC)

ENDIF()

# protobuf
find_package(Protobuf REQUIRED)
include_directories(${Protobuf_INCLUDE_DIRS})
include_directories(${PROJECT_BINARY_DIR}/proto/)

include_directories(${Python3_INCLUDE_DIRS})
add_executable(platform ${DIR_SRC})
target_link_libraries(platform ${Python3_LIBRARIES})

IF(UNIX)
target_link_libraries(platform libdl.so)
target_link_libraries(platform stdc++fs)
ENDIF()

target_link_libraries(platform comm)