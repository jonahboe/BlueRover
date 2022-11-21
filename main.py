import sys
import Drive
import Ultrasonic
import FacialRecognition
import IR
import time
import threading
from simple_pid import PID
from playsound import playsound

car = Drive.Drive()
us = Ultrasonic.Ultrasonic()
ir = IR.IR()

YAH = 80
LOCATING_TIMEOUT = 10
OWNER_TIMEOUT = 20

def sound():
    playsound(em.soundQueue.pop(0))

# Main code goes here
if __name__ == '__main__':
    # Set up the emotion detection
    em = FacialRecognition.FacialRecognition()
    em.daemon = True
    args = []
    for arg in sys.argv:
        args.append(arg.lower())
    if 'render=true' in args:
        em.render = True
    try:
        em.start()
    except KeyboardInterrupt:
        del car
        del us
        del ir
        del em

    # set pitch and yah servo for camera... Twice? There's a bug in the library.
    car.Ctrl_Servo(1, YAH)
    car.Ctrl_Servo(2, 60)
    time.sleep(1)
    car.Ctrl_Servo(1, YAH)
    car.Ctrl_Servo(2, 60)

    # We need a PID controller for the pitch servo
    pitch_pid = PID(1, 0.1, 0.09, setpoint=0) 

    # Run main control loop
    pitch = 60

    # Thread for sound
    soundThread = threading.Thread(target=sound)
    while True:
        try:
            # Check if there is a person
            for t in range(LOCATING_TIMEOUT):
                loc = em.location
                if loc is not None:
                    break
            # If there isn't, then reset the pitch servo and wonder around
            if loc is None:
                pitch = 60
                car.avoid(us, ir)
            # Otherwise move the camera pitch to center the subject
            else:
                # Adjust the camera
                pitch -= pitch_pid(loc[1]/100)
                print(pitch)
                if pitch < 10:
                    pitch = 10
                elif pitch > 60:
                    pitch = 60
                # Check if owner
                car.Car_Stop
                for i in range(OWNER_TIMEOUT):
                    time.sleep(0.5)
                    if em.owner:
                        break
                # Drive to owner
                if em.owner:
                    car.approach(loc[0]/30)
                # TODO: Otherwise run away
            # Write the pitch to the camera 
            time.sleep(0.2)
            car.Ctrl_Servo(2, int(pitch))

            # Play sounds
            if len(em.soundQueue) > 0 and not soundThread.is_alive():
                soundThread = threading.Thread(target=sound)
                soundThread.start()
        except KeyboardInterrupt:
            del car
            del us
            del ir
            del em
