cmake_minimum_required(VERSION 3.22.1)

project(numerical_integration)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)


cmake_minimum_required(VERSION 3.10)

# Set C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

# Add compile options for GCC/Clang
if(CMAKE_CXX_COMPILER_ID MATCHES "GNU|Clang")
    add_compile_options(
        -Wall
        -Wextra
        -Wpedantic
        -Wcast-align
        -Wcast-qual
        -Wconversion
        -Wenum-compare
        -Wfloat-equal
        -Wnon-virtual-dtor
        -Woverloaded-virtual
        -Wredundant-decls
        -Wsign-conversion
        -Wsign-promo
        -Weffc++
        -Werror
        -Wunused
        -Wshadow
        -Wold-style-cast
        -Wpointer-arith
        -Winit-self
        -Wswitch-default
        -Wmissing-include-dirs
        -Wuninitialized
        -Wmissing-noreturn
        -Wno-unused-parameter # Consider using this to suppress warnings for unused parameters
    )
endif()

# Add compile options for MSVC
if(MSVC)
    add_compile_options(
        /W4
        /WX
        /analyze
        /permissive-
        /Za
        /wd4251 # Disable a specific warning; example: C4251 for dll-interface
        /wd4189 # Disable a specific warning; example: C4189 for local variable is initialized but not referenced
        /D_CRT_SECURE_NO_WARNINGS # Suppress warnings about "unsafe" C functions
    )
endif()

add_subdirectory(src)


