# Create our exectuable target
add_executable(stressTest
    ${CMAKE_CURRENT_SOURCE_DIR}/stressTest.cpp
)

# Set some target specific options
target_compile_features(stressTest PUBLIC cxx_std_17)
target_compile_options(stressTest
    PRIVATE
        $<$<OR:$<CXX_COMPILER_ID:Clang>,$<CXX_COMPILER_ID:GNU>>:
	        -pipe -march=native -msse4.1
            $<$<CONFIG:Debug>:-O0>>
        $<$<CXX_COMPILER_ID:MSVC>:
            /arch:SSE4.1
            $<$<CONFIG:Debug>:/Od /Wall /Zi>>
)
set_target_properties(stressTest
    PROPERTIES
        POSITION_INDEPENDENT_CODE ON
        DEBUG_POSTFIX ${CMAKE_DEBUG_POSTFIX}
)
