# Test Script for Ultrasonic Range Finder Adjusting the wheel speed
# (to be run on the SERVER/REMOTE PC)

import socket
from rpidatareceivetest import SocketReceive
from finch import Finch
from time import sleep
import numpy as np


# Before you begin this test script make sure you comment 
# out the test codes in all of the import python files
sket = dataSocketSettings()

#Instantiate the Finch object
autopilotFinch = Finch()

k = 0
while True:
    # just testing for 50 samples
    if (k == 50):
        break
    
    # receive ultrasonic range finder data from the raspberry pi
    d = dataReceiveSocket(sket, 1)

    # define the left, right wheel speeds 
    leftWheel = d[0]
    rightWheel = d[1]

    # Before you send the instructions to the wheels, make sure that
    # they are converted into 0.1 -> 1.0 values
    
    # Send instructions to the Finch Wheels
    autopilotFinch.wheels(leftWheel, rightWheel)

    # increment 
    k = k + 1
    
autopilotFinch.close()
sket.close()
