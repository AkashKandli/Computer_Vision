import numpy as np
import cv2
import circles as circ
import time 
from numba import jit




x = time.time()
image = cv2.imread('./many_circles.png', 0)
image = cv2.medianBlur(image,3)
# cv2.imshow('image', image)
# cv2.waitKey(0)



# detect edges using Canny or some other method
# edges = cv2.Canny(image, 2000, 5000, apertureSize=5)
# print(edges[100][100])

# @jit(nopython=True) 
circles = circ.HoughTransformCircleOptimized(image, 10, 70, 20)

color = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
print(len(circles))

for c in circles:
    # print("Radius:{}".format(c.r))
    # draw the outer circle
    cv2.circle(color, (c.x, c.y), c.r, (0, 255, 0), 2)
    # draw the center of the circle
    cv2.circle(color, (c.x, c.y), 2, (0, 0, 255), 3)



timeV = time.time() - x
print("time here->", timeV)
cv2.imshow('circles', color)

cv2.waitKey(0)

cv2.destroyAllWindows()