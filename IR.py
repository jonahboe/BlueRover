# This script describes a class for infrared detrection, using the robots GPIO
#
# Last edit: 4 Nov, 2022 
# By: Jonah Boe
#

import RPi.GPIO as GPIO

class IR:
    # Initialize all of the GPIO pins
    def __init__(self):
        self.AvoidSensorLeft = 21     #Left infrared obstacle avoidance sensor pin
        self.AvoidSensorRight = 19    #Right infrared obstacle avoidance sensor pin
        self.Avoid_ON = 22   #Infrared obstacle avoidance sensor switch pin
        GPIO.setmode(GPIO.BOARD)
        GPIO.setwarnings(False)
        GPIO.setup(self.AvoidSensorLeft, GPIO.IN)
        GPIO.setup(self.AvoidSensorRight, GPIO.IN)
        GPIO.setup(self.Avoid_ON, GPIO.OUT)
        GPIO.output(self.Avoid_ON,GPIO.HIGH)
    
    # Upon deletion, release the GPIO resources
    def __del__(self):
        GPIO.cleanup()

    # Get the right sensor distance from nearest obsticle
    def getRightDetect(self):
        return not GPIO.input(self.AvoidSensorRight)

    # Get the left sensor distance from nearest obsticle
    def getLeftDetect(self):
        return not GPIO.input(self.AvoidSensorLeft)
    
