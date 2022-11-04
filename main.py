import Drive
import Ultrasonic
import IR
import time

car = Drive.Drive()
us = Ultrasonic.Ultrasonic()
ir = IR.IR()

def runCar():
    car.Car_Run(150, 150)
    time.sleep(1)
    car.Car_Stop()

def tiltServo():
    # Tilt
    car.Ctrl_Servo(1, 180) #The servo connected to the S1 interface on the expansion board, rotate to 180°
    time.sleep(0.5)

    car.Ctrl_Servo(2, 180) #The servo connected to the S2 interface on the expansion board, rotate to 180°
    time.sleep(0.5)
    
    # And back
    car.Ctrl_Servo(1, 90)
    time.sleep(0.5)
        
    car.Ctrl_Servo(2, 90)
    time.sleep(0.5)

def detectDistance():
    for i in range(20):
        print(us.distance())
        time.sleep(1)

def testIR():
    for i in range(20):
        print("Right: " + str(ir.getRightDetect()))
        print("Left: " + str(ir.getLeftDetect()))
        print()
        time.sleep(1)

def avoid():
    distance = us.distanceTest()
    LeftSensorValue  = ir.getLeftDetect()
    RightSensorValue = ir.getRightDetect()
    print("L: {0}, R: {1}".format(LeftSensorValue, RightSensorValue))
    #With obstacle pin is low level, the indicator light is on, without obstacle, pin is high level, the indicator light is off
    if distance < 15 and LeftSensorValue and RightSensorValue:
        car.Car_Stop() 
        time.sleep(0.1)
        car.Car_Spin_Right(80,80) 
        time.sleep(1)
    elif distance < 15 and not LeftSensorValue and RightSensorValue:
        car.Car_Stop()
        time.sleep(0.1)
        car.Car_Spin_Left(80,80) 
        time.sleep(1)
        if LeftSensorValue and not RightSensorValue:
            car.Car_Stop()
            time.sleep(0.1)
            car.Car_Spin_Right(80,80) 
            time.sleep(2)
    elif distance < 15 and LeftSensorValue and not RightSensorValue:
        car.Car_Stop() 
        time.sleep(0.1)
        car.Car_Spin_Right(80,80)
        time.sleep(1)
        if not LeftSensorValue and RightSensorValue:
            car.Car_Stop()
            time.sleep(0.1)
            car.Car_Spin_Left(80,80) 
            time.sleep(2)
    elif distance < 15 and not LeftSensorValue and not RightSensorValue:
        car.Car_Stop() 
        time.sleep(0.1)
        car.Car_Spin_Right(80,80) 
        time.sleep(0.5)
    elif distance >= 15 and LeftSensorValue and RightSensorValue:
        car.Car_Stop() 
        time.sleep(0.1)
        car.Car_Spin_Right(80,80) 
        time.sleep(1)
    elif distance >= 15 and LeftSensorValue and not RightSensorValue:
        car.Car_Stop() 
        time.sleep(0.1)
        car.Car_Spin_Right(80,80) 
        time.sleep(0.5)
    elif distance >= 15 and not LeftSensorValue and RightSensorValue:
        car.Car_Stop() 
        time.sleep(0.1)
        car.Car_Spin_Left(80,80) 
        time.sleep(0.5)
    else:
        car.Car_Run(80,80) 

# Main code goes here
try:
    while True:
        avoid()
except KeyboardInterrupt:
    pass
car.Car_Stop() 
del car
del us
del ir