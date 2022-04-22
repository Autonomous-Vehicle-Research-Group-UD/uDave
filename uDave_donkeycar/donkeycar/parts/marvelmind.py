# Added by Palkovics Dénes
import time
import mm_gps
from . import udpclient
from .CarSpeed import Car_Speed

GPS_KEYS = ('gps/x', 'gps/y', 'gps/z', 'gps/angle', 'gps/time')
GPS_TYPES = ('float', 'float', 'float', 'int', 'int')
QUALITY_KEYS = ('gps/quality',)
QUALITY_TYPES = ('int',)
IMU_KEYS = ('imu/acl_x', 'imu/acl_y', 'imu/acl_z',
            'imu/gyr_x', 'imu/gyr_y', 'imu/gyr_z',
            'imu/mag_x', 'imu/mag_y', 'imu/mag_z', 'imu/time')
IMU_TYPES = ('int', 'int', 'int',
             'int', 'int', 'int',
             'int', 'int', 'int', 'int')
IMU_FUS_KEYS = ('imu-fus/x', 'imu-fus/y', 'imu-fus/z',
                'imu-fus/qtr_w', 'imu-fus/qtr_x', 'imu-fus/qtr_y', 'imu-fus/qtr_z',
                'imu-fus/vel_x', 'imu-fus/vel_y', 'imu-fus/vel_z',
                'imu-fus/acl_x', 'imu-fus/acl_y', 'imu-fus/acl_z', 'imu-fus/time')
IMU_FUS_TYPES = ('float', 'float', 'float',
                 'float', 'float', 'float', 'float',
                 'float', 'float', 'float',
                 'float', 'float', 'float', 'int')

__TYPE_DEFAULT_VAL__ = {'int': 0, 'float': 0.}


class Marvelmind:
    def __init__(self,addr=None,usb_tty="/dev/ttyACM0", services=(), poll_delay=0.25):
        udpclient.open_socket("172.22.9.60", 3002)
        self.services = services
        self.addr = addr
        self.data = {}
        self.types = {}
        # Register the right datafields for each service on demand
        # Available services: "gps", "quality", "imu", "imu-fusion"
        if 'gps' in self.services:
            self.data.update(zip(GPS_KEYS, map(__TYPE_DEFAULT_VAL__.__getitem__, GPS_TYPES)))
            self.types.update(zip(GPS_KEYS, GPS_TYPES))
        if 'quality' in self.services:
            self.data.update(zip(QUALITY_KEYS, map(__TYPE_DEFAULT_VAL__.__getitem__, QUALITY_TYPES)))
            self.types.update(zip(QUALITY_KEYS, QUALITY_TYPES))
        if 'imu' in self.services:
            self.data.update(zip(IMU_KEYS, map(__TYPE_DEFAULT_VAL__.__getitem__, IMU_TYPES)))
            self.types.update(zip(IMU_KEYS, IMU_TYPES))
        if "imu-fusion" in self.services:
            self.data.update(zip(IMU_FUS_KEYS, map(__TYPE_DEFAULT_VAL__.__getitem__, IMU_FUS_TYPES)))
            self.types.update(zip(IMU_FUS_KEYS, IMU_FUS_TYPES))
        self.datakeys = tuple(self.data.keys())
        self.poll_delay = poll_delay
        # self.sensor.start()
        mm_gps.initHedge(usb_tty,1,0)
        self.on = True

    def update(self):
        while self.on:
            self.poll()
            #print(self.data)
            speed=Car_Speed.car_Speed(self.data['imu/acl_x'],self.data['imu/acl_y'])
            udpclient.senddata(0,self.data['imu/gyr_x'],self.data['imu/gyr_y'],speed,self.data['gps/angle'])
            time.sleep(self.poll_delay)

    def poll(self):
        if 'gps' in self.services:
            try:
                addr, timestamp, x, y, z, angle, highRes, _, _ = mm_gps.getHedgePosition()
                if self.addr and self.addr != addr:
                    print("data from another beacon({}). Skip it!".format(addr))
                    return
                
                div = 1000
                
                x,y,z = x/div, y/div, z/div
                self.data.update(zip(GPS_KEYS, (x, y, z, angle, timestamp)))
		
            except:
                print("Error [Marvelmind]: polling position was failed!")

        if 'quality' in self.services:
            try:
                addr, quality_per = mm_gps.getHedgeQuality()
                if self.addr and self.addr != addr:
                    print("data from another beacon({}). Skip it!".format(addr))
                    return
                
                self.data[QUALITY_KEYS[0]] = quality_per
            except:
                print("Error [Marvelmind]: polling quality was failed!")
        
        if 'imu' in self.services:
            try:
                acc_x,acc_y,acc_z,gyro_x,gyro_y,gyro_z,compass_x,compass_y,compass_z,timestamp = mm_gps.getHedgeRawIMU()
                self.data.update(
                    zip(IMU_KEYS, (acc_x,     acc_y,     acc_z,
                                   gyro_x,    gyro_y,    gyro_z,
                                   compass_x, compass_y, compass_z,
                                   timestamp)))

            except:
                print("Error [Marvelmind]: polling imu was failed!")

        if 'imu-fusion' in self.services:
            try:
                x,y,z,qw,qx,qy,qz,vx,vy,vz,ax,ay,az,timestamp = mm_gps.getHedgeFusionIMU()
                self.data.update(zip(IMU_FUS_KEYS, (x,  y,  z,
                                                    qw, qx, qy, qz,
                                                    vx, vy, vz,
                                                    ax, ay, az,
                                                    timestamp)))
            except:
                print("Error [Marvelmind]: polling imu-fusion was failed!")

    def run(self):
        self.poll()
        return tuple(map(self.data.__getitem__, self.datakeys))

    def run_threaded(self):
        return tuple(map(self.data.__getitem__, self.datakeys))

    def shutdown(self):
        self.on = False
        udpclient.close_socket()
        # self.sensor.stop()
        mm_gps.stopHedge()
