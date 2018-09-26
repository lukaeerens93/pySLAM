import matplotlib.pyplot as plt
import numpy as np


def mapper(locationList):
    points = np.array([[150,200], [-150,200], [150,0], [-150,0]] + locationList)
    print points
    from scipy.spatial import Delaunay
    tri = Delaunay(points)
    xcentroids = []
    ycentroids = []
    centroids = []

    #Current location of robot
    xcentroids.append(0)
    ycentroids.append(0)
    centroids.append([0,0])


    graph = {}
    for i in range(0, len(points[tri.simplices])):
        
        #x coordinate of delaunay constraint nodes
        a = points[tri.simplices][i][2][0]
        #y coordinate of delaunay constraint nodes
        b = points[tri.simplices][i][2][1]
        #Midpoint coordinate between 2 delaunay nodes
        c = (points[tri.simplices][i][0] + points[tri.simplices][i][1])/2


        #center coordinate of delaunay triangle
        centroid = [a + 2*(c[0] - a)/3, b + 2*(c[1] - b)/3]
        centroids.append(centroid)
        xcentroids.append(centroid[0])
        ycentroids.append(centroid[1])
        
        graph.update({str(i):(tri.neighbors[i])})

        #The last items on the list are giant negative numbers
        #This is used because later calling centroids[-1] actually goes to 
        #the end of the list whereas if the neighbor index is -1, it means  
        #that there is no neighbor and thus no centroid for that neighbor

    centroids.append([-999,-999])

    #Draw triangulations for all contraint points
    plt.triplot(points[:,0], points[:,1], tri.simplices.copy())
    plt.plot(points[:,0], points[:,1], 'o')
    #Plot the center coordinate of the triangles
    plt.plot(xcentroids, ycentroids, 'o')

    return points, tri, xcentroids, ycentroids, centroids, graph






def nodeWebDictionary(Points, Triangle, Centroids, Graph):
    #Centroid distance dictionary
    Dict_of_centDistDict = {}

    # Create a list of all the nodes (this is used later by Dijkstra's algorithm)
    nodes = list()

    #Now Find the Distance Between Centroid Nodes to employ in Dijkstra Algorithm
    import math
    for j in range(0, len(Points[Triangle.simplices])):
        nodes.append(str(j))

        #Centroid of current triange + 3 Possible Neighboring Triangles (A,B and C)for each triangle
        centLocal = Centroids[j]
        neighborA = Graph[str(j)][0]
        neighborB = Graph[str(j)][1]
        neighborC = Graph[str(j)][2]
        centA = Centroids[neighborA]
        centB = Centroids[neighborB]
        centC = Centroids[neighborC]


        if (centA == [-999,-999]):
            #Pythagoras
            distB = math.sqrt((centLocal[0]-centB[0])*(centLocal[0]-centB[0]) + (centLocal[1]-centB[1])*(centLocal[1]-centB[1]))
            distC = math.sqrt((centLocal[0]-centC[0])*(centLocal[0]-centC[0]) + (centLocal[1]-centC[1])*(centLocal[1]-centC[1]))        
            #Dictionary of dictionaries for distance for each neighbor node of each node
            Dict_of_centDistDict[str(j)] = {}
            Dict_of_centDistDict[str(j)][str(neighborB)] = distB
            Dict_of_centDistDict[str(j)][str(neighborC)] = distC


        if (centB == [-999,-999]):
            distA = math.sqrt((centLocal[0]-centA[0])*(centLocal[0]-centA[0]) + (centLocal[1]-centA[1])*(centLocal[1]-centA[1]))
            distC = math.sqrt((centLocal[0]-centC[0])*(centLocal[0]-centC[0]) + (centLocal[1]-centC[1])*(centLocal[1]-centC[1]))        
            Dict_of_centDistDict[str(j)] = {}
            Dict_of_centDistDict[str(j)][str(neighborA)] = distA
            Dict_of_centDistDict[str(j)][str(neighborC)] = distC


        if (centC == [-999,-999]):
            distA = math.sqrt((centLocal[0]-centA[0])*(centLocal[0]-centA[0]) + (centLocal[1]-centA[1])*(centLocal[1]-centA[1]))
            distB = math.sqrt((centLocal[0]-centB[0])*(centLocal[0]-centB[0]) + (centLocal[1]-centB[1])*(centLocal[1]-centB[1]))        
            Dict_of_centDistDict[str(j)] = {}
            Dict_of_centDistDict[str(j)][str(neighborA)] = distA
            Dict_of_centDistDict[str(j)][str(neighborB)] = distB


        elif(centA != [-999,-999] and centB != [-999,-999] and centC != [-999,-999]):
            distA = math.sqrt((centLocal[0]-centA[0])*(centLocal[0]-centA[0]) + (centLocal[1]-centA[1])*(centLocal[1]-centA[1]))
            distB = math.sqrt((centLocal[0]-centB[0])*(centLocal[0]-centB[0]) + (centLocal[1]-centB[1])*(centLocal[1]-centB[1]))
            distC = math.sqrt((centLocal[0]-centC[0])*(centLocal[0]-centC[0]) + (centLocal[1]-centC[1])*(centLocal[1]-centC[1]))
            Dict_of_centDistDict[str(j)] = {}
            Dict_of_centDistDict[str(j)][str(neighborA)] = distA
            Dict_of_centDistDict[str(j)][str(neighborB)] = distB
            Dict_of_centDistDict[str(j)][str(neighborC)] = distC

    for y in range(0, len(nodes)):
        print (str(y) + ": " + str(Dict_of_centDistDict[str(y)]))
    print nodes
    return Dict_of_centDistDict, nodes






def dijkstra(Points, Triangle, Nodes, graph, end):

    distList = []           #contains shortest accumulated distance to each node
    targetList = []         #fills visited nodes with 99999 so as to find the minimum total distance of any unvisited nodes
    precedingList = []      #precedingList[2] = previous node (in shortest path) that connects to node 2   
    currentNode = '0'
    combinedDist = 0
    visited = []            #list of all visited nodes
    path = []               #nodes which constitute the shortest path are appended here
    shortestPath = []       #This returns the list of nodes that form shortest path FOR each node
    
    # Fill all distances to infinity (except for starting node which is distance of 0)
    distList.append(combinedDist)
    targetList.append(combinedDist)
    # Fill all preceding node list as None
    precedingList.append(currentNode)


    for i in range (1, len(Points[Triangle.simplices])):
        distList.append(999999)     #Big number like infinity
        targetList.append(999999)
        precedingList.append(None)


    while True:
        for neighbour, distance in graph[currentNode].items():
            if neighbour not in visited:
                
                previousNode = precedingList[int(currentNode)]
                #print ("neighbour" + str(neighbour))
                #print ("previousNode = " + str(previousNode))
                #print ("distList[int(previousNode)] = " + str(distList[int(previousNode)]))
                combinedistance = distance + distList[int(currentNode)]
                #print ("combined distance: " + str(combinedistance))

                # If total distance to get there is smaller than current total distance to get there
                if combinedistance < distList[int(neighbour)] and neighbour not in visited:
                    distList[int(neighbour)] = combinedistance
                    targetList[int(neighbour)] = combinedistance                
                    precedingList[int(neighbour)] = currentNode
                    

                # When done with finding distances for neighbours, list the currentNode as visited
            if currentNode not in visited:
                visited.append(currentNode)
                    #print ("len(visited): " + str(len(visited)))
                #print (len(Points[Triangle.simplices]))


        # The currentNode that will be checked next will be the one with smallest total distance THAT HAS NOT
        # BEEN VISITED YET! So create seperate list that is equal to distList but where you replace the values
        # of visisted nodes with 99999, to find the shortest combine distance out of all none visisted nodes
        
        if (len(visited) != len(Points[Triangle.simplices])):
            for j in visited:
                targetList[int(j)] = 999999

        #print ("str(distList)" + str(distList))
        #print ("str(targetList)" + str(targetList))
        closest = min(targetList[1:])
        currentNode = str(distList.index(closest))
        
        #print ("visited: " + str(visited))
        #print ("len(visited): " + str(len(visited)))
        
        if (len(visited) == len(Points[Triangle.simplices])):
            break
        #if currentNode == str(end): 
         #   break

            
    # Now find the node order for the shortest path
    for k in range (0, len(Points[Triangle.simplices])):
        #print ("k: " + str(k))
        path.append(str(k))
        while True:
            
            p = str(precedingList[k])
            print p
            path.append(p)
            if (p != str(0)):
                
                k = int(p)
            else:
                #print ("Zero has been reached")
                break
        print ("Optimal Reverse path to this node is: ",path)
        shortestPath.append(path[:])
        #print ("Shortest Path: " + str(shortestPath))
        #print ("")
        path[:] = []

    return Nodes, distList, precedingList, shortestPath[end]#you only need the shortest path for the end node    





#def pathOptimizer():
 #   print ("pathOptimizer Initiated")





def shortestPathConnector(Path, Centroids):
    nodeXList = []
    nodeYList = []
    for b in Path:
        nodeXList.append(Centroids[int(b)][0])
        nodeYList.append(Centroids[int(b)][1])
    plt.plot(nodeXList, nodeYList, '-r')    
    Path[:] = []




    
def pointReset(Points):
    # When the perspective of the robot changes, you want to get a fresh new chart to plot 
    # the corners contraints, so delete the ones that you had in the previous timestep
    Points = np.array([[150,200], [-150,200], [150,0], [-150,0]])



#================================ Test Script ===========================================
chartShowIndex = 0
AList = [[20,34], [-15,38], [11,47], [-8,22]]
print ("AList: " + str(AList))
extra = 0

while True:
    
    p,t,x,y,c,g = mapper(extra)
    d,n = nodeWebDictionary(p,t,c,g)
    nodes, shortestTotalDist2Node, precedingNode, short = dijkstra(p,t,n, d, 1)

    shortestPathConnector(short, c)
    chartShowIndex = chartShowIndex + 1
    plt.show(block = False)     #block = false otherwise display of plt prevents code from continuing computation

    if chartShowIndex % 5 == 0:
        plt.close()

    pointReset(p)

