#!/usr/bin/env python
# -*- coding: utf-8 -*-

from conans import ConanFile, tools, CMake
import os
import tempfile


class Catch2Conan(ConanFile):
    name = "catch2"
    version = "2.3.0"
    description = "A modern, C++-native, header-only, framework for unit-tests, TDD and BDD"
    homepage = "https://github.com/catchorg/Catch2"
    url = "https://github.com/bincrafters/conan-catch"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "https://github.com/catchorg/Catch2/blob/master/LICENSE.txt"
    exports = ["LICENSE.md"]
    source_subfolder = "source_subfolder"
    header_name = "catch.hpp"
    generators = "cmake"
    exports_sources = "CMakeLists.txt"
    no_copy_source = True

    def source(self):
        source_url = "https://github.com/catchorg/Catch2"
        tools.download(
            "{0}/releases/download/v{1}/{2}".format(source_url, self.version, self.header_name),
            self.header_name
        )

        # All this to get the LICENSE.txt
        extracted_dir = "Catch2-" + self.version
        tools.get("{0}/archive/v{1}.tar.gz".format(source_url, self.version))
        os.rename(extracted_dir, self.source_subfolder)

    def package(self):
        install_dir = tempfile.mkdtemp()
        module_dir = os.path.join("lib", "cmake", "Catch2")
        cmake = CMake(self)
        cmake.definitions["CMAKE_INSTALL_PREFIX"] = install_dir
        cmake.configure()
        cmake.install()
        self.copy(pattern="LICENSE.txt", dst="licenses", src=self.source_subfolder)
        self.copy(pattern=self.header_name, dst=os.path.join("include", self.name))
        self.copy(pattern="*.cmake", dst=module_dir, src=os.path.join(install_dir, module_dir))
        tools.replace_in_file(os.path.join(self.package_folder, module_dir, "Catch2ConfigVersion.cmake"),
         "# if the installed or the using project don't have CMAKE_SIZEOF_VOID_P set, ignore it:", """if ("${CMAKE_GENERATOR}" MATCHES "(Win64|IA64)")
            return()
         endif()
         """)

    def package_id(self):
        self.info.header_only()
