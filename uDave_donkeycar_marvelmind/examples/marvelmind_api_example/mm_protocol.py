#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 11:45:31 2021

Python file to call the C API

@author: mate
"""

#Import - Use ctypes
import ctypes as ct

#Defines
_MAX_STATIONARY_BEACONS = 30
_MAX_BUFFERED_POSITIONS = 3

#Structures
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
        ("distances",RawDistanceItem * 4), # 4 element array
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
        ("beacons",StationaryBeaconPosition * _MAX_STATIONARY_BEACONS), # _MAX_STATIONARY_BEACONS element array
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

#Global ctype library variable    
c_lib = None

#Load the library and initialise the data provider
def LoadLibrary(lib_path, serial_port_asByte):
    global c_lib
    #import pathlib
    #pathlib.Path().absolute() / "c_api_plugin.so"
    c_lib = ct.CDLL(lib_path)
    
    #Return types
    c_lib.initHedge.restype = ct.c_bool
    c_lib.getHedgePosition.restype = ct.c_bool
    c_lib.getHedgePosition.argtypes = [ct.POINTER(PositionValue)]
    c_lib.getHedgeStationaryBeaconsPositions.restype = ct.c_bool
    c_lib.getHedgeStationaryBeaconsPositions.argtypes = [ct.POINTER(StationaryBeaconPosition)]
    c_lib.getHedgeRawDistances.restype = ct.c_bool
    c_lib.getHedgeRawDistances.argtypes = [ct.POINTER(RawDistances)]
    c_lib.getHedgeRawIMU.restype = ct.c_bool
    c_lib.getHedgeRawIMU.argtypes = [ct.POINTER(RawIMUValue)]
    c_lib.getHedgeFusionIMU.restype = ct.c_bool
    c_lib.getHedgeFusionIMU.argtypes = [ct.POINTER(FusionIMUValue)]
    c_lib.getHedgeTelemetry.restype = ct.c_bool
    c_lib.getHedgeTelemetry.argtypes = [ct.POINTER(TelemetryData)]
    c_lib.getHedgeQuality.restype = ct.c_bool
    c_lib.getHedgeQuality.argtypes = [ct.POINTER(QualityData)]
    c_lib.initHedge.restype = ct.c_bool
    
    #Start the hedge thread - initialize the service
    #b'/dev/ttyACM0'
    init_success = c_lib.initHedge(ct.c_char_p(serial_port_asByte))
    
    if not init_success:
        raise Exception("Cannot initialize the data provider.")
    
    return

#Read in hedge position data.
def GetHedgePosition():
    global c_lib
    #Exception if not loaded
    if c_lib is None:
        raise Exception("Library not loaded yet.")
    #Read in the data
    pos_data_buffer = PositionValue()
    success = c_lib.getHedgePosition(ct.byref(pos_data_buffer))
    #Exception if unsuccessfull
    #if not success:
    #    raise Exception("Cannot read hedge position.")
    return pos_data_buffer

#Read in stationary beacon position data.
def GetStationaryBeaconsPositions():
    global c_lib
    #Exception if not loaded
    if c_lib is None:
        raise Exception("Library not loaded yet.")
    #Read in the data
    stationary_pos_data_buffer = StationaryBeaconsPositions()
    success = c_lib.getHedgeStationaryBeaconsPositions(ct.byref(stationary_pos_data_buffer))
    #Exception if unsuccessfull
    #if not success:
    #    raise Exception("Cannot read stationary beacons positions.")
    return stationary_pos_data_buffer

#Read in hedge and staionary beacon raw distance data.
def GetRawDistances():
    global c_lib
    #Exception if not loaded
    if c_lib is None:
        raise Exception("Library not loaded yet.")
    #Read in the data
    raw_dist_data_buffer = RawDistances()
    success = c_lib.getHedgeRawDistances(ct.byref(raw_dist_data_buffer))
    #Exception if unsuccessfull
    #if not success:
    #    raise Exception("Cannot read raw distances.")
    return raw_dist_data_buffer

#Read in raw hedge imu data.
def GetRawIMU():
    global c_lib
    #Exception if not loaded
    if c_lib is None:
        raise Exception("Library not loaded yet.")
    #Read in the data
    raw_imu_data_buffer = RawIMUValue()
    success = c_lib.getHedgeRawIMU(ct.byref(raw_imu_data_buffer))
    #Exception if unsuccessfull
    #if not success:
    #    raise Exception("Cannot read raw imu.")
    return raw_imu_data_buffer

#Read in fusion hedge position and imu data.
def GetFusionIMU():
    global c_lib
    #Exception if not loaded
    if c_lib is None:
        raise Exception("Library not loaded yet.")
    #Read in the data
    fus_imu_data_buffer = FusionIMUValue()
    success = c_lib.getHedgeFusionIMU(ct.byref(fus_imu_data_buffer))
    #Exception if unsuccessfull
    #if not success:
    #    raise Exception("Cannot read fusion imu.")
    return fus_imu_data_buffer

#Read in telemetry data.
def GetTelemetry():
    global c_lib
    #Exception if not loaded
    if c_lib is None:
        raise Exception("Library not loaded yet.")
    #Read in the data
    tel_data_buffer = TelemetryData()
    success = c_lib.getHedgeQuality(ct.byref(tel_data_buffer))
    #Exception if unsuccessfull
    #if not success:
    #    raise Exception("Cannot read telemetry data.")
    return tel_data_buffer

#Read in quality data.
def GetQuality():
    global c_lib
    #Exception if not loaded
    if c_lib is None:
        raise Exception("Library not loaded yet.")
    #Read in the data
    qua_data_buffer = QualityData()
    success = c_lib.getHedgePosition(ct.byref(qua_data_buffer))
    #Exception if unsuccessfull
    #if not success:
    #    raise Exception("Cannot read quality data.")
    return qua_data_buffer

#Close the data provider and free the ctype library variable.
def CloseLibrary():
    global c_lib
    #Exception if not loaded
    if c_lib is None:
        raise Exception("Library not loaded yet.")
    #Close the hedge thread - close the service
    stopped = c_lib.stopHedge()
    #Exception if unsuccessfull
    if not stopped:
        raise Exception("Hedge cannot be closed.")
    else:
        del c_lib
    return stopped
