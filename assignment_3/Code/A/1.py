import cv2
import numpy as np
import math

def main():

    img = cv2.imread("pic2.jpg")

    #define scaling matrix for transformation
    scale = np.array([[1.01, 0, 0],
                      [0, 1.01, 0],
                      [0, 0, 1]])

    #define translation matrix for transformation
    trans = np.array([[1, 0, 30],
                      [0, 1, 30],
                      [0, 0, 1]])

    #define rotational matrix for transformation with rotation of 15 degrees
    cos = math.pow(3, 0.5)
    sin = 0.5
    rot = np.array([[cos, sin, 0],
                    [-sin, cos, 0],
                    [0, 0, 1]])
    matrix = np.dot(rot, trans)
    matrix = np.dot(scale, matrix)

    transformNN(img, matrix)
    transformBL(img, matrix)

#apply transformation and apply nearest neighbor transformation to plot the image
def transformNN(img, matrix):
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
    cv2.imshow("Nearest Neighbor", img2)
    cv2.waitKey(0)


#apply transformation and apply Bilinear transformation to plot the image
def transformBL(img, matrix):
    m = img.shape[0]
    n = img.shape[1]
    img2 = np.zeros((m, n, 3), np.uint8)
    matrix = np.linalg.inv(matrix)
    for i in range(m):
        for j in range(n):
            res = np.dot(matrix,np.array([i,j,1.0]))
            fourpx = []
            fourpx.append(img[int(math.floor(res[0])), int(math.floor(res[1]))])
            fourpx.append(img[int(math.ceil(res[0])), int(math.floor(res[1]))])
            fourpx.append(img[int(math.floor(res[0])), int(math.ceil(res[1]))])
            fourpx.append(img[int(math.ceil(res[0])), int(math.ceil(res[1]))])
            twopx = []
            x1 = res[0]%1.0
            x2 = 1 - x1
            y1 = res[1]%1.0
            y2 = 1 - y1
            twopx.append(np.array((x1*fourpx[1] + x2*fourpx[0]),np.uint8))
            twopx.append(np.array((x1*fourpx[3] + x2*fourpx[2]),np.uint8))
            px = np.array((y1*twopx[1] + y2*twopx[0]),np.uint8)
            if res[0] >= 0 and res[0] < m and res[1] >= 0 and res[1] < n:
                img2[i, j] = px
            else:
                img2[i, j] = [0,0,0]
    cv2.imshow("Bilinear", img2)
    cv2.waitKey(0)


main()


