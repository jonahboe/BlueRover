from yahboom_tank import YahboomTank
import time

tank = YahboomTank()

try:
  # If nothing is in front of the tank for 65 cm, go forwrd at quarter speed for 1 s. 
  # Else, go backward at quarter speed for 1 s.
  while True:
    dist = tank.get_sonar_distance()
    print(dist)
    if dist > 65:
      tank.set_motor_ratios(0.25, 0.25)
    else:
      tank.set_motor_ratios(-0.25, -0.25)
    time.sleep(1)


except KeyboardInterrupt:
  pass

tank.destroy()