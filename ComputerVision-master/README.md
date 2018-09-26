# ComputerVision
Finch 2.0 Computer Vision API
____________________________________________________________________________________
Table of Contents:
1) OpenCV and Dependencies Installation Tutorial
2) Explanation of Files in the Repository

_____________________________________________________________________________________
1) OpenCV and Dependencies Installation Tutorial

-----------------------------------Mac----------------------------------------------

Installing Dependencies through drag and drop
In order to install python, numpy, scipy, matplotlib follow instructions in video: 
https://www.youtube.com/watch?v=-llHYUMH9Dg&t=21s

You can choose between downloading Python2 or Python3. In the above tutorial video, the website used to download python is: 
https://www.python.org/downloads/


Pip
Alternatively you could install everything using pip. This allows you to install everything from terminal as opposed to downloading things separately and dragging and dropping them into directories etc. 

a) Installing Pip
To install pip, open up terminal and enter:
```
sudo easy_install pip
```

b) Updating Pip
In order to upgrade pip, enter the following:
```
pip install -U pip
```

c) Installing Dependencies using Pip
With pip installed you can now install library dependencies for the code such as numpy, scipy and matplotlib. To do so enter the following in terminal:
```
pip install numpy
pip install scipy
pip install matplotlib
```

Installing OpenCV
The following youtube video shows how best to install opencv:
https://www.youtube.com/watch?v=37RvqZVddAw

This is a followup tutorial on how to actually implement the installed OpenCV files into XCode (in C++):
https://www.youtube.com/watch?v=OVSPfUmNyOw


-------------------------------------Windows------------------------------------------------
The following youtube video shows a step by step plan on how best to install opencv, numpy, scipy and matplotlib which are all needed in order to execute some of his code.
https://www.youtube.com/watch?v=pENBnsSCZm8

It is recommended that you follow this method using miniconda because manually installing every dependency separately requires versions that are compatible with one another and in the case of matplotlib require a whole cascade of other pre-requisite dependencies to be installed. They also need to all be organised in specific ways in directories, which could trick students who are not familiar with computer science. 

The first link that is used in the above video tutorial is the following: http://conda.pydata.org/miniconda.html

Everything follows on from this link, simply pay close attention to the video and take your time, and you will have everything functioning well!

_________________________________________________________________________________________
2) Explanation of Files in the Repository
-------------------------------------------------------------------------------------------
Geometry.py: Contains functions for detecting straight lines and edges in the camera feed (both by in the format of a trackbar manual editing function, and one when you know the correct values of the arguements. Also contains a test script that shows how to implement these functions in code.


-------------------------------------------------------------------------------------------
HSV.py: Contains functions that are all geared towards finding blobs of certain color qualities. There is a manual trackbar HSV range setting function that allows you to at runtime modify the hue, saturation and value ranges that you want to be captured. Once you have found the correct qualities, bring the object 30cm in front of the camera and press the letter q on the keyboard. The image will then freeze and in the shell you will be asked whether you want to capture any additional standalone HSV ranges. Enter either y (yes) or n (no). 

The computer will save not only the lower ranges of hue, saturation and value but the size of the blob when seen from 30cm away. 
The cross section of the blob is used for a vision based range function (cvBasedRange) later. (Note ultrasonic range finders work way better (but have to be precisely directed at the objected), as do stereoscopic camera arrangements but this vision based range finder works quite well with objects like spheres or cones.) 

There is also a blob tracking function (BlobTracker) that finds all blobs within the requested HSV ranges and based on a filter that ignores tiny noise like blobs with dimensions of your choosing, it tracks the centroid coordinate of these blobs.

Then by sampling both the range from cvBasedRange, and the xCoordinate of the centroid of the blob form BlobTracker, the function obstGraphProj is used in order to transform the location of the blob as seen by the camera into a birds eye view, representation of the world that is being mapped by the robot. There are also a bunch of little functions that are used for clearing arrays in a way that is demonstrated in a test script provided at the end. 

Included in this HSV.py function is also a path follower function that is used to detect sequential path centroids in horizontally sliced sections of the image. 


-------------------------------------------------------------------------------------------
ImageDistrubance.py: Background subtraction algorithm and follow up functions that are not complete yet. However the base function (backSubtract) does detect foreign objects that enter within the field of view of the robot provided. These work when the robot is absolutely still because it takes a reference image and then recursively subtracts each received frame from this reference image. The different areas are marked in white, whereas everything in smarked in black. 

This system will detect slight changes in lighting as differences, because literally every pixel is compared and even a slight difference is marked as white. Denoising is heavily used here to try avoid this, and work was underway in order to be able to ID each blob (in order to track them individually when there are many in the field of view). Work was not completed on this but since the code is opensource it can be further developed by the community. A test script is included to show how all of these functions can be used by students. 


-------------------------------------------------------------------------------------------
dataBuilder.py: Used to build labelled image datasets in order to train convolution neural networks. Test script is included that shows how to implement all of the functions. Work was underway to convert the images into a byte stream that is appended to a txt file but this doesn't work if more than one image is added to the dataset. However this system does create a csv label file that acts as the label file for neural networks, and it does add the images into a directory as jpg. 

You can request how many images of the object you want the computer to take, write the label, and specify in which labelset and dataset these can be added to. You can then pan the Finch around the object as the images are being captured so that you can automate image dataset building with hundreds of images in seconds. 

