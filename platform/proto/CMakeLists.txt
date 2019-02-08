cmake_minimum_required(VERSION 3.0.0)
project(comm)

set(CMAKE_BUILD_TYPE Debug)

set(CMAKE_CXX_STANDARD 17)

find_package(Protobuf REQUIRED)
include_directories(${Protobuf_INCLUDE_DIRS})
set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${PROJECT_BINARY_DIR}/lib)
protobuf_generate_cpp(PROTO_SRCS PROTO_HDRS comm.proto)
add_library(comm SHARED ${PROTO_SRCS} ${PROTO_HDRS})
target_link_libraries(comm ${Protobuf_LIBRARIES})