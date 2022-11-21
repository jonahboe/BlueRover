import sys
import Drive
import Ultrasonic
import FacialRecognition
import IR
import time
import threading
from simple_pid import PID
from playsound import playsound

us = Ultrasonic.Ultrasonic()
ir = IR.IR()
car = Drive.Drive(us, ir)

YAH = 80
PERSON_TIMEOUT = 10
OWNER_TIMEOUT = 5

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
    # Timer for person detection
    personTimer = time.time() + PERSON_TIMEOUT
    ownerTimer = time.time() + OWNER_TIMEOUT
    while True:
        try:
            # Get person location
            loc = em.location

            # If there is an owner...
            if em.owner:
                # If there isn't a person...
                if loc is None:
                    # If so much time has elapsed since last seeing someone...
                    if time.time() - personTimer >= 10:
                        # Reset the owner
                        em.owner = False
                    # Otherwise, wait for a person to enter frame
                    else:
                        car.Car_Stop()
                # If there is a person...
                else:
                    # Reset the person timer
                    personTimer = time.time()
                    # Adjust the camera
                    pitch -= pitch_pid(loc[1]/100)
                    print(pitch)
                    if pitch < 10:
                        pitch = 10
                    elif pitch > 60:
                        pitch = 60
                    # Drive towards them
                    car.approach(loc[0]/30, pitch)


            # If there is not an owner...
            else:
                # If there isn't a person...
                if loc is None:
                    # If so much time has elapsed since last seeing someone...
                    if time.time() - personTimer >= 10:
                        # Reset the pitch servo and wonder around
                        pitch = 60
                        car.rome()
                    # Otherwise, wait for a person to enter frame
                    else:
                        car.Car_Stop()
                # If there is a person...
                else:
                    # Reset the person timer
                    personTimer = time.time()
                    # If no owner exists, wait for owner identification
                    if not em.owner:
                        car.Car_Stop()
                        ownerTimer = time.time()
                        while time.time() - ownerTimer < OWNER_TIMEOUT:
                            if em.owner:
                                break
                    # If there is stil no owner, then get away barking
                    if not em.owner:
                        em.soundQueue.append('audio/growling.wav')
                        em.soundQueue.append('audio/growling.wav')
                        car.evade()

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
