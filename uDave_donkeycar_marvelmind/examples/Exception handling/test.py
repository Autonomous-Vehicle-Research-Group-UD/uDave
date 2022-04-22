import os
import time
import traceback

# importing the extension like a standart python module
from mm_gps import *

# calling functions from extension like a standart python function
# Inicialize the service
print("Loading plugin...")
time.sleep(1)
print("Connecting...")
#time.sleep(1)

try:
    initHedge('/dev/ttyACM0', 1, 1);
except Exception as exc:
    traceback.print_exception(type(exc), exc, exc.__traceback__)
    pass

#Read data
for i in range(10):
    #1 data per second
    time.sleep(1)
    
    #Read in the hedge coordinate
    print("Positions:", end="\t")
    try:
        pos_buffer = getHedgePosition()
        print(pos_buffer)
    except Exception as exc:
        print(exc)
    
    #Read in the beacon coordinate
    print("Beacons:", end="\t")
    try:
        beac_pos_buffer = getHedgeStationaryBeaconsPositions()
        print(beac_pos_buffer)
    except Exception as exc:
        print(exc)
    
    #Read in the beacon distances
    print("Distances:", end="\t")
    try:
        dist_buffer = getHedgeRawDistances()
        print(dist_buffer)
    except Exception as exc:
        print(exc)
    
    #Read in the raw IMU data
    print("IMU data:", end="\t")
    try:
        IMU_buffer = getHedgeRawIMU()
        print(IMU_buffer)
    except Exception as exc:
        print(exc)
    
    #Read in the fusion IMU data
    print("Fusion data:", end="\t")
    try:
        fusion_buffer = getHedgeFusionIMU()
        print(fusion_buffer)
    except Exception as exc:
        print(exc)
        
    #Read in the telemetry data
    print("Telemetry:", end="\t")
    try:
        telemetry_buffer = getHedgeTelemetry()
        print(telemetry_buffer)
    except Exception as exc:
        print(exc)
        
    #Read in the quality data
    print("Quality:", end="\t")
    try:
        quality_buffer = getHedgeQuality()
        print(quality_buffer)
    except Exception as exc:
        print(exc)
    
    print(" - - - - ")

# Close the service
print("Closing connection...")
#time.sleep(1)
try:
    stopHedge()
except Exception as exc:
    traceback.print_exception(type(exc), exc, exc.__traceback__)

print("Exit application...")
