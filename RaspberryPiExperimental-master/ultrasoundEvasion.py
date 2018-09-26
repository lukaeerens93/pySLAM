# Finch Testing Script for initiating evasive maneuvers based on ultrasonic
# range finder PROXIMITY data
#
# There will be 2 main test scripts for sonar based colision avoidance, one for
# proximity (how far objects are relative to Finch)
# speed (how quickly objects are approaching Finch)

import ultrasonicRangeRpi
from finch import Finch
from time import sleep

#Instantiate the Finch Object
TestFinch = Finch()

#Details about the Finch
FinchWidth = 20         #Distance between mid points of two tires
TireCircumf = 20.797    #Circumference of Finch Wheels

l, ril, rel = ultrasonicRangeRpi.lists()

#Starting Speed (0.5 on each wheel)
TestFinch.wheels(0.5, 0.5)

while True:

    # Find the distances from each sensor
    sensor1 = ultrasonicRangeRpi.ultrasound(26,19,3)       #Left Ultrasound
    sensor2 = ultrasonicRangeRpi.ultrasound(20,21,2)       #Rear Ultrasound
    sensor3 = ultrasonicRangeRpi.ultrasound(23,24,1)       #Right Ultrasound

    # Enter a number between 0-1, with 0.1 increments (example: 0.2, 0.5, 0.6, 0.9 etc.)
    rw,lw = ultrasonicRangeRpi.finchSpeed(0.5, 0.5)
    
    ultrasonicRangeRpi.listGenerator(sensor1, sensor2, sensor3, l, rel, ril)

    
    if ((len(l) == 2) and (len(ril) == 2)):
        changeR, changeL, changeRear = ultrasonicRangeRpi.maneuver(l,rel,ril, 25)
        
        rightwheel,leftwheel = ultrasonicRangeRpi.turnExecution(rw,lw,changeR,changeL,changeRear,0)

        TestFinch.wheels(rightwheel, leftwheel)
        
    sleep(0.1)
        
GPIO.cleanup()
