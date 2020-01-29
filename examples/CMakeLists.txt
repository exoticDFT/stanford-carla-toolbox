# Create our exectuable target
add_executable(test
    ${CMAKE_CURRENT_SOURCE_DIR}/main.cpp
)

# Set some target specific options
target_compile_features(test PUBLIC cxx_std_17)
target_compile_options(test
    PRIVATE
        $<$<OR:$<CXX_COMPILER_ID:Clang>,$<CXX_COMPILER_ID:GNU>>:
	        -pipe -march=native -msse4.1
            $<$<CONFIG:Debug>:-O0>>
        $<$<CXX_COMPILER_ID:MSVC>:
            /arch:SSE4.1
            $<$<CONFIG:Debug>:/Od /Wall /Zi>>
    PUBLIC
        -DJULIA_ENABLE_THREADING=1
)
set_target_properties(test
    PROPERTIES
        POSITION_INDEPENDENT_CODE ON
        DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX}
)
set(THREADS_PREFER_PTHREAD_FLAG ON)

# Find external packages
find_package(Julia REQUIRED)
find_package(Threads REQUIRED)

# Link packages to our target
target_include_directories(test
    PUBLIC
        $<BUILD_INTERFACE:${Julia_INCLUDE_DIRS}>
)
target_link_libraries(test
    PUBLIC
        ${Julia_LIBRARY}
       Threads::Threads
)
