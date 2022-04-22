#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 09:23:16 2021

Test c code running on python.

@author: mate
"""

#Imports - Use ctypes
import time
import ctypes
import pathlib

#Use test_lib.so
if __name__ == "__main__":
    libname = pathlib.Path().absolute() / "test_lib.so"
    c_lib = ctypes.CDLL(libname)
    
    print("Run callTest()...")
    time.sleep(1)
    
    #CallTest
    x = ctypes.c_int(15)
    call_answer = c_lib.callTest(x)
    
    print("returned: " + str(call_answer))
    print("Run pointerTest()...")
    time.sleep(1)
    
    #pointerTest
    c_lib.pointerTest.argtypes = (ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
    c_lib.pointerTest.restype = ctypes.c_bool
    a, b = ctypes.c_int(0), ctypes.c_int(0)
    pointer_answer = c_lib.pointerTest(ctypes.byref(a), ctypes.byref(b))
    
    print("a: " + str(a) + " - b: " + str(b) + " - returned: " + str(pointer_answer))
    
    
    
