import RPi.GPIO as GPIO
import time

EchoPin = 0
TrigPin = 1

def sonar_init():
    GPIO.setup(EchoPin,GPIO.IN,initial=GPIO.HIGH)
    GPIO.setup(TrigPin,GPIO.OUT,initial=GPIO.LOW)

def Distance():
    GPIO.output(TrigPin,GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(TrigPin,GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin,GPIO.LOW)

    t3 = time.time()

    while not GPIO.input(EchoPin):
        t4 = time.time()
        if (t4 - t3) > 0.03 :
            return -1


    t1 = time.time()
    while GPIO.input(EchoPin):
        t5 = time.time()
        if(t5 - t1) > 0.03 :
            return -1

    t2 = time.time()
    time.sleep(0.01)
#    print "distance is %d " % (((t2 - t1)* 340 / 2) * 100)
    return ((t2 - t1)* 340 / 2) * 100
