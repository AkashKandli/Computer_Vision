import cv2
import numpy as np
import math

l1 = []
l2 = []

def main():
    img1 = cv2.imread("1.jpg")
    img2 = cv2.imread("2.jpg")

    cv2.imshow('Test', img1)
    cv2.setMouseCallback("Test", click_event)
    cv2.waitKey(0)

    cv2.imshow('Test', img2)
    cv2.setMouseCallback("Test", click_event2)
    cv2.waitKey(0)

    a = affine3()
    transformNN(img1,a)

    a = affine()
    transformNN(img1,a)
    
#record clicks on the first image
def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        l = [x,y]
        l1.append(l)

#record clicks on the second image
def click_event2(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        l = [x,y]
        l2.append(l)


#calculate affine matrix for the 3 landmarks
def affine3():
    m = [l2[0][0],l2[0][1],l2[1][0],l2[1][1],l2[2][0],l2[2][1]]
    m = np.array(m)
    matrix = [[l1[0][0],l1[0][1],1,0,0,0],
         [0,0,0,l1[0][0],l1[0][1],1],
         [l1[1][0], l1[1][1], 1, 0, 0, 0],
         [0, 0, 0, l1[1][0], l1[1][1], 1],
         [l1[2][0], l1[2][1], 1, 0, 0, 0],
         [0, 0, 0, l1[2][0], l1[2][1], 1]]
    matrix = np.array(matrix)
    matrix = np.linalg.inv(matrix)
    a = np.dot(matrix,m)

    return a

#calculate affine matrix for any number of landmarks
def affine():
    m = []
    for i in range(len(l2)):
        m.append(l2[i][0])
        m.append(l2[i][1])
    m = np.array(m)

    matrix = []
    for i in range(0, len(l1)):
        matrix.append([l1[i][0],l1[i][1],1,0,0,0])
        matrix.append([0,0,0,l1[i][0], l1[i][1], 1])
    matrix = np.array(matrix)
    matrix = np.linalg.pinv(matrix)
    a = np.dot(matrix, m)

    return a


#use nearest neighbor to plot the resulting image
def transformNN(img, a):
    matrix = [[a[0], a[1], a[2]],
              [a[3], a[4], a[5]],
              [0, 0, 1]]
    m = img.shape[0]
    n = img.shape[1]
    img2 = np.zeros((m, n, 3), np.uint8)
    matrix = np.linalg.inv(matrix)
    for i in range(m):
        for j in range(n):
            res = np.dot(matrix,np.array([i,j,1.0]))
            for k in range(2):
                if res[k]%1.0 < 0.5:
                    res[k] = math.floor(res[k])
                else:
                    res[k] = math.ceil(res[k])
            if res[0] >= 0 and res[0] < m and res[1] >= 0 and res[1] < n:
                img2[i, j] = img[int(res[0]), int(res[1])]
            else:
                img2[i, j] = [0,0,0]
    cv2.imshow("image", img2)
    cv2.waitKey(0)


main()