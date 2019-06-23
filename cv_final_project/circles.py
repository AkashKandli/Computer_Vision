import numpy as np
import cv2
from numba import jit


# circle class for storing detected circle center and radius values
class Circle:
    def __init__(self, x, y, r):
        self.x = x
        self.y = y
        self.r = r

# Euclidean distance function
def distance(x1, y1, x2, y2):
    return np.sqrt((np.power((y2 - y1), 2) + np.power((x2 - x1), 2)))


def HoughTransformCircle(image, minRadius, maxRadius, threshold):
    # detect edges using Canny method
    edges = cv2.Canny(image, 2000, 3000, apertureSize=5)

    # display edge map
    cv2.imshow('edges', edges)
    cv2.waitKey(0)


    #accumulator same size as image and edges with 3rd dimesnion for radius
    height = edges.shape[0]
    width = edges.shape[1]
    acc = np.zeros((height, width, maxRadius - minRadius + 1))

    # list to store detected circles
    circles = []

    print("Check Radius Values")
    # for each edge point detected vote for a circle center
    for x in range(edges.shape[1]):
        for y in range(edges.shape[0]):
            if edges[y][x] != 0:
                for r in range(minRadius, maxRadius + 1):

                    # Lower step value in range function to get more votes, longer computation time
                    for phi in range(1, 360, 4):
                        a = int(x - r*(np.cos(phi)))
                        b = int(y - r*(np.sin(phi)))
                        if b < acc.shape[0] and a < acc.shape[1]:
                            acc[b][a][r - minRadius] += 1

    #add circles with accumulated value greater than or equal to the given threshold value
    maxACC = 0
    for x in range(acc.shape[1]):
        for y in range(acc.shape[0]):
            for r in range(minRadius, maxRadius + 1):

                if acc[y][x][r - minRadius] > maxACC:
                    maxACC = acc[y][x][r - minRadius]

                if acc[y][x][r - minRadius] >= threshold:
                    #check if theres already a circle in range so circles dont overlap
                    closeFlag = False
                    for c in circles:
                        if(distance(x, y, c.x, c.y)) < (c.r + r):
                            closeFlag = True

                    if closeFlag is False:
                        c = Circle(x, y, r)
                        circles.append(c)

    # print max accumulator value for testing purposes
    print("MaxACC:{}".format(maxACC))

    return circles




#does calculations and creates accumulator. We Use numba to make this code run faster 
@jit
def houghTransformCalculations(acc, edges, minRadius, maxRadius, threshold, dY, dX):
    for x in range(edges.shape[1]):
        for y in range(edges.shape[0]):
            if edges[y][x] != 0:
                # Calculate edge direction phi using gradient information
                phi = np.arctan2(dY[y][x],dX[y][x])

                for r in range(minRadius, maxRadius + 1):
                    aNeg = int(round(x - (r * np.cos(phi))))
                    bNeg = int(round(y - (r * np.sin(phi))))
                    aPos = int(round(x + (r * np.cos(phi))))
                    bPos = int(round(y + (r * np.sin(phi))))
                    if bNeg < acc.shape[0] and aNeg < acc.shape[1]:
                        acc[bNeg][aNeg][r - minRadius] += 1
                    if bPos < acc.shape[0] and aPos < acc.shape[1]:
                        acc[bPos][aPos][r - minRadius] += 1


    return acc



# #add circles with accumulated greater than or equal to the given threshold
# #Doesn't work 
# @jit
# def returnCircles(acc, minRadius, maxRadius, threshold):
#     circles = []
#     maxACC = 0
#     for x in range(acc.shape[1]):
#         for y in range(acc.shape[0]):
#             for r in range(minRadius, maxRadius + 1):
#                 if acc[y][x][r - minRadius] > maxACC:
#                     maxACC = acc[y][x][r - minRadius]

#                 if acc[y][x][r - minRadius] >= threshold:
#                     #check if theres already a circle in range so circles dont overlap
#                     closeFlag = False
#                     for c in circles:
#                         if(distance(x, y, c.x, c.y)) < (c.r + r):
#                             closeFlag = True

#                     if closeFlag is False:
#                         c = Circle(x, y, r)
#                         circles.append(c)


#     print("MaxACC:{}".format(maxACC))
#     return circles 



def HoughTransformCircleOptimized(image, minRadius, maxRadius, threshold):
    # detect edges using Cannymethod
    edges = cv2.Canny(image, 2000, 3000, apertureSize=5)

    # calculate derivate in x and y direction using sobel operator function to use in gradient calculation
    dX = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=-1)

    dY = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=-1)



    #accumulator same size as image and edges with 3rd dimesnion for radius
    height = edges.shape[0]
    width = edges.shape[1]
    acc = np.zeros((height, width, maxRadius - minRadius + 1))

    # list to store detected circles
    circles = []


    # print("Checking Radius Values")
    acc = houghTransformCalculations(acc, edges, minRadius, maxRadius, threshold, dY, dX)


    # add circles with accumulated greater than or equal to the given threshold
    maxACC = 0
    for x in range(acc.shape[1]):
        for y in range(acc.shape[0]):
            for r in range(minRadius, maxRadius + 1):
                if acc[y][x][r - minRadius] > maxACC:
                    maxACC = acc[y][x][r - minRadius]

                if acc[y][x][r - minRadius] >= threshold:
                    #check if theres already a circle in range so circles dont overlap
                    closeFlag = False
                    for c in circles:
                        if(distance(x, y, c.x, c.y)) < (c.r + r):
                            closeFlag = True

                    if closeFlag is False:
                        c = Circle(x, y, r)
                        circles.append(c)

    # print("MaxACC:{}".format(maxACC))
    return circles




