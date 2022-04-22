import os
import time

# importing the extension like a standart python module
from mm_gps import *

# calling functions from extension like a standart python function
# Inicialize the service
print("Loading plugin...")
time.sleep(1)
print("Connecting...")
#time.sleep(1)

path_var = os.path.dirname(__file__)+"/mm_c_api_plugin.so" 
print(path_var)
if initHedge('/dev/ttyACM0'):
    print(True)
else:
    print(False)

#Read data
for i in range(10):
    #1 data per second
    time.sleep(1)
    
    #Read in the hedge coordinate
    pos_buffer = getHedgePosition()
    print("Positions:\t" + str(pos_buffer))
    
    #Read in the beacon coordinate
    beac_pos_buffer = getHedgeStationaryBeaconsPositions()
    print("Beacons:\t" + str(beac_pos_buffer))
    
    #Read in the beacon distances
    dist_buffer = getHedgeRawDistances()
    print("Distances:\t" + str(dist_buffer))
    
    #Read in the raw IMU data
    IMU_buffer = getHedgeRawIMU()
    print("IMU data:\t" + str(IMU_buffer))
    
    #Read in the fusion IMU data
    fusion_buffer = getHedgeFusionIMU()
    print("Fusion data:\t" + str(fusion_buffer))
    
    #Read in the telemetry data
    telemetry_buffer = getHedgeTelemetry()
    print("Telemetry:\t" + str(telemetry_buffer))
    
    #Read in the quality data
    quality_buffer = getHedgeQuality()
    print("Quality:\t" + str(quality_buffer))
    
    print(" - - - - ")

# Close the service
print("Closing connection...")
#time.sleep(1)
stopped = stopHedge()
if stopped : print("Closed")
else: print("Error")
