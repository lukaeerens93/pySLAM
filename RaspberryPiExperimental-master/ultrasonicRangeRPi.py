#------------ Ultrasonic Range Finder Cluster Python Script -------------------

    
def ultrasound(TRIG,ECHO,num):
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    
    GPIO.output(TRIG, False)
    time.sleep(0.001)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO) == 0:
        pulse_start= time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    return distance

        

def lists():
    leftList = []
    rightList = []
    rearList = []
    return leftList, rightList, rearList




def listGenerator(s1,s2,s3,l1,l2,l3):
    # Make sure that you hook up correct sensors to correct pins
    l1.append(s1)
    l2.append(s2)
    l3.append(s3)


    
def finchSpeed():
    #These wheel speeds will be obtained from Finch
    rightWheelSpeed = 25
    leftWheelSpeed = 25
    return rightWheelSpeed, leftWheelSpeed



def maneuver(dist1,dist2,dist3,trigger):
    # The maneuver function should be used if you care about how QUICKLY an obstacle is approaching
    # not how far away. The rational behind having this kind of a function was that in some situations
    # finches would be driving parallel to walls or other mobile finchs driving in the same direction, 
    # the proximity to these obstacles doesn't remain a threat so long as the Finch maintains the same
    # course. The Finch could even be driving a perpendicular distance of 5cm from a wall and would only
    # steer away if the difference between the distance at t1 and t2 (timestep 1 and timestep 2) was negative
    # meaning that the gap is closing.
    
    # These are sublists that contain 2 values
    ll = []
    rel = []
    ril = []
    
    #_______RIGHT SIDE OF FINCH_________
    if (len(dist1) == 2):           #If there are 2 elements in the list
        if (dist1[0] > trigger):        #If current distance is not a threat
            evasionDistRight = 0            #Stay the course
        if (dist1[0] < trigger):        #If element within trigger distance
            evasionDistRight = round(dist1[1] - dist1[0],2) #velocity away from threat = threat incoming velocity 
        dist1[0] = dist1[1]         #move last element to beginning and make
        del dist1[1]                #room for next measurement by clearing second index
        
    #________LEFT SIDE OF FINCH_________                        
    if (len(dist3) == 2):        
        if (dist3[0] > trigger):
            evasionDistLeft = 0
        if (dist3[0] < trigger):
            evasionDistLeft = round(dist3[1] - dist3[0],2)
        dist3[0] = dist3[1]
        del dist3[1]

    #________REAR SIDE OF FINCH_________                        
    if (len(dist2) == 2):        
        if (dist2[0] > trigger):
            evasionDistRear = 0
        if (dist2[0] < trigger):
            evasionDistRear = round(dist2[1] - dist2[0],2)
        dist2[0] = dist2[1]
        del dist2[1]        

    return evasionDistRight, evasionDistLeft, evasionDistRear   




def turnExecution(rWspeed, lWspeed, rightCorrection, leftCorrection, rearCorrection, policy):

    # turnExecution examines the data and calculations made previously and determins how to act
    # What most of this function deals with is a navigation policy which is manually decided by
    # the user and affects the nature of the evasive actions done by the Finch.
    # Though a policy isn't really needed if there is an incoming collision on the right side alone
    # or on the left side alone (simply drive away from collision), but consider following scenario:
    #
    # If incoming sideways collisions on both sides imminent, this is a complex issue and so a policy
    # should be followed that determines turning executions:
    #
    #______________________Example policies:_________________________
    # 0: Stop     = If collisions imminent halt motion of Finch
    # 1: Middle   = Ensures impact velocities are equal on both sides
    # 2: Evasion  = Flee from collision (full speed ahead/reverse)

    
    #If incoming collision on right, right wheel should spin faster to turn Finch away.
    if (rightCorrection > 0 or rightCorrection < 0):
        if (leftCorrection == 0):
            rWspeed = rWspeed + rightCorrection
            lWspeed = lWspeed
            
    if (leftCorrection > 0 or leftCorrection < 0):
        if (rightCorrection == 0):
            lWspeed = lWspeed + leftCorrection
            rWspeed = rWspeed
            

   # If collisions from both left and right is imminent (this is where the driving policy comes in handy
   # Ultimately the last arguement of turnExecution that has been entered only comes in handy after this
   # point. Whether you entered a 0,1 or a 2 will only have an effect on the code after this (when the
   # Finch faces a simultaneous lateral collision on both sides).
   
    if (rightCorrection < 0 and leftCorrection < 0):

        if (policy == 0):
            rWspeed = 0
            lWspeed = 0
            
        
        if (policy == 1):
            #If incoming rear collision, but coast is clear in front
            if (rearCorrection < 0 and frontCorrection == 0):    
                rWspeed = rWspeed + rightCorrection
                lWspeed = lWspeed + leftCorrection
            #If incoming front collision, but coast is clear in rear
            if (rearCorrection == 0 and frontCorrection < 0):
                rWspeed = -rWspeed - rightCorrection
                lWspeed = -lWspeed - leftCorrection
            #If collisions imminent from front, rear, and both sides, stop!
            if (rearCorrection < 0 and leftCorrection < 0):
                rWspeed = 0
                lWspeed = 0


        if (policy == 2):            
            if (rearCorrection < 0 and frontCorrection == 0):    
                rWSpeed = 100
                lWSpeed = 100
            if (rearCorrection == 0 and frontCorrection < 0):
                rWSpeed = -100
                lWSpeed = -100
            if (rearCorrection < 0 and leftCorrection < 0):
                rWspeed = 0
                lWspeed = 0


        return rWspeed, lWspeed




#============================ Test Code ================================#
'''
# This code is implemented directly into the raspberry pi

import RPi.GPIO as GPIO
import time
import math
GPIO.setmode(GPIO.BCM)

#Details about the Finch
FinchWidth = 20         #Distance between mid points of two tires
TireCircumf = 20.797    #Circumference of Finch Wheels


l, ril, rel = lists()
while True:
    # Find the distances from each sensor
    sensor1 = ultrasound(26,19,3)       #Left Ultrasound
    sensor2 = ultrasound(20,21,2)       #Rear Ultrasound
    sensor3 = ultrasound(23,24,1)       #Right Ultrasound
    
    rw,lw = finchSpeed()
    
    listGenerator(sensor1, sensor2, sensor3, l, rel, ril)

    if ((len(l) == 2) and (len(ril) == 2)):
    
        changeR, changeL, changeRear = maneuver(l,rel,ril, 25)

        right, left = turnExecution(rw, lw, changeR, changeL, changeRear, 0)
        
    time.sleep(1)
        
GPIO.cleanup()
'''
