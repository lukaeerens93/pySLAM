##----------------------Image Disturbance---------------------------
import numpy as np
import cv2
import serial
import math

# WHEN READY TO SHIP, HASHTAG ALL OF THE STUFF IN THE TEST SCRIPT AT THE BOTTOM OF THE FILE

#=================================================================================================================#            
def backSubtract(frame, erosionIteration, dilationIteration, small, large):
    
    Frame = cv2.GaussianBlur(frame, (5,5), 0)
    
    #Employ a background cancellation algorithm
    foregroundmask = backgroundsub.apply(Frame)
    Erosion = cv2.dilate(foregroundmask, kernelID, erosionIteration)
    Dilation = cv2.dilate(Erosion, kernelID, dilationIteration)
    
    contours, hierachy = cv2.findContours(Dilation,
                                          cv2.RETR_EXTERNAL,
                                          cv2.CHAIN_APPROX_NONE)

    # Contours might not be found so need "sanity check before accessing contours"
    # len(contours) > 0:
    for cnt in contours:
        M = cv2.moments(cnt)
        cx = float(M['m10']/M['m00'])
        cy = float(M['m01']/M['m00'])
        area = cv2.contourArea(cnt)
        

        if (area < large and area > small):
            horilist.append(cx)
            vertlist.append(cy)
            contlist.append(cnt)
            x,y,w,h = cv2.boundingRect(cnt)
            cv2.rectangle(frame,(x,y),(x+w, y+h),(0,255,0),2)
                 
        #else:
            #print 'sorry no contours found'
    
    if (len(contlist) == 0):                # IF there are no contours detected:
        horilist.append(-666)               # append impossible values to the list which will trigger
        vertlist.append(-666)               # exception handling in functions that would otherwise
        contlist.append([[-666,-666]])      # use the values from the empty list and subsequently fail.
        areaIDlist.append(0)

    return horilist, vertlist, contlist, areaIDlist







######################################## A NOTE ABOUT BLOB TRACKING: ###################################################

# You can give an ID to each blob in the frame that first detects them, and then link up the blobs frame by frame.
# There are several rudimentary approaches to doing this:
# 1: By Distance
# 2: By Geometry
# 3: By Color
# 4: BY Area

blobXList = []
blobYList = []
blobIDTrackingMatrix = []   #Contains coordinates of each blob ID
test = []                   #contains blob count values
test1 = []                  #used for testing whether x and y cordinates are 666
frame1d = []                #contains the distance to origin of all centroids in frame1
frame2d = []                #contains the distance to origin of all centroids in frame2
distTrial = []              # Stores all distances from ALL points in successive frames

# List of lists that will contain coordinates for each blobID (10 blob ID limit)
blobIDMatrix = [[] for i in range(10)]

#=================================================================================================================#
def blobTrackingByDist(xlist, ylist, maxBlobDist):
    # 1) By Distance:   If the blobs are far away from each other and remain that way.
    #                   In this case you could assign IDs based on how close these blobs
    #                   are to the blobs in the previous frames.
    #       DOWNSIDE:   Not many real world scenarios exist with these conditions so  
    #                   limits the scope of problem sets which suit this method.
    #------------------------------------------------------------------------------------

    # X-Coordinate
    blobXList.append(len(xlist))    #Used by computer to know how many blob coordinates it has to parse through
    for x in xlist:
        if (x == -666):     # Exception handling
            continue
        blobXList.append(round(x,2))
    blobXList.append(666)   # A POSITIVE 666 is used in order to signify the end of a frame

    # Y-Coordinate
    blobYList.append(len(ylist))
    for y in ylist:
        if (x == -666):
            continue
        blobYList.append(round(y,2))
    blobYList.append(666)

    ###############################################################################
    # A point of notice is that the format of this list visualised in Unicode is: #
    # bloby: [4, 161.65, 141.5, 84.05, 98.72, 666, 3, 143.15, 86.57, 120.21, 666] #
    # _________________________(end of frame1)_^______________(end of frame2)_^__ #
    #_________^_Contour Count______________________^_Contour Count_______________ #
    ###############################################################################   
 
    # When blobs from 2 frames have been sampled
    if (blobYList.count(666) == 2):
        
        # If in sampling of both frames, the blob count is 1 IN BOTH: there is only 1 blob in the scene
        # so it has the same ID PROVIDED that it is not very far, otherwise could be seperate blob
      
        test.append(blobYList[0])   # 1st element : contour count for first frame        
        test.append(blobYList[blobYList.index(666)+1])  # Element after 666 : contour count in frame 2
    
        test1.append(blobYList[1])
        test1.append(blobYList[blobYList.index(666)+2])

        print ("bloby: " + str(blobYList))
        print ("test: " + str(test))
        print ("test1: " + str(test1))
        
        ##############################################################################################################
        # Here is a Challenge with the datastructure and my solution to get around it given the time constraints:
        # If NO contour detected in both frames:
        # bloby: [1, 666, 1, 666]
        #
        # If 1 contour detected in both frames:
        # bloby: [1, 156.42, 666, 1, 156.3, 666]
        #
        # The first thing that is appended to the blobXList and blobYList is the length of the list that contains the
        # blob x and y centroid coordinates. The length of the array is 1 if there is no contour (because of the 666
        # element) but is also 1 if there is one contour found. Here is conditional logic to deal with this:
        ##############################################################################################################

        
        # If contour length for both is 1, check to see if coordinates are 666,
        # if not then ID the blob and track it 
        if (test[0] == 1 and test[1] == 1):
            blobByDistSubFn1(maxBlobDist)
            
                 
        if (test[0] > 1 and test[1] == 1):
            blobByDistSubFn2(maxBlobDist)
            
                        
        if (test[0] == 1 and test[1] > 1):
            blobByDistSubFn3(maxBlobDist)
                    

        if (test[0] > 1 and test[1] > 1):
            blobByDistSubFn4(maxBlobDist)

        print ("blobIDMatrix: " + str(blobIDMatrix))
        #Delete the test arrays 
        test[:] = []
        test1[:] = []
        print ("")       
        #print ("bloby: " + str(blobYList))


        
        



def blobByDistSubFn1(maxBlobDistance):
    if (test1[0] == 666 and test1[1] == 666):
        # If no contours found, delete contour lists and move on...
        blobYList[:] = []
        blobXList[:] = []
        
    if (test1[0] != 666 and test1[1] == 666):
        # Preserve contour coordinates from frame1 and delete those from frame 2 in next loop
        print ("B")
        blobXList[blobXList.index(666)+1 : len(blobXList)] = []
        blobYList[blobYList.index(666)+1 : len(blobYList)] = []
        # if blob detected in frame 1 is close to a previously detected blob in the past 10 timesteps
        # add its location in the list of that blob ID
        for i in blobIDMatrix:
            # Difference between current coordinate and the last one for each of the blob IDs
            xid = blobXList[1] - blobIDMatrix[i][len(i)]
            yid = blobYList[1] - blobIDMatrix[i][len(i)]
            xid2 = xid*xid
            yid2 = yid*yid
            dstncXY = math.sqrt(xid2+yid2)
            if (dstncXY < maxBlobDistance):
                blobXList[1]

        # else add this location to a brand new blob ID

        
    if (test1[0] == 666 and test1[1] != 666):
        # Preserve contour coordinates from frame 2 and delete those from frame 1 in next loop
        print ("C")
        # Copy and paste data from frame 2 into lists for frame 1
        blobXList[0 : blobXList.index(666)] = blobXList[blobXList.index(666)+1 : len(blobXList)]
        blobYList[0 : blobYList.index(666)] = blobYList[blobYList.index(666)+1 : len(blobYList)]
        # And delete elements from frame 2
        blobXList[blobXList.index(666)+1 : len(blobXList)] = []
        blobYList[blobYList.index(666)+1 : len(blobYList)] = []


    if (test1[0] != 666 and test1[1] != 666):
        # if contours are found in both cases, compare the positions of centroids in both frames
        print ("All contours detected")
        
        # Create a blob tracking matrix that will return the coordinates of each blob ID centroid

        ######################################################
        #   BlobIDTrackingMatrix[] will have this format:    #
        #                                                    #
        #       | x1 | y1 | x2 | y2 | x3 | y3 | x4 | y4 |    #
        #-------+----+----+----+----+----+----+----+----+    #
        # Blob1 |    |    |    |    |    |    |    |    |    #
        #-------+----+----+----+----+----+----+----+----+    #
        # Blob2 |    |    |    |    |    |    |    |    |    #
        #-------+----+----+----+----+----+----+----+----+    #
        # Blob3 |    |    |    |    |    |    |    |    |    #
        #-------+----+----+----+----+----+----+----+----+    #
        #                       etc....                      #
        ######################################################

        
        #blobIDTrackingMatrix[]

        # When done, empty the lists
        blobYList[:] = []
        blobXList[:] = []





def blobByDistSubFn2(maxBlobDistance):
    if (test1[1] == 666):
        # Preserve contour coordinates from frame1 and delete those from frame 2 in next loop
        print ("E")
        blobXList[blobXList.index(666)+1 : len(blobXList)] = []
        blobYList[blobYList.index(666)+1 : len(blobYList)] = []

    else:
        # go through each blob in frame 1 and ID sequential blobs based on how close they are.
        # If it is a new blob incidence, then add ID for it, however if you do not detect any blobs
        # whose centroid is a maxBlobDist away from the last blob centroid appended for that ID,
        # then you should remove entire row for that blob. After path history reaches ~20 timesteps
        # per blob ID then delete the rear 10 elements

        # append x and y coordinates in the frame1d list
        for i in range(1, blobYList.index(666)):
            frame1d.append(blobXList[i])
            frame1d.append(blobYList[i])
        # append x and y coordinates in the frame2d list
        for j in range(blobYList.index(666)+1, len(blobYList)):
            frame2d.append(blobXList[j])
            frame2d.append(blobYList[j])    

        
        # for all x and y coordinates in frame 1
        for i in range(0, len(frame1d),2):
            # find distance points are from all points in frame2
            for j in range(0, len(frame2d), 2):
                dX = frame1d[i] - frame2d[j]
                dY = frame1d[i+1] - frame2d[j+1]
                sqrX = dX*dX
                sqrY = dY*dY
                distXY = math.sqrt(sqrX+sqrY)
                distTrial.append(distXY)
                
            #find closest coordinates in frame 1 to those of frame2
            m = min(distTrial)
            # if smaller than maximum distance allowable, then is same blob by Distance
            if (m < maxBlobDistance):
                print distTrial.index(m)
                blobIDMatrix[0].append(blobXList[i])
                blobIDMatrix[0].append(blobYList[i+1])


    ##########THIS IS NOT COMPLETE!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!###################################
    blobYList[:] = []
    blobXList[:] = []






def blobByDistSubFn3(maxBlobDistance):
    # When done, empty the lists
    blobYList[:] = []
    blobXList[:] = []





def blobByDistSubFn4(maxBlobDistance):
    
    #append x and y coordinates
    for i in range(1, blobYList.index(666)):
        frame1d.append(blobXList[i])
        frame1d.append(blobYList[i])
    for j in range(blobYList.index(666)+1, len(blobYList)):
        frame2d.append(blobXList[j])
        frame2d.append(blobYList[j])    

    # for all x and y coordinates in frame 1
    for i in range(0, len(frame1d),2):
        # find distance points are from all points in frame2
        for j in range(0, len(frame2d), 2):
            dX = frame1d[i] - frame2d[j]
            dY = frame1d[i+1] - frame2d[j+1]
            sqrX = dX*dX
            sqrY = dY*dY
            distXY = math.sqrt(sqrX+sqrY)
            distTrial.append(distXY)
            
        #find closest coordinates in frame 1 to those of frame2
        m = min(distTrial)
        # if smaller than maximum distance allowable, then is same blob by Distance
        if (m < maxBlobDistance):
            print distTrial.index(m)
            blobIDMatrix[0].append(blobXList[i])
            blobIDMatrix[0].append(blobYList[i+1])
                
    blobYList[:] = []
    blobXList[:] = []






#=================================================================================================================#
def blobTrackingByGeo(xlist, ylist):
    # 2) By Geometry:   If blobs in image are all geometrically heterogeneous in ways that
    #                   can be perceived by the computer. Blobs would be IDed based on whether
    #                   they are positive matches with a certain shape filter/ detector.
    #       DOWNSIDE:   Perspective changes the apparent cross section geometry. What looks like
    #                   a rectangle from one angle may look like a square from another etc. The
    #                   shapes would have to maintain pretty much the same orientation
    #                   irrespective of the robot's location. So either you do this with shapes
    #                   that look the same no matter the perspective (sphere, cyliner, cone - provided
    #                   Finch and Cone/cylinder stay level with one another) or you manually orient them in
    #                   real time so as to maintain a fixed orientation to the robot camera.
    #------------------------------------------------------------------------------------

    
    # X-Coordinate
    blobXList.append(len(xlist))    #Used by computer to know how many blob coordinates it has to parse through
    for x in xlist:
        if (x == -666):     # Exception handling
            continue
        blobXList.append(round(x,2))
    blobXList.append(666)   # A POSITIVE 666 is used in order to signify the end of a frame

    # Y-Coordinate
    blobYList.append(len(ylist))
    for y in ylist:
        if (x == -666):
            continue
        blobYList.append(round(y,2))
    blobYList.append(666)

    ##-------------------------------------------
    print ("THIS FUNCTION IS NOT YET AVAILABLE!")
    # When it is, you can remove this print ^
    ##-------------------------------------------

    test[:] = []
    test1[:] = []
    blobYList[:] = []
    blobXList[:] = []






#=================================================================================================================#
def blobTrackingByColor(xlist, ylist):
    # 3) By Color:      If the color qualities inside the space that is occupied by the blobs remains
    #                   within the treshold HSV settings. If you apply cv2.mask() to the binary image,
    #                   so that you fill the white with the colors that exist within that blob, you
    #                   should see for yourself whether blobs in successive frames retain that same color
    #                   histogram. You could thus ID them based on whether they are positive matches for this.
    #       DOWNSIDE:   Lighting, lighting, lighting... Computational cost higher because you are creating
    #                   histograms for each blob and comparing it to reference histograms, but appears in
    #                   principle to be the most robust of the 3 options

    for x in xlist:
        if (x == -666):
            continue





# def IDmemPolicy(triggerEndValue, ):
    # In order save memory you should also follow a coarsening/data clearing policy whereby either you:
    # - remove every Nth collumns after matrix reaches certain size, (to get coarse history of Finch path)
    # - Delete collumns from range(0,n) once the size of matrix passes a threshold

#=================================================================================================================#
def updateOriginalImage():
    print ("ok")
    # This function is for changing the default image that every frame is compared to in background subtraction
    
#=================================================================================================================#    
def resetIDPoints(xlist,ylist,clist):
    # Clear the list that contains the xcoordinate and ycoordinate of the background subtraction
    # blobs. You don't need to implement this in every iteration of the while loop, as it could be
    # used to sample a short or even long history of the coordinate locations.
    # Example Applications:
    # Short History -   You could keep a track of 2-5 succcessive blob locations to see in which 
    #                   direction they are headed. You could also investigate the acceleration
    # Long History -    You could investigate whether a blob was loitering around a particular area, which
    #                   requires the sampling of many data points and perhaps to apply K-Means, K-NN etc. 

    xlist[:] = []
    ylist[:] = []
    clist[:] = []



#---------------------------------------------------------------------------------------------------
# If you would like to test this script in isolation:
# Just remove all of the hashtags (#) from the lines of code below:

# Dimensions for camera feed
framewidth = 360
frameheight = 240
Feed = cv2.VideoCapture(0)
Feed.set(3, framewidth)
Feed.set(4, frameheight)

# Create array that holds x coordinates
horilist = []
vertlist = []
contlist = []   # contour list
areaIDlist = []

# Gaussian Mixture-based Background/Foreground Segmentation Algorithm from OpenCV
backgroundsub = cv2.BackgroundSubtractorMOG()
# Kernel size for image disturbance function
kernelID = np.ones((10,10), np.uint8)

jj = 1
while (True):
    #If you wanna read from the PiCamera ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ## ##  ##  ##  ##
    #frame = cv2.imread('PiCam.bmp',1)
    ret, frayme = Feed.read()

    a,b,c,d = backSubtract(frayme, 0,1,1000, 70000)

    blobTrackingByDist(a,b, 25)
    cv2.imshow ('Original Frame', frayme)
    resetIDPoints(a,b,c)
    jj = jj + 1
    
    if (cv2.waitKey(1) & 0xFF == ord ('q')):
        break


Feed.release()
cv2.destroyAllWindows()

