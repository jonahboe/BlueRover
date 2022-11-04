import RPi.GPIO as GPIO

class IR:
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
    
    def __del__(self):
        GPIO.cleanup()

    def getRightDetect(self):
        return not GPIO.input(self.AvoidSensorRight)

    def getLeftDetect(self):
        return not GPIO.input(self.AvoidSensorLeft)
    
