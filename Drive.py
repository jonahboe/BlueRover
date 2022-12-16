# This script describes a class for controlling the GPIO pins
# connected to the tires of the robot.
#
# Last edit: 30 Nov, 2022 
# By: Colton Hill
#

import smbus
import time
import math
from simple_pid import PID

# The minimum and maximum speeds of the indevidual tires.
MAX_SPEED = 60
MIN_SPEED = 30

class Drive(object):

    # Method for initializing the I2C device and setting up the PID controller for turning.
    def get_i2c_device(self, address, i2c_bus):
        self._addr = address
        self.pid = PID(1, 0.1, 0.09, setpoint=0)
        self.diff = 0
        if i2c_bus is None:
            return smbus.SMBus(1)
        else:
            return smbus.SMBus(i2c_bus)

    # Initialize by creating the I2C, ultra-sonic, and infrared devices.
    def __init__(self, us, ir):
        # Create I2C device.
        self._device = self.get_i2c_device(0x16, 1)
        self.us = us
        self.ir = ir
    
    # Upon deletion, stop.
    def __del__(self):
        self.Car_Stop() 

    # Methods for writing to the motors
    # Note: This code came with the robot
    def write_u8(self, reg, data):
        try:
            self._device.write_byte_data(self._addr, reg, data)
        except:
            print ('write_u8 I2C error')

    def write_reg(self, reg):
        try:
            self._device.write_byte(self._addr, reg)
        except:
            print ('write_u8 I2C error')

    def write_array(self, reg, data):
        try:
            # self._device.write_block_data(self._addr, reg, data)
            self._device.write_i2c_block_data(self._addr, reg, data)
        except:
            print ('write_array I2C error')

    def Ctrl_Car(self, l_dir, l_speed, r_dir, r_speed):
        try:
            reg = 0x01
            data = [l_dir, l_speed, r_dir, r_speed]
            self.write_array(reg, data)
        except:
            print ('Ctrl_Car I2C error')
            
    def Control_Car(self, speed1, speed2):
        try:
            if speed1 < 0:
                dir1 = 0
            else:
                dir1 = 1
            if speed2 < 0:
                dir2 = 0
            else:
                dir2 = 1 
            
            self.Ctrl_Car(dir1, int(math.fabs(speed1)), dir2, int(math.fabs(speed2)))
        except:
            print ('Ctrl_Car I2C error')

    # Drive forwards
    def Car_Run(self, speed1, speed2):
        try:
            self.Ctrl_Car(1, speed1, 1, speed2)
        except:
            print ('Car_Run I2C error')

    def Car_Stop(self):
        try:
            reg = 0x02
            self.write_u8(reg, 0x00)
        except:
            print ('Car_Stop I2C error')

    def Car_Back(self, speed1, speed2):
        try:
            self.Ctrl_Car(0, speed1, 0, speed2)
        except:
            print ('Car_Back I2C error')

    def Car_Left(self, speed1, speed2):
        try:
            self.Ctrl_Car(0, speed1, 1, speed2)
        except:
            print ('Car_Spin_Left I2C error')

    def Car_Right(self, speed1, speed2):
        try:
            self.Ctrl_Car(1, speed1, 0, speed2)
        except:
            print ('Car_Spin_Left I2C error')

    def Car_Spin_Left(self, speed1, speed2):
        try:
            self.Ctrl_Car(0, speed1, 1, speed2)
        except:
            print ('Car_Spin_Left I2C error')

    def Car_Spin_Right(self, speed1, speed2):
        try:
            self.Ctrl_Car(1, speed1, 0, speed2)
        except:
            print ('Car_Spin_Right I2C error')

    # This method sets the pitch of the camera.
    def Ctrl_Servo(self, id, angle):
        try:
            reg = 0x03
            data = [id, angle]
            if angle < 0:
                angle = 0
            elif angle > 180:
                angle = 180
            self.write_array(reg, data)
        except:
            print ('Ctrl_Servo I2C error') 

    # This method allows the car to rome around while it waits to detect a person.
    def rome(self):
        distance = self.us.distanceTest()
        LeftSensorValue  = self.ir.getLeftDetect()
        RightSensorValue = self.ir.getRightDetect()
        # print("L: {0}, R: {1}".format(LeftSensorValue, RightSensorValue))
        #With obstacle pin is low level, the indicator light is on, without obstacle, pin is high level, the indicator light is off
        
        # If we are aproaching an object head-on, stop and spin right by 90 degrees or so
        # Note: Spin sets one side moving forwards, and the other moving back
        if distance < 15 or (LeftSensorValue and RightSensorValue):
            self.Car_Spin_Right(MAX_SPEED,MAX_SPEED) 
            time.sleep(1)

        # If there is an object on the right, then turn left slighty
        elif not LeftSensorValue and RightSensorValue:
            self.Car_Left(MAX_SPEED,0) 
            time.sleep(0.5)

        # If there is an object on the left, then turn right slighty
        elif LeftSensorValue and not RightSensorValue:
            self.Car_Right(0,MAX_SPEED) 
            time.sleep(0.5)

        # Otherwise, just keep moving forward
        # Note: Here, some random movment could also be done
        else:
            self.Car_Run(MAX_SPEED,MAX_SPEED)
    
    # If the person in front of us is somebody we do not know, then spin right 180 degrees,
    # and go the other direction
    def evade(self):
        self.Car_Spin_Right(MAX_SPEED,MAX_SPEED)
        time.sleep(1)
        timer = time.time()
        while time.time() - timer < 10:
            self.rome()

    # If the person in front of us is our owner, than we wan to go towards them until the
    # camera is pointed up 15 degrees, or we are close to an object (the person)
    def approach(self, pos, pitch):
        # If we are not close yet
        if not (self.us.distanceTest() < 15 or pitch < 15):
            # The PID is a differential variable
            self.diff -= int(self.pid(pos))
            # Bounded between -10 and 10
            self.diff = min(max(self.diff,-10),10)
            # And used to speed up / slow down one side or the other, in order to drive 
            # towards the the person
            self.Car_Run(MAX_SPEED + self.diff, MAX_SPEED - self.diff)