import sys
import Drive
import Ultrasonic
import Emotion
import IR
import time
from simple_pid import PID

car = Drive.Drive()
us = Ultrasonic.Ultrasonic()
ir = IR.IR()

YAH = 80
LOCATING_TIMEOUT = 10

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

    # set pitch and yah servo for camera... Twice? There's a bug in the library.
    car.Ctrl_Servo(1, YAH)
    car.Ctrl_Servo(2, 60)
    time.sleep(1)
    car.Ctrl_Servo(1, YAH)
    car.Ctrl_Servo(2, 60)

    # We need a PID controller for the pitch servo
    pitch_pid = PID(1, 0.1, 0.05, setpoint=60)
    pitch_pid.output_limits = (0, 60) 

    # Run main control loop 
    while True:
        # Check if there is a person
        for t in range(LOCATING_TIMEOUT):
            loc = em.location
            if loc is not None:
                break
        # If there isn't, then reset the pitch servo
        if loc is None:
            car.Ctrl_Servo(2, 60)
        # Otherwise move the cmera pitch to center the subject
        else:
            y = loc[1]
            y_delta = pitch_pid(loc[1])
            car.Ctrl_Servo(2, y_delta)
            print(loc)
        #car.avoid(ir=ir, us=us)

    # Stop the car and dispose of resources
    car.Car_Stop() 
    del car
    del us
    del ir
    del em
