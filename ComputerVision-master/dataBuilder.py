# Machine Learning

import numpy as np
import cv2
import csv


#If you want to to use frames from PiCam go to comment secion market with loads of: ##  ##  ##  ##
# comment out the 
        #frame = cv2.imread('PiCam.bmp',1)
# and comment in the
        #ret, frame = cap.read()
        
        
        
# you could have the Finch automate the phototaking when it encounters an obstacle
# thereby building up a dataset of images to train ML algorithms on, so it could
# recognize this object in a scene thereafter (leave that to community of user)

# imageDataSetGenerator(frame, "label", 50, "obstacles", "C:\Users\BirdBrain\Documents\BirdBrain Tech\obstacles\")

def imageDatasetGenerator(total_images, label, recursion, dataset, directory):
    import os.path
    
    while (True):
        
        #If the dataset filename DOES exist
        if (os.path.isfile(str(dataset) + ".csv") == True):
            labelset = str(dataset) + ".csv"
            byteset = str(dataset) + ".txt"
            directory = str(directory)

        #If the dataset filename does NOT exist
        if (os.path.isfile(str(dataset) + ".csv") == False):
            #Create csv file that contains the labels for images
            lbl = open(str(dataset) + ".csv", "w+")
            lbl.close()
            labelset = str(dataset) + ".csv"
            
            #Create txt file that contains bytes for images in case you want to be able
            #to load images from a txt file without constantly needing them in directories
            byt = open(str(dataset) + ".txt", "w+")
            byt.close()
            byteset = str(dataset) + ".txt"
            
            #Create directory to store images
            directory = str(directory)
            os.makedirs(dataset)

        break


    #Write the labels in the rows i number of times
    with open(labelset, 'a') as labelFile:
        writer = csv.writer(labelFile)
        for i in range(0, recursion):
            writer.writerow(label)


    # settings for the feed
    framewidth = 320
    frameheight = 240
    Feed = cv2.VideoCapture(0)
    Feed.set(3, framewidth)
    Feed.set(4, frameheight)

    i = total_images
    print i
    while (True):

        # the labelFile hass rows written in an appended manner, so the index of the last row should replace the 0
        # in i = 0. it should also be added to the recursion goal below...
        
        #If you have reached recursion goal, stop
        if (i == recursion + total_images):
            total_images = total_images + recursion
            break

        #Capture images recusively by recursion quantitiy
       
        #If you want to to use frames from PiCam: ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##  ##
        # comment out frame = cv2.imread('PiCam.bmp',1) and comment in ret, frame = Feed.read()
        
        #frame = cv2.imread('PiCam.bmp',1)
        ret, frame = Feed.read()

        #Write the images into the directory
        image = cv2.imwrite(str(directory) +"\%d" % i + ".jpg", frame)

        #Encode these images into byte strings
        img_str = cv2.imencode('.jpg', frame)[1].tostring()
        print img_str[0:20]

        #Write the binary strings into the byte Image Dataset            
        with open(byteset, 'a') as byteFile:
            byteFile.write(img_str)
            byteFile.close()
            
        i = i + 1
        
    print ("")
    print ("")
    return total_images
    
# the bytes are not being store properly in the csv file
# originally you had a txt file and a csv file both of which had the same name except with different.csv or .txt.
# you may need to ask the trademark vision guy what he would recommend you do in order to store the binary strings, should they be saved in a txt file, a csv file, and then how do you loop over them
# in such a way that you can seperate which strings belong to which image.
    #while (True):
     #   for j in byteset:
      #      print j
       #     nparr = np.fromstring(j, np.uint8)
        #    img = cv2.imdecode(nparr, cv2.CV_LOAD_IMAGE_COLOR)
         #   cv2.imshow('decodedimg', img)
          #  cv2.waitKey(0)

    

#=================================== Test Code ========================================= 
framewidth = 320
frameheight = 240
Feed = cv2.VideoCapture(0)
Feed.set(3, framewidth)
Feed.set(4, frameheight)

# Tells you how many images are in the dataset
total_Img = 0

while (True):
    ret, Frame = Feed.read()
    # imageDataSetGenerator("label", 50, "obstacles", "C:\Users\BirdBrain\Documents\BirdBrain Tech\obstacles\")
    ti = imageDatasetGenerator(total_Img, "Finch", 10, "obstacles", "C:\Users\Luka\Documents\BirdBrain Tech\obstacles")
    ti = imageDatasetGenerator(ti, "Cat", 10, "obstacles", "C:\Users\Luka\Documents\BirdBrain Tech\obstacles")
    ti = imageDatasetGenerator(ti, "Dog", 10, "obstacles", "C:\Users\Luka\Documents\BirdBrain Tech\obstacles")

    cv2.waitKey(1)
        
