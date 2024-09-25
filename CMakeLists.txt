cmake_minimum_required(VERSION 3.5)

# ===========================================================================
# Project Information
# ===========================================================================
project(
  tkdnd
  LANGUAGES C
  VERSION 0.14)

# ===========================================================================
# Locate Tcl/Tk
# ===========================================================================
if(MSVC)
  find_package(TCL QUIET)
  if(NOT TCL_FOUND)
    include(FetchContent)
    FetchContent_Declare(
      cpython-tcltk-win32
      GIT_REPOSITORY https://github.com/python/cpython-bin-deps
      GIT_TAG tcltk)
    FetchContent_MakeAvailable(cpython-tcltk-win32)

    if(cpython-tcltk-win32_POPULATED)
      if(MSVC_C_ARCHITECTURE_ID STREQUAL "ARM64")
        set(CMAKE_PREFIX_PATH
            ${CMAKE_PREFIX_PATH};${cpython-tcltk-win32_SOURCE_DIR}/arm64)
      elseif(MSVC_C_ARCHITECTURE_ID STREQUAL "x64")
        set(CMAKE_PREFIX_PATH
            ${CMAKE_PREFIX_PATH};${cpython-tcltk-win32_SOURCE_DIR}/amd64)
      elseif(MSVC_C_ARCHITECTURE_ID STREQUAL "X86")
        set(CMAKE_PREFIX_PATH
            ${CMAKE_PREFIX_PATH};${cpython-tcltk-win32_SOURCE_DIR}/win32)
      else()
        message(
          WARNING
            "No Tcl/Tk prebuilt binaries from CPython could be found for your platform (MSVC ${MSVC_C_ARCHITECTURE_ID})."
            "If the build fails, Ensure a MSVC-built Tcl/Tk is available on CMAKE_PREFIX_PATH."
        )
      endif()
    endif()
  endif()
endif()

find_package(TCL REQUIRED)
find_package(TclStub REQUIRED)

# ===========================================================================
# Target: tkdnd shared library
# ===========================================================================
#configure_file(tkdnd/generic/tkImgSVG.c
               ${CMAKE_CURRENT_BINARY_DIR}/tkImgSVG.c)
#add_library(tkdnd SHARED ${CMAKE_CURRENT_BINARY_DIR}/tkImgSVG.c)
target_link_libraries(tkdnd PRIVATE ${TCL_STUB_LIBRARY})
target_link_libraries(tkdnd PRIVATE ${TK_STUB_LIBRARY})

target_compile_definitions(tkdnd PRIVATE -DUSE_TCL_STUBS)
target_compile_definitions(tkdnd PRIVATE -DUSE_TK_STUBS)
target_compile_definitions(tkdnd PRIVATE -DPACKAGE_NAME="${CMAKE_PROJECT_NAME}")
target_compile_definitions(tkdnd
                           PRIVATE -DPACKAGE_VERSION="${CMAKE_PROJECT_VERSION}")
target_include_directories(tkdnd PRIVATE ${TCL_INCLUDE_PATH})
target_include_directories(tkdnd PRIVATE ${TK_INCLUDE_PATH})

block()
set(PACKAGE_NAME ${CMAKE_PROJECT_NAME})
set(PACKAGE_VERSION ${CMAKE_PROJECT_VERSION})
set(PKG_LIB_FILE
    ${CMAKE_SHARED_LIBRARY_PREFIX}tkdnd${CMAKE_SHARED_LIBRARY_SUFFIX})
configure_file(tkdnd/pkgIndex.tcl.in pkgIndex.tcl @ONLY)
endblock()

if(WIN32)
  install(TARGETS tkdnd RUNTIME DESTINATION tkdnd)
else()
  install(TARGETS tkdnd LIBRARY DESTINATION tkdnd)
endif()
install(FILES ${CMAKE_CURRENT_BINARY_DIR}/pkgIndex.tcl DESTINATION tkdnd)
