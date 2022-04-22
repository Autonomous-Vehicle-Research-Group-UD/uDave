"""
Lidar
"""

import time
import math
import pickle
import serial
import numpy as np
from donkeycar.utils import norm_deg, dist, deg2rad, arr_to_img
from PIL import Image, ImageDraw

class RPLidar(object):
    '''
    https://pypi.org/project/pyrplidar/
    '''
    def __init__(self, port='/dev/ttyUSB0', mode='LEGACY', pwm=500):
        from pyrplidar import PyRPlidar
        self.port = port
        self.mode = mode
        self.pwm = pwm
        self.distances_prev = [] #a list of distance measurements 
        self.angles_prev = [] # a list of angles corresponding to dist meas above
        self.quality_prev = []
        self.distances_curr = [] #a list of distance measurements 
        self.angles_curr = [] # a list of angles corresponding to dist meas above
        self.quality_curr = []
        self.return_curr = False
        self.lidar = PyRPlidar()
        self.lidar.connect(self.port, baudrate=115200, timeout=3)
        self.lidar.set_motor_pwm(pwm)
        time.sleep(5)
        self.on = True
        print("info: ", self.lidar.get_info())
        print("health: ", self.lidar.get_health())
        #print("sample rate: ", self.lidar.get_samplerate())
        #print("typical scan mode: ", self.lidar.get_scan_mode_typical())
        #self.lidar.get_scan_modes()
        self.scan_started = False

    def update(self):
        if self.mode == 'EXPRESS':
              self.scan_generator = self.lidar.start_scan_express(2)
        else:
              self.scan_generator = self.lidar.start_scan()
        while self.on:
            try:
                   for count, scan in enumerate(self.scan_generator()):
                        if scan.start_flag == True:
                              #print(time.time())
                              self.scan_started = True
                              #print("COMPLETE: ", len(self.distances))
                              if self.return_curr == True:
                                    self.return_curr = False
                                    self.distances_curr = []
                                    self.angles_curr = []
                                    self.quality_curr = []
                              else:
                                    self.return_curr = True
                                    self.distances_prev = []
                                    self.angles_prev = []
                                    self.quality_prev = []
                        if self.scan_started == True:
                              if self.return_curr == True:
                                    self.distances_prev.append(scan.distance)
                                    self.angles_prev.append(scan.angle)
                                    self.quality_prev.append(scan.quality)
                              else:
                                    self.distances_curr.append(scan.distance)
                                    self.angles_curr.append(scan.angle)
                                    self.quality_curr.append(scan.quality)
            except serial.serialutil.SerialException:
                print('serial.serialutil.SerialException from Lidar. common when shutting down.')

    def run_threaded(self):
          if self.return_curr == True:
                #print("THREADED CURR: ", len(self.distances_curr))
                return self.distances_curr, self.angles_curr, self.quality_curr
          else:
                #print("THREADED PREV: ", len(self.distances_prev))
                return self.distances_prev, self.angles_prev, self.quality_prev

    def shutdown(self):
        self.on = False
        time.sleep(2)        
        self.lidar.stop()
        self.lidar.set_motor_pwm(0)
        self.lidar.disconnect()



class LidarPlot(object):
    '''
    takes the raw lidar measurements and plots it to an image
    '''
    PLOT_TYPE_LINE = 0
    PLOT_TYPE_CIRC = 1
    def __init__(self, resolution=(500,500),
        max_dist=1000, #mm
        radius_plot=3,
        plot_type=PLOT_TYPE_CIRC):
        self.frame = Image.new('RGB', resolution)
        self.max_dist = max_dist
        self.rad = radius_plot
        self.resolution = resolution
        if plot_type == self.PLOT_TYPE_CIRC:
            self.plot_fn = self.plot_circ
        else:
            self.plot_fn = self.plot_line
            

    def plot_line(self, img, dist, theta, max_dist, draw):
        '''
        scale dist so that max_dist is edge of img (mm)
        and img is PIL Image, draw the line using the draw ImageDraw object
        '''
        center = (img.width / 2, img.height / 2)
        max_pixel = min(center[0], center[1])
        dist = dist / max_dist * max_pixel
        if dist < 0 :
            dist = 0
        elif dist > max_pixel:
            dist = max_pixel
        theta = np.radians(theta)
        sx = math.cos(theta) * dist + center[0]
        sy = math.sin(theta) * dist + center[1]
        ex = math.cos(theta) * (dist + self.rad) + center[0]
        ey = math.sin(theta) * (dist + self.rad) + center[1]
        fill = 128
        draw.line((sx,sy, ex, ey), fill=(fill, fill, fill), width=1)
        
    def plot_circ(self, img, dist, theta, max_dist, draw):
        '''
        scale dist so that max_dist is edge of img (mm)
        and img is PIL Image, draw the circle using the draw ImageDraw object
        '''
        center = (img.width / 2, img.height / 2)
        max_pixel = min(center[0], center[1])
        dist = dist / max_dist * max_pixel
        if dist < 0 :
            dist = 0
        elif dist > max_pixel:
            dist = max_pixel
        theta = np.radians(theta)
        sx = int(math.cos(theta) * dist + center[0])
        sy = int(math.sin(theta) * dist + center[1])
        ex = int(math.cos(theta) * (dist + 2 * self.rad) + center[0])
        ey = int(math.sin(theta) * (dist + 2 * self.rad) + center[1])
        fill = 128

        draw.ellipse((min(sx, ex), min(sy, ey), max(sx, ex), max(sy, ey)), fill=(fill, fill, fill))

    def plot_scan(self, img, distances, angles, max_dist, draw):
        for dist, angle in zip(distances, angles):
            self.plot_fn(img, dist, angle, max_dist, draw)
            
    def run(self, distances, angles):
        '''
        takes two lists of equal length, one of distance values, the other of angles corresponding to the dist meas 
        '''
        self.frame = Image.new('RGB', self.resolution, (255, 255, 255))
        draw = ImageDraw.Draw(self.frame)
        self.plot_scan(self.frame, distances, angles, self.max_dist, draw)
        return self.frame

    def shutdown(self):
        pass


class BreezySLAM(object):
    '''
    https://github.com/simondlevy/BreezySLAM
    '''
    def __init__(self, MAP_SIZE_PIXELS=500, MAP_SIZE_METERS=10):
        from breezyslam.algorithms import RMHC_SLAM
        from breezyslam.sensors import Laser

        laser_model = Laser(scan_size=360, scan_rate_hz=10., detection_angle_degrees=360, distance_no_detection_mm=12000)
        MAP_QUALITY=5
        self.slam = RMHC_SLAM(laser_model, MAP_SIZE_PIXELS, MAP_SIZE_METERS, MAP_QUALITY)
    
    def run(self, distances, angles, map_bytes):
        
        self.slam.update(distances, scan_angles_degrees=angles)
        x, y, theta = self.slam.getpos()

        if map_bytes is not None:
            self.slam.getmap(map_bytes)

        #print('x', x, 'y', y, 'theta', norm_deg(theta))
        return x, y, deg2rad(norm_deg(theta))

    def shutdown(self):
        pass



class BreezyMap(object):
    '''
    bitmap that may optionally be constructed by BreezySLAM
    '''
    def __init__(self, MAP_SIZE_PIXELS=500):
        self.mapbytes = bytearray(MAP_SIZE_PIXELS * MAP_SIZE_PIXELS)

    def run(self):
        return self.mapbytes

    def shutdown(self):
        pass

class MapToImage(object):

    def __init__(self, resolution=(500, 500)):
        self.resolution = resolution

    def run(self, map_bytes):
        np_arr = np.array(map_bytes).reshape(self.resolution)
        return arr_to_img(np_arr)

    def shutdown(self):
        pass

