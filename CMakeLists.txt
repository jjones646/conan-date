project( ConanDate )
cmake_minimum_required( VERSION 3.0 )

set(DATE_TZDATA_DIR "" CACHE STRING "Location of tzdata.YYYv.tar.gz")


add_definitions("-DINSTALL=\"${DATE_TZDATA_DIR}\"")

include( conanbuildinfo.cmake )
conan_basic_setup( TARGETS )
add_subdirectory( date )