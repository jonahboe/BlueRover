import sys
import Drive
from Drive import MAX_SPEED, MIN_SPEED
import Ultrasonic
import FacialRecognition
import IR
import time
import threading
from simple_pid import PID
from pynput.keyboard import Key, Listener
import math
 

us = Ultrasonic.Ultrasonic()
ir = IR.IR()
car = Drive.Drive(us, ir)

MAX_PITCH = 120
MIN_PITCH = 45
MAX_YAH = 150
MIN_YAH = 30


YAH = 80
PITCH = 60
THROTTLE = 0

def control(key):
    global MAX_PITCH, MIN_PITCH, PITCH, MAX_YAH, MIN_YAH, YAH, MAX_SPEED,THROTTLE
    try:
        if key.char == 'a':
            YAH = min(YAH+1,MAX_YAH)
            car.Ctrl_Servo(1, YAH)

        elif key.char == 'd':
            YAH = max(YAH-1,MIN_YAH)
            car.Ctrl_Servo(1, YAH)

        elif key.char == 's':
            PITCH = min(PITCH+1,MAX_PITCH)
            car.Ctrl_Servo(2, PITCH)

        elif key.char == 'w':
            PITCH = max(PITCH-1,MIN_PITCH)
            car.Ctrl_Servo(2, PITCH)

    except AttributeError:
        if key == Key.left:
            THROTTLE = THROTTLE if abs(THROTTLE)>=45 else int(math.copysign(45,THROTTLE))
            car.Car_Left(abs(THROTTLE),abs(THROTTLE))

        elif key == Key.right:
            THROTTLE = THROTTLE if abs(THROTTLE)>=45 else int(math.copysign(45,THROTTLE))
            car.Car_Right(abs(THROTTLE),abs(THROTTLE))

        elif key == Key.up:
            THROTTLE = min(THROTTLE+1,MAX_SPEED)
            THROTTLE = MIN_SPEED if MIN_SPEED > THROTTLE > -MIN_SPEED else THROTTLE
            if THROTTLE >= 0:
                car.Car_Run(THROTTLE,THROTTLE)
            else:
                car.Car_Back(-THROTTLE,-THROTTLE)

        elif key == Key.down:
            THROTTLE = max(THROTTLE-1,-MAX_SPEED)
            THROTTLE = -MIN_SPEED if MIN_SPEED > THROTTLE > -MIN_SPEED else THROTTLE
            if THROTTLE >= 0:
                car.Car_Run(THROTTLE,THROTTLE)
            else:
                car.Car_Back(-THROTTLE,-THROTTLE)

        elif key == Key.space:
            THROTTLE = 0
            car.Car_Stop()

        elif key == Key.delete:
            return sys.exit(0)

    print(f'\tTHROTTLE:{THROTTLE}, PITCH:{PITCH}, YAH:{YAH}')
            


# Main code goes here
if __name__ == '__main__':
    args = []
    for arg in sys.argv:
        args.append(arg.lower())
    if 'render=true' in args:
        # Set up the emotion detection
        FR = FacialRecognition.FacialRecognition()
        FR.daemon = True
        FR.render = True
        FR.start()
    print("READY")

    # set pitch and yah servo for camera... Twice? There's a bug in the library.
    car.Ctrl_Servo(1, YAH)
    car.Ctrl_Servo(2, PITCH)
    time.sleep(1)
    car.Ctrl_Servo(1, YAH)
    car.Ctrl_Servo(2, PITCH)

# Collect all event until released
with Listener(on_press = control) as listener:  
    listener.join()

