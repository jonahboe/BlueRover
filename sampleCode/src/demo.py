from yahboom_tank import YahboomTank
import time

tank = YahboomTank()
try:
    # Go forward for .5 seconds
    tank.set_motor_ratios(1, 1)
    time.sleep(0.5)
    # Turn left for 1 second
    tank.set_motor_ratios(0, 1)
    time.sleep(1)
    # Go forward for 1 second
    tank.set_motor_ratios(1, 1)
    time.sleep(1)
# Stop if Ctrl-C is pressed
except KeyboardInterrupt:
    pass
tank.destroy()
