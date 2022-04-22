import Jetson.GPIO as GPIO
import time
import math
class Speedometer:
    def __init__(self,pin_1=None,pin_2=None,pin_3=None,pin_4=None,diameter = 8,stop_time=2000):
        if pin_1==None or pin_2==None or pin_3==None or pin_4==None:
            raise Exception("Set up every pin for speedometer")
        self.pin_1_time = time.time()*1000
        self.pin_2_time = time.time()*1000
        self.pin_3_time = time.time()*1000
        self.pin_4_time = time.time()*1000
        self.stop_time = stop_time
        self.s = (diameter/100)*math.pi

        self.v1 = 0
        self.v2 = 0
        self.v3 = 0
        self.v4 = 0

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(pin_1, GPIO.IN)  
        GPIO.setup(pin_2, GPIO.IN)  
        GPIO.setup(pin_3, GPIO.IN)  
        GPIO.setup(pin_4, GPIO.IN)  

        GPIO.add_event_detect(pin_1, GPIO.FALLING, callback=self.handle_pin_1, bouncetime=10)
        GPIO.add_event_detect(pin_2, GPIO.FALLING, callback=self.handle_pin_2, bouncetime=10)
        GPIO.add_event_detect(pin_3, GPIO.FALLING, callback=self.handle_pin_3, bouncetime=10)
        GPIO.add_event_detect(pin_4, GPIO.FALLING, callback=self.handle_pin_4, bouncetime=10)

    def handle_pin_1(self,channel):
        d = time.time()*1000 - self.pin_1_time
        self.v1 = self.s/(d/1000)
        self.pin_1_time = time.time()*1000

    def handle_pin_2(self,channel):
        d = time.time()*1000 - self.pin_2_time
        self.v2 = self.s/(d/1000)
        self.pin_2_time = time.time()*1000

    def handle_pin_3(self,channel):
        d = time.time()*1000 - self.pin_3_time
        self.v3 = self.s/(d/1000)
        self.pin_3_time = time.time()*1000

    def handle_pin_4(self,channel):
        d = time.time()*1000 - self.pin_4_time
        self.v4 = self.s/(d/1000)
        self.pin_4_time = time.time()*1000

    def run(self):
        if (time.time()*1000 - self.pin_1_time >self.stop_time):
            self.v1 = 0
        if (time.time()*1000 - self.pin_2_time >self.stop_time):
            self.v2 = 0
        if (time.time()*1000 - self.pin_3_time >self.stop_time):
            self.v3 = 0
        if (time.time()*1000 - self.pin_4_time >self.stop_time):
            self.v4 = 0
        return self.v1,self.v2,self.v3,self.v4

    def run_threaded(self):
        if (time.time()*1000 - self.pin_1_time >self.stop_time):
            self.v1 = 0
        if (time.time()*1000 - self.pin_2_time >self.stop_time):
            self.v2 = 0
        if (time.time()*1000 - self.pin_3_time >self.stop_time):
            self.v3 = 0
        if (time.time()*1000 - self.pin_4_time >self.stop_time):
            self.v4 = 0
        return self.v1,self.v2,self.v3,self.v4
    
    def shutdown(self):
        GPIO.cleanup()


