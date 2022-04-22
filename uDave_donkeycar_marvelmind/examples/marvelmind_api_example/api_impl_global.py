#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 11:57:37 2021

Test the marvelmind C api integration

@author: mate
"""

#Imports
import time
import pathlib
import mm_protocol
import ctypes as ct

#Use test_lib.so
if __name__ == "__main__":
    
    # Inicialize the service
    print("Loading plugin...")
    time.sleep(1)
    print("Connecting...")
    #time.sleep(1)
    
    mm_protocol.LoadLibrary( (pathlib.Path().absolute() / "c_api_plugin_global.so"), (b'/dev/ttyACM0') )
    
    #Read data
    for i in range(10):
        
        #1 data per second
        time.sleep(1)
        
        #Read in the hedge coordinate
        pos_buffer = mm_protocol.GetHedgePosition()
        print("x: " + str(pos_buffer.x) + " - y: " + str(pos_buffer.y) + " - z: " + str(pos_buffer.z))
        
        #Read in the raw distances
        raw_dist_buffer = mm_protocol.GetRawDistances()
        for i in range(4):
            print(raw_dist_buffer.distances[i].address_beacon, raw_dist_buffer.distances[i].distance)
        
    
    # Close the service
    print("Closing connection...")
    #time.sleep(1)
    if mm_protocol.CloseLibrary() : print("Closed")
    else: print("Error")
