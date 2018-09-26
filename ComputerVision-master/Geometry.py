# Geometry
import numpy as np
import cv2
import cv2.cv as cv
from matplotlib import pyplot as plt

#If you want to to use frames from PiCam go to comment secion market with loads of: ##  ##  ##  ##
# comment out the 
        #frame = cv2.imread('PiCam.bmp',1)
# and comment in the
        #ret, frame = cap.read()
    



# This should be opensourced so that the community can add extra functions.
# Pretty much every function here is directly copied from the OpenCV website with 
# the exception of manual calibrator functions (findLineMC and edgeDectorMC).
#
# A point of notice is that this file needs a large number of additional shape detection
# algorithms in order to effectively use the blobTrackingByGeo in ImageDisturbance.py
#
# The geometric shape filter that would held in IDing the blobs would be called up by nesting one
# of the functions in Geometry.py into the ImageDisturbance.py file.


## ------------------------------------ Finding Lines  --------------------------------------------------------  

def findLine(image, minLineLength, maxLineGap, color):

    ret, frame = cap.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray,50,150,apertureSize = 3)
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength, maxLineGap)

    for x1,y1,x2,y2 in lines[0]:
        cv2.line(img, (x1,y1), (x2,y2), color, 2)
    cv2.imshow('PiCamera', frame)
    return lines



def nothing(x):
    pass



def findLineMC():
    cv2.namedWindow('PiCamera')
    cv2.createTrackbar('Min Line Length', 'PiCamera', 0, 500, nothing)
    cv2.createTrackbar('Max Line Gap', 'PiCamera', 0, 100, nothing)
    cv2.createTrackbar('B', 'PiCamera', 0, 255, nothing)
    cv2.createTrackbar('G', 'PiCamera', 0, 255, nothing)
    cv2.createTrackbar('R', 'PiCamera', 0, 255, nothing)

    while (True):
        #If you wanna read from the PiCamera ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ##
        #frame = cv2.imread('PiCam.bmp',1)
        ret, frame = cap.read()
        Filter = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        thresh1 = cv2.getTrackbarPos('Min Line Length', 'PiCamera')
        thresh2 = cv2.getTrackbarPos('Max Line Gap', 'PiCamera')

        B = cv2.getTrackbarPos('B', 'PiCamera')
        G = cv2.getTrackbarPos('G', 'PiCamera')
        R = cv2.getTrackbarPos('R', 'PiCamera')
        
        edges = cv2.Canny(Filter,50,150,apertureSize = 3)
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, thresh1, thresh2)
        if (lines != None):
            for x1,y1,x2,y2 in lines[0]:
                cv2.line(frame, (x1,y1), (x2,y2), (B,G,R), 2)

        cv2.imshow('PiCamera', frame)
        if (cv2.waitKey(1) & 0xFF == ord ('q')):
            break
    return lines



#----------------------------------- Edge Detection ---------------------------------------------------

def edgeDetector(image, thresh1, thresh2):
    #If you wanna read from the PiCamera ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ##
    #frame = cv2.imread('PiCam.bmp',1)
    ret, frame = cap.read()
    Filter = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(frame,thresh1,thresh2)
    cv2.imshow('PiCamera Edges', edges)
    return edges


def nothing(x):
    pass



def edgeDetectorMC():
    cv2.namedWindow('PiCamera')
    cv2.createTrackbar('Threshold1', 'PiCamera', 0, 1000, nothing)
    cv2.createTrackbar('Threshold2', 'PiCamera', 0, 1000, nothing)

    while (True):
        #If you wanna read from the PiCamera ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ##
        #frame = cv2.imread('PiCam.bmp',1)
        ret, frame = cap.read()
        Filter = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        thresh1 = cv2.getTrackbarPos('Threshold1', 'PiCamera')
        thresh2 = cv2.getTrackbarPos('Threshold2', 'PiCamera')

        edges = cv2.Canny(frame,thresh1,thresh2)

        cv2.imshow('PiCamera', edges)
        if (cv2.waitKey(1) & 0xFF == ord ('q')):
            break
    return edges


#-----------------------------------------------------------------------------------------------------
# If you would like to test this script in isolation:
# Just remove all of the hashtags (#) from the lines of code below:

# Dimensions for camera feed
#width=360
#height=240
#cap = cv2.VideoCapture(0)
#cap.set(3, width)
#cap.set(4, height)

#findLineMC()
#edgeDetectorMC()
#cv2.destroyAllWindows()
