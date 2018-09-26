# Test Script for Ultrasonic Range Finder sending instructions to PC

# this is to be run on the raspberry pi, so the only files that should
# be imported are the ultrasonic range finder reader and socket data
# sending files.
import ultrasonicRangeRPi
import RPi.GPIO as GPIO
import time
import math
import socket
import sys
import rPiServerSocketSend

GPIO.setmode(GPIO.BCM)

#Details about the Finch
FinchWidth = 20         #Distance between mid points of two tires
TireCircumf = 20.797    #Circumference of Finch Wheels


l, ril, rel = ultrasonicRangeRPi.lists()
# defined with 2 default values that will never be obtained during measurements
sendList = [-1,-1]

while True:
    # Find the distances from each sensor
    sensor1 = ultrasonicRangeRPi.ultrasound(26,19,3)       #Left Ultrasound
    sensor2 = ultrasonicRangeRPi.ultrasound(20,21,2)       #Rear Ultrasound
    sensor3 = ultrasonicRangeRPi.ultrasound(23,24,1)       #Right Ultrasound
    
    rw,lw = ultrasonicRangeRPi.finchSpeed()
    
    listGenerator(sensor1, sensor2, sensor3, l, rel, ril)

    # If you have filled in the left and right side distance
    # arrays with 2 sequential values
    if ((len(l) == 2) and (len(ril) == 2)):
        
        changeR, changeL, changeRear = ultrasonicRangeRPi.maneuver(l,rel,ril,25)
        
        exR, exL = ultrasonicRangeRPi.turnExecution(rw, lw, changeR, changeL, changeRear, 0)
        
        sendList[0], sendList[1] = exR, exL
        
        rPiServerSocketSend.socketSend(sendList,20,'172.16.1.191',8000,1)
        
    time.sleep(1)
        
GPIO.cleanup()

