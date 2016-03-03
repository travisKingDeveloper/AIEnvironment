__author__ = 'travi_000'

from distutils.core import setup, Extension

# Fourth, write a setup.py script:

# the c++ extension module
extension_mod = Extension("hello", ["hellomodule.c", "hello.c"])

setup(name = "hello", ext_modules=[extension_mod])