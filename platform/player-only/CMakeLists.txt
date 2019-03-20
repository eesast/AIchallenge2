cmake_minimum_required(VERSION 3.0.0)
project(AI)
set(CMAKE_MAJOR_VERSION 0)
set(CMAKE_MINOR_VERSION 1)

set(CMAKE_CXX_STANDARD 17)

include_directories(${PROJECT_SOURCE_DIR}/include)
include_directories(${PROJECT_BINARY_DIR}/../proto/)
aux_source_directory(${PROJECT_SOURCE_DIR}/src DIR_SRC)
aux_source_directory(${PROJECT_SOURCE_DIR}/player_only/src DIR_SRC)
find_package(Protobuf REQUIRED)
include_directories(${Protobuf_INCLUDE_DIRS})


IF(WIN32)

# set(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} /Od /MDd /D "_DEBUG" /ZI /GZ /Gm")
# set(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} /O2 /MD /D "NDEBUG" /GF")

ELSEIF(UNIX)

set(CMAKE_CXX_FLAGS_DEBUG "$ENV{CXXFLAGS} -o0 -Wall -Wextra -g -ggdb")
set(CMAKE_CXX_FLAGS_RELEASE "$ENV{CXXFLAGS} -o3 -Wall -Wextra")

ENDIF()

add_library(AI SHARED ${DIR_SRC})
# target_link_libraries(AI ${Protobuf_LIBRARIES})
target_link_libraries(AI comm)