import smbus
import time
import math
from simple_pid import PID

MAX_SPEED = 40

class Drive(object):

    def get_i2c_device(self, address, i2c_bus):
        self._addr = address
        self.pid = PID(1, 0.1, 0.09, setpoint=0)
        self.diff = 0
        if i2c_bus is None:
            return smbus.SMBus(1)
        else:
            return smbus.SMBus(i2c_bus)

    def __init__(self):
        # Create I2C device.
        self._device = self.get_i2c_device(0x16, 1)
    
    def __del__(self):
        self.Car_Stop() 

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

    def avoid(self, us, ir):
        distance = us.distanceTest()
        LeftSensorValue  = ir.getLeftDetect()
        RightSensorValue = ir.getRightDetect()
        print("L: {0}, R: {1}".format(LeftSensorValue, RightSensorValue))
        #With obstacle pin is low level, the indicator light is on, without obstacle, pin is high level, the indicator light is off
        if distance < 15 or (LeftSensorValue and RightSensorValue):
            self.Car_Spin_Right(MAX_SPEED,MAX_SPEED) 
            time.sleep(1)
        elif not LeftSensorValue and RightSensorValue:
            self.Car_Left(MAX_SPEED,0) 
            time.sleep(0.5)
        elif LeftSensorValue and not RightSensorValue:
            self .Car_Right(0,MAX_SPEED) 
            time.sleep(0.5)

    def approach(self, pos):
        self.diff -= int(self.pid(pos))
        if self.diff < -10:
            self.diff = -10
        elif self.diff > 10:
            self.diff = 10
        self.Car_Run(60+self.diff, 60-self.diff)