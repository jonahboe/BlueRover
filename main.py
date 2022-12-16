# This script describes the main functionality of the Blue Rover
# Emotional Support animal. This project was developed for the
# final project of the SC6510 course, at Utah State University.
#
# Contributers:
# Jonah Boe, Colton Hill, Ela Bohlourihajar, and Tyler Conley
#
# Last edit: 30 Nov, 2022 
# By: Colton Hill
#

import sys
import Drive
import Ultrasonic
import FacialRecognition
import IR
import time
import threading
from simple_pid import PID
from playsound import playsound

# Create ultrasonic, infrared, and motor driving objects
us = Ultrasonic.Ultrasonic()
ir = IR.IR()
car = Drive.Drive(us, ir)

# Default camera pitch
YAH = 80
# Timeout to wait for a person to reenter the frame
PERSON_TIMEOUT = 10
# Timeout from the time a person is noticed to the time they have
# to be confirmed as the owner
OWNER_TIMEOUT = 5

# Function for playing the last sound in the queue
def sound():
    playsound(FR.soundQueue.pop(0))

# Main code goes here
if __name__ == '__main__':
    # Set up the facial detection
    FR = FacialRecognition.FacialRecognition()
    FR.daemon = True
    args = []
    for arg in sys.argv:
        args.append(arg.lower())
    if 'render=true' in args:
        FR.render = True
    try:
        FR.start()
    # If the program is closed, delete resources
    except KeyboardInterrupt:
        del car
        del us
        del ir
        del FR

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
            loc = FR.location

            # If there is an owner...
            if FR.owner:
                # If there isn't a person...
                if loc is None:
                    # If so much time has elapsed since last seeing someone...
                    if time.time() - personTimer >= PERSON_TIMEOUT:
                        print("--- Lost Owner!")
                        # Reset the owner
                        FR.owner = False
                    # Otherwise, wait for a person to enter frame
                    else:
                        # print("\tLooking for owner.")
                        #TODO: Should pan to look for owner face
                        car.Car_Stop()
                # If there is a person...
                else:
                    print("\tFound Owner found!")
                    # Reset the person timer
                    personTimer = time.time()
                    # Adjust the camera
                    pitch -= pitch_pid(loc[1]/100)
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
                        print("\tI'm board...")
                        # Reset the pitch servo and wonder around
                        pitch = 60
                        car.rome()
                    # Otherwise, wait for a person to enter frame
                    else:
                        print("\tI'm all alone...")
                        car.Car_Stop()
                # If there is a person...
                else:
                    # Reset the person timer
                    personTimer = time.time()
                    # If no owner exists, wait for owner identification
                    if not FR.owner:
                        print("\tWho are you?!")
                        car.Car_Stop()
                        ownerTimer = time.time()
                        while time.time() - ownerTimer < OWNER_TIMEOUT:
                            if FR.owner:
                                break
                    # If there is stil no owner, then get away barking
                    if not FR.owner:
                        print("--- Run away!!!")
                        FR.soundQueue.append('audio/growling.wav')
                        FR.soundQueue.append('audio/growling.wav')
                        car.evade()

                # Write the pitch to the camera 
                time.sleep(0.2)
                car.Ctrl_Servo(2, int(pitch))

            # Play sounds
            if len(FR.soundQueue) > 0 and not soundThread.is_alive():
                soundThread = threading.Thread(target=sound)
                soundThread.start()

        # If the program is closed, delete resources
        except KeyboardInterrupt:
            del car
            del us
            del ir
            del FR
