cmake_minimum_required(VERSION 3.28)
project(signal C)

set(CMAKE_C_STANDARD 23)
set(CMAKE_OSX_SYSROOT "")

set(FLAG_FILE "${CMAKE_CURRENT_SOURCE_DIR}/flag.txt")

if (EXISTS ${FLAG_FILE})
    file(READ ${FLAG_FILE} FLAG)
    string(LENGTH ${FLAG} FLAG_LENGTH)
    string(STRIP ${FLAG} FLAG)
    foreach(INDEX RANGE 0 ${FLAG_LENGTH})
        string(SUBSTRING ${FLAG} ${INDEX} 1 CHAR)
        add_compile_definitions(FLAG_${INDEX}='${CHAR}')
    endforeach()
endif()

add_compile_definitions(FLAG_FILE="${FLAG_FILE}")

add_executable(signal main.c)
