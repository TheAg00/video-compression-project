cmake_minimum_required(VERSION 3.10)
project(colorization)


include_directories(include)


find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} )
# target_link_libraries( DisplayImage ${OpenCV_LIBS} )

# Globbing all source files
file(GLOB SOURCES "src/*.cpp")

# Add an executable target for your project
add_executable(colorization ${SOURCES})

target_link_libraries( colorization ${OpenCV_LIBS} )
