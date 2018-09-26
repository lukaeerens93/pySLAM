##-------------------------HSV Manual Calibrator------------------------------
import cv2
import numpy as np


#If you want to to use frames from PiCam go to comment secion market with loads of: ##  ##  ##  ##
# comment out the 
        #frame = cv2.imread('PiCam.bmp',1)
# and comment in the
        #ret, frame = cap.read()


##----------------------------------------------------------------------------
def nothing(x):
    pass


width=360
height=240
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)
cv2.namedWindow('PiCamera')

cv2.createTrackbar('Hue low', 'PiCamera', 0, 179, nothing)
cv2.createTrackbar('Hue high', 'PiCamera', 0, 179, nothing)
cv2.createTrackbar('Saturation low', 'PiCamera', 0, 255, nothing)
cv2.createTrackbar('Saturation high', 'PiCamera', 0, 255, nothing)
cv2.createTrackbar('Value low', 'PiCamera', 0, 255, nothing)
cv2.createTrackbar('Value high', 'PiCamera', 0, 255, nothing)

index = 0
HSVarray = []
centroidArray = []
areaFrom30Array = []
areaArray = []
distanceArray = []
boxes = []






##----------------------------------------------------------------------------
def HSVManualCalib():
    print ("PLACE OBJECT 30CM FROM THE CAMERA")
    global index
    while (True):
        while (True):
            #If you wanna read from the PiCamera ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ##
            #frame = cv2.imread('PiCam.bmp',1)
            ret, frame = cap.read()
            Frame = cv2.GaussianBlur(frame, (5,5), 0)
            Filter = cv2.cvtColor(Frame, cv2.COLOR_BGR2HSV)

            huelow = cv2.getTrackbarPos('Hue low', 'PiCamera')
            huehigh = cv2.getTrackbarPos('Hue high', 'PiCamera')
            satulow = cv2.getTrackbarPos('Saturation low', 'PiCamera')
            satuhigh = cv2.getTrackbarPos('Saturation high', 'PiCamera')    
            valuelow = cv2.getTrackbarPos('Value low', 'PiCamera')
            valuehigh = cv2.getTrackbarPos('Value high', 'PiCamera')

            HSVLow = np.array([huelow,satulow,valuelow])
            HSVHigh = np.array([huehigh,satuhigh,valuehigh])    
            mask = cv2.inRange(Filter, HSVLow, HSVHigh)
            res = cv2.bitwise_and(frame, frame, mask= mask)

            cv2.imshow('PiCamera', res)
            if (cv2.waitKey(1) & 0xFF == ord ('q')):
                break
        HSVarray.append(huelow)
        HSVarray.append(satulow)
        HSVarray.append(valuelow)
        HSVarray.append(huehigh)
        HSVarray.append(satuhigh)
        HSVarray.append(valuehigh)

        cntr, hierchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cont in cntr:
            m = cv2.moments(cont)
            if (m['m00'] != 0):
                cx = float(m['m10']/m['m00'])
                cy = float(m['m01']/m['m00'])
                areaFrom30cm = cv2.contourArea(cont)
                if (areaFrom30cm > 1000):
                    areaFrom30Array.append(areaFrom30cm)    #
        
        decision = raw_input("Would you like to Calibrate for an additional colour? (Y/N)")
        if (decision == 'n' or decision == 'N'):
            break
        if (decision == 'y' or decision == 'Y'):
            index = index + 6
    cv2.destroyAllWindows()
    return index
    




##----------------------------------------------------------------------------
def BlobTracker(index):
    if (index == 0):
        contourCount = []
        c = 0   #If there are no contours detected, contourCount = 0
        
        #If you wanna read from the PiCamera ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ##
        #frame = cv2.imread('PiCam.bmp',1)
        ret, frame = cap.read()
        Frame = cv2.GaussianBlur(frame, (5,5), 0)
        Filter = cv2.cvtColor(Frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(Filter,
                           (HSVarray[index],HSVarray[index+1],HSVarray[index+2]),
                           (HSVarray[index+3],HSVarray[index+4],HSVarray[index+5]))
        contour, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contour:
            m = cv2.moments(cnt)
            if (m['m00'] != 0):
                cx = float(m['m10']/m['m00'])
                cy = float(m['m01']/m['m00'])
                area = cv2.contourArea(cnt)
                if area == 0:
                    print ('no color match')
                if area > 200:
                    x,y,w,h = cv2.boundingRect(cnt)
                    cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                    centroidArray.append(cx)
                    centroidArray.append(cy)
                    areaArray.append(area)
                    c = c + 1
            else:
                cx, cy = 0, 0
        contourCount.append(c)
        cv2.imshow('PiCamera', frame)
        
        return centroidArray, areaArray, contourCount

                            
    if (index > 0):
        contourCount = []
        c = 0               #If there are no contours detected, contourCount = 0
        for i in range (0, index + 1, 6):
            #c = 1   #counter of all contours
            
            #If you wanna read from the PiCamera ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ##
            #frame = cv2.imread('PiCam.bmp',1)
            ret, frame = cap.read()
            Frame = cv2.GaussianBlur(frame, (5,5), 0)
            Filter = cv2.cvtColor(Frame, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(Filter,
                               (HSVarray[i],HSVarray[i+1],HSVarray[i+2]),
                               (HSVarray[i+3],HSVarray[i+4],HSVarray[i+5]))
            contour, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in contour:
                m = cv2.moments(cnt)
                if (m['m00'] != 0):
                    cx = float(m['m10']/m['m00'])
                    cy = float(m['m01']/m['m00'])
                    area = cv2.contourArea(cnt)
                    if area == 0:
                        print ('no color match')
                        areaArray.append(-1)    #exception
                    if area > 200:
                        x,y,w,h = cv2.boundingRect(cnt)
                        boxes.append((x,y,w,h))
                        cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 2)
                        centroidArray.append(round(cx,3))   #Round these
                        centroidArray.append(round(cy,3))
                        areaArray.append(area)
                        c = c + 1
                        print ("i: " + str(i) + ", area: " + str(area))
                else:
                    cx, cy = 0, 0
            contourCount.append(c)
            c = 0

        # This part here is just used in order to created bounding boxes of different
        # colors based on the different HSV filter quantities used to detect the blobs
        a = 0
        # Go through array containing number of contours in each HSV range. eg: [3,5,2] 
        for z in range(0, len(contourCount),1):
            b = contourCount[z]

            # Draw rectangles with a different color based on contour count in each HSV range
            for m in range(a,b,1):
                i = boxes[m]
      
                # HSV qualities in RGB format (not converted)
                color = (HSVarray[z*6], HSVarray[z*6 + 1], HSVarray[z*6 + 2])

                # Key:  i[0]=x,   i[1]=y,     i[2]=w,     i[3]=h
                cv2.rectangle(frame, (i[0],i[1]), (i[0]+i[2], i[1]+i[3]), color, 2)
                
            # Upper end then becomes lower end
            a = b
 
        cv2.imshow('PiCamera', frame)
        boxes[:] = []
        return centroidArray, areaArray, contourCount
         




##----------------------------------------------------------------------------
## WARNING: This works best on shapes that look alike from different angles like spheres, cones etc.
def cvBasedRange(dstnc, countr):

    #if all objects that have same HSV property
    if (index == 0):
        for a in dstnc:
            rangeBySight = int(30*areaFrom30Array[0]/a)
            # Add the apparent distance to distanceArray
            distanceArray.append(rangeBySight)

        # Delete the "DistanceGauger" array, refered to as dstnc here
        del dstnc[:]
        return distanceArray


    #if detected objects were from multitple HSV filters
    if (index > 0):
        a = 0
        # Go through array containing number of contours in each HSV range.
        # eg: [3,5,2] 
        for z in range(0, len(countr),1):
            if (z == 0):
                b = countr[z]
                
            # areas from all HSV ranges are appended to areaArrays...
            # so is from a = 0, b = countr[i], then a = b, and b = countr[i] + countr[i-1]
            if (z > 0):
                b = countr[z] + countr[z-1]

            # Define i as area in each HSV range
            for m in range(a,b,1):
                i = areaArray[m]
                rangeBySight = int(30*i / areaFrom30Array[z])
                distanceArray.append(rangeBySight)
                
            # Upper end then becomes lower end
            a = b
        #Append this -1 distance which will show the end of measurement    
        distanceArray.append(-1)

        del dstnc[:]
        return distanceArray


        



##----------------------------------------------------------------------------
def obstGraphProj(CenterArray, RangeArray, countr):
    # Transform X coord whereby 0 marks the middle, not the top left corner
    # because in SLAM map, the birds eye view centreline has xcoord = 0

    # Remember also that the y-axis on the map is the distance in front, and so
    # the points sent to chart need to be (transformed x-coord, range)

    PointList = []

    # if object centroids are detected
    if (len(CenterArray) > 0): 

        for i in range(0, len(CenterArray), 2):
            
            XCent = int(CenterArray[i]) - 150    #150 is half the width of the image
            
            # extraPoints = np.array([XCent, RangeArray[i/2]])
            # Why is half the index used?
            # Index |   CenterArray |   RangeArray
            #   0   |       x1      |       r1
            #   1   |       y1      |       r2
            #   2   |       x2      |       -1
            #   3   |       y2      |

           
            # if range element is not -1 (equal to value appended at last element)
            if (RangeArray[i/2] != -1):
                # Append the coordinates to the those used up for SLAM algorithms
                PointList.append([XCent, RangeArray[i/2]])
        
        print ("PointList" + str(PointList))
        return PointList
    else:
        extraPoints = [-999,-999]   #this obscene number will disactivate successive functions in current loop count
        return extraPoints
        




##----------------------------------------------------------------------------
def ArrayReset(CenterArray, RangeArray, ExtraPointArray, ContourCnt):
    CenterArray[:] = []
    RangeArray[:] = []
    ExtraPointArray[:] = []
    ContourCnt[:] = []
    




##--------------------------------------------------------------------------------------------------------
def pathFollower(index, segmentationCount, minArea):    # work both as a line/road follower

    # -index:             Index of an HSV storage array, in case more than 1 path network color
    # -segmentationCount: How many times image will be cut horizontally in order to find centroids within those segments
    # - minArea:          Smallest size a blob within each image segment can be in order to still detect centroid
    
    #Centroid found in horizonatal segments of image, thereby finding centroids for successive chunks of path
    # Note:
    # - Low segmentation count values: coarsen centroid path (quicker code)
    #       However imagine a scenario when Finch encounters a divergence
    #       of 2 paths from current singular path...
    #       If segmentation is low, then centroid coordinate COULD end up
    #       being located between diverging paths (if a small enough chunk
    #       of original path was encompased within this segmentation.) Thus
    #       the Finch will drive in between diverging roads and later very
    #       aggressively execute a corrective turn, which may cause it to
    #       overshoot the path, as it will approach path quasi perpendicularly
    #       (such could be the extent of the correction). Thus horizontal
    #       segmentations will not be useful in finding the next centroid it
    #       has to drive to. Will instead need vertical ones as path now appears
    #       horizontally on image.. Complicated! Not good for this scenario!
    #
    # - High segmentation count values: make more regular adjustments, and better
    #   pick up road bifurcations, because you are segmenting the road into finer
    #   chunks and so are more precisely spotting the transition from 1 road to 2.
    #   If you have a centroid coordinate placed between diverging paths, location
    #   is not that far forward and so the corrective turns are not as aggressive.

    
    segmRatio = 240/segmentationCount    # Thickness (in pixels) of each segment
    segmList = []                        # List contains segmentation intervals
    # Append all of intervals into the list
    for i in range(0, 240, segmRatio):
        segmList.append(i)
        
    
    if (index == 0):
        contCount = []
        
        #If you wanna read from the PiCamera ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ##
        #frame = cv2.imread('PiCam.bmp',1)
        ret, frame = cap.read()
        Frame = cv2.GaussianBlur(frame, (5,5), 0)
        Filter = cv2.cvtColor(Frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(Filter,
                           (HSVarray[index],HSVarray[index+1],HSVarray[index+2]),
                           (HSVarray[index+3],HSVarray[index+4],HSVarray[index+5]))

        #Now segment image horizontally
        for j in range(0, len(segmList)-1): 
            
            #define segmenation bounding values by 2 sequential values at a time from the segmList
            segm = mask[segmList[j]:segmList[j+1] , :]
            
            #Find contours in each of those segmentation
            contour, hierarchy = cv2.findContours(segm, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contour:
                m = cv2.moments(cnt)
                if (m['m00'] != 0):
                    cx = float(m['m10']/m['m00'])
                    cy = float(m['m01']/m['m00'])
                    cy = cy + j     # Because cy is y coordinate within each image horizontal segmentation 
                    area = cv2.contourArea(cnt)
                    if area == 0:
                        print ('no road found')
                    if area > minArea:
                        # not that it is necessary in this code but if you want to avoid just having the
                        # contours in the last segment array with nothing else, you may need to create an array
                        # that holds the x,y,w,h values along with the BGR chosenfor the bounding box (doesnt have to be matching to the HSV
                        # to the HSV) 
                        x,y,w,h = cv2.boundingRect(cnt)
                        
                        # Append these to a list to be reffered to at the end of the loop otherwise you will 
                        #boxes.append((x,y+j*segmRatio,w,h))
                        cv2.rectangle(frame, (x, y+j*segmRatio), (x + w, y+j*segmRatio+ h), (0,255,0), 2)
                        centroidArray.append(cx)
                        centroidArray.append(cy)
                else:
                    cx, cy = 0, 0
        #for i in boxes:
            # Reminder:     i[0]=x, i[1]=y, i[2]=w, i[3]=h    
            #cv2.rectangle(frame, (i[0],i[1]), (i[0]+i[2], i[1]+i[3]), (0,255,0), 2)
        cv2.imshow('PiCamera', frame)
        #boxes[:] = []
        
        return centroidArray



    
    
##-----------------------------------------------------------------------------------------------------------
# Testing of this code:


#Calib = HSVManualCalib()
#AList = [[20,34], [-15,38], [11,47], [-8,22]]
#print ("AList: " + str(AList))
#extra = 0

#while True:
    
    #c = pathFollower(Calib, 8, 200)
 #   center, DistanceGauger, ContourCounter = BlobTracker(Calib)

                                #if len(ContourCounter) > 1:

  #  Range = cvBasedRange(DistanceGauger, ContourCounter)
   # print ("Range: " + str(Range))
    #extra = obstGraphProj(center, Range, ContourCounter)
    
#    if (extra != [-999,-999]):
 #       print ("AListB4" + str(extra))
  #      AList = np.array(extra)
   #     print ("AList" + str(AList))
#    else:
 #       AList = np.array([])
  #  print ("...........................................")
   # ArrayReset(center,Range,extra, ContourCounter)

  #  if (cv2.waitKey(1) & 0xFF == ord ('q')):
   #     break
#cv2.destroyAllWindows()


