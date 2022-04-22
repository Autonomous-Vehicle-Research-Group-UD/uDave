#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 10 11:57:37 2021

Test the marvelmind C api integration

@author: mate
"""

#Imports - Use ctypes
import time
import ctypes as ct
import pathlib

#Global vars
_MAX_STATIONARY_BEACONS = 30
_MAX_BUFFERED_POSITIONS = 3

class PositionValue(ct.Structure):
    _fields_ = [
        ("address",ct.c_uint8),
        ("timestamp",ct.c_uint32),
        ("x",ct.c_int32),
        ("y",ct.c_int32),
        ("z",ct.c_int32),            # coordinates in millimeters
        ("angle",ct.c_double),
        ("highResolution",ct.c_bool),
        ("ready",ct.c_bool),
        ("processed",ct.c_bool)
    ]

class RawIMUValue(ct.Structure):
    _fields_ = [
        ("acc_x",ct.c_uint16),
        ("acc_y",ct.c_uint16),
        ("acc_z",ct.c_uint16),
        ("gyro_x",ct.c_uint16),
        ("gyro_y",ct.c_uint16),
        ("gyro_z",ct.c_uint16),
        ("compass_x",ct.c_uint16),
        ("compass_y",ct.c_uint16),
        ("compass_z",ct.c_uint16),
        ("timestamp",ct.c_uint32),
        ("updated",ct.c_bool)
    ]

class FusionIMUValue(ct.Structure):
    _fields_ = [
        ("x",ct.c_uint32),              # coordinates in mm
        ("y",ct.c_uint32),
        ("z",ct.c_uint32),
        ("qw",ct.c_uint16),
        ("qx",ct.c_uint16),
        ("qy",ct.c_uint16),
        ("qy",ct.c_uint16),             # quaternion, normalized to 10000
        ("vx",ct.c_uint16),
        ("vy",ct.c_uint16),
        ("vz",ct.c_uint16),             # velocity, mm/s
        ("ax",ct.c_uint16),
        ("ay",ct.c_uint16),
        ("az",ct.c_uint16),             # acceleration, mm/s^2
        ("timestamp",ct.c_uint32),
        ("updated",ct.c_bool)
    ]

class RawDistanceItem(ct.Structure):
    _fields_ = [
        ("address_beacon",ct.c_uint8),
        ("distance",ct.c_uint32)        # distance, mm
    ]

class RawDistances(ct.Structure):
    _fields_ = [
        ("address_hedge",ct.c_uint8),
        ("distances",ct.POINTER(RawDistanceItem * 4)), # 4 element array
        #("distances",RawDistanceItem * 4), # 4 element array
        ("timestamp",ct.c_uint32),
        ("timeShift",ct.c_uint16),
        ("updated",ct.c_bool)
    ]

class StationaryBeaconPosition(ct.Structure):
    _fields_ = [
        ("address",ct.c_uint8),
        ("x",ct.c_uint32),
        ("y",ct.c_uint32),
        ("z",ct.c_uint32),              # coordinates in millimeters
        ("highResolution",ct.c_bool)
    ]

class StationaryBeaconsPositions(ct.Structure):
    _fields_ = [
        ("numBeacons",ct.c_uint8),
        ("beacons",ct.POINTER(StationaryBeaconPosition)), # _MAX_STATIONARY_BEACONS element array
        #("beacons", StationaryBeaconPosition * _MAX_STATIONARY_BEACONS), # _MAX_STATIONARY_BEACONS element array
        ("updated",ct.c_bool)
    ]

class TelemetryData(ct.Structure):
    _fields_ = [
        ("vbat_mv",ct.c_uint16),
        ("rssi_dbm",ct.c_int8),
        ("updated",ct.c_bool)
    ]

class QualityData(ct.Structure):
    _fields_ = [
        ("address",ct.c_uint8),
        ("quality_per",ct.c_uint8),
        ("updated",ct.c_bool)
    ]

#Use test_lib.so
if __name__ == "__main__":
    libname = pathlib.Path().absolute() / "c_api_plugin.so"
    c_lib = ct.CDLL(libname)
    
    print("Loading plugin...")
    #time.sleep(1)
    
    # ---------------------- #
    # Inicialize the service #
    # ---------------------- #
    
    c_lib.initHedge.restype = ct.c_void_p
    hedge_pointer = c_lib.initHedge(ct.c_char_p(b'/dev/ttyACM0'))     #The serial port
    
    print("Connecting...")
    #time.sleep(1)
    
    # --------------------- #
    # Get a few sensor data #
    # --------------------- #
    
    #getHedgePositionByAddr datatypes.
    c_lib.getHedgePosition.argtypes = (ct.c_void_p, ct.POINTER(PositionValue))
    c_lib.getHedgePosition.restype = ct.c_bool
    pos_data_buffer = PositionValue()
    
    #getHedgeStationaryBeaconsPositions datatypes.
    c_lib.getHedgeStationaryBeaconsPositions.argtypes = (ct.c_void_p, ct.POINTER(StationaryBeaconsPositions))
    c_lib.getHedgeStationaryBeaconsPositions.restype = ct.c_bool
    stationary_pos_data_buffer = StationaryBeaconsPositions()
    
    #getHedgeRawDistances datatypes.
    c_lib.getHedgeRawDistances.argtypes = (ct.c_void_p, ct.POINTER(RawDistances))
    c_lib.getHedgeRawDistances.restype = ct.c_bool
    raw_dist_data_buffer = RawDistances()
    
    #getHedgeRawIMU datatypes.
    c_lib.getHedgeRawIMU.argtypes = (ct.c_void_p, ct.POINTER(RawIMUValue))
    c_lib.getHedgeRawIMU.restype = ct.c_bool
    raw_imu_data_buffer = RawIMUValue()
    
    #getHedgeFusionIMU datatypes.
    c_lib.getHedgeFusionIMU.argtypes = (ct.c_void_p, ct.POINTER(FusionIMUValue))
    c_lib.getHedgeFusionIMU.restype = ct.c_bool
    fus_imu_data_buffer = FusionIMUValue()
    
    #getHedgeTelemetry datatypes.
    c_lib.getHedgeTelemetry.argtypes = (ct.c_void_p, ct.POINTER(TelemetryData))
    c_lib.getHedgeTelemetry.restype = ct.c_bool
    tel_data_buffer = TelemetryData()
    
    #getHedgeQuality datatypes.
    c_lib.getHedgeQuality.argtypes = (ct.c_void_p, ct.POINTER(QualityData))
    c_lib.getHedgeQuality.restype = ct.c_bool
    qua_data_buffer = QualityData()
    
    for i in range(20):
        
        #1 data per second
        time.sleep(1)
        
        #Read in the hedge coordinates
        success = c_lib.getHedgePosition(ct.c_void_p(hedge_pointer), ct.byref(pos_data_buffer))
        if success: 
            print("x: " + str(pos_data_buffer.x) + " - y: " + str(pos_data_buffer.y) + " - z: " + str(pos_data_buffer.z))
        else:
            print("Position read error.")
        
        #Read in the raw distances
        success = c_lib.getHedgeRawDistances(ct.c_void_p(hedge_pointer), ct.byref(raw_dist_data_buffer))
        if success:
            print(raw_dist_data_buffer.distances)
            #for i in range(4):
            #    print(list_of_dist[i].address_beacon, list_of_dist[i].distance)
        else:
            print("Raw distance read error.")
        
    
    # ----------------- #
    # Close the service #
    # ----------------- #
    
    print("Closing connection...")
    #time.sleep(1)
    
    #Close
    c_lib.initHedge.restype = ct.c_bool
    stopped = c_lib.stopHedge(ct.c_void_p(hedge_pointer))
    
