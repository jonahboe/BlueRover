import sys
import Drive
import Ultrasonic
import Emotion
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

# Main code goes here
if __name__ == '__main__':
    # Set up the emotion detection
    em = Emotion.Emotion()
    em.daemon = True
    args = []
    for arg in sys.argv:
        args.append(arg.lower())
    if 'render=true' in args:
        em.render = True
    try:
        em.start()
    except KeyboardInterrupt:
        pass

    # Run avoidance 
    while True:
        time.sleep(1)
        #car.avoid(ir=ir, us=us)

    # Stop the car and dispose of resources
    car.Car_Stop() 
    del car
    del us
    del ir
    del em
