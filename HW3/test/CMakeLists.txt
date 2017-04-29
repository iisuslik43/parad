cmake_minimum_required(VERSION 2.8)
project(test)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -O0 -Wall -Werror -std=c++11 -pedantic -Wextra -lgtest_main -lgtest -lpthread")
include_directories(../include/)

set(SOURCE_FILES test.cpp ../src/huffman.cpp ../src/options.cpp)
add_executable(test ${SOURCE_FILES})
