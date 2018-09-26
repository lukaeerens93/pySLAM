import matplotlib.pyplot as plt
import cv2
import numpy as np

import HSV
import finchSLAM


chartShowIndex = 0
Calib = HSV.HSVManualCalib()
AList = [[20,34], [-15,38], [11,47], [-8,22]]
print ("AList: " + str(AList))
extra = 0

while True:
    center, DistanceGauger, ContourCounter = HSV.BlobTracker(Calib)
    if len(ContourCounter) > 1:
        Range = HSV.visionBasedRange(DistanceGauger, ContourCounter)
        extra = HSV.obstacleGraphProjection(center, Range, ContourCounter)
        
        if (extra != [-999,-999]):
            AList = np.array(extra)
            print ("AList" + str(AList))
        else:
            AList = np.array([])
        print ("...........................................")
        
        p,t,x,y,c,g = finchSLAM.mapper(extra)
        d,n = finchSLAM.nodeWebDictionary(p,t,c,g)
        nodes, shortestTotalDist2Node, precedingNode, short = finchSLAM.dijkstra(p,t,n, d, 1)

        finchSLAM.shortestPathConnector(short, c)
        chartShowIndex = chartShowIndex + 1
        plt.show(block = False)     #block = false otherwise display of plt prevents code from continuing computation

        if chartShowIndex % 5 == 0:
            plt.close()
            
        finchSLAM.pointReset(p)
        HSV.ArrayReset(center,Range,extra, ContourCounter)

    if (cv2.waitKey(1) & 0xFF == ord ('q')):
        break
cv2.destroyAllWindows()
