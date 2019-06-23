import cv2
import numpy as np
from matplotlib import pyplot as plt 
import copy

# reads an input image 
img = cv2.imread('b2_a.png')

def filter(k):
	x = int(k/2)
	n = len(img)
	m = len(img[0])
	img2 = copy.deepcopy(img)
	#for every pixel other than the border pixels apply the filter
	for i in range(x,n-x):
		for j in range(x,m-x):
			sum = 0
			for a in range(0,k):
				for b in range(0,k):
					sum = sum + img[i-x+a][j-x+b][0]
			img2[i][j][0] = int(sum/(k*k))
			img2[i][j][1] = int(sum/(k*k))
			img2[i][j][2] = int(sum/(k*k))
	imgplot = plt.imshow(img2)
	plt.show()

#filter of kernel size 3
filter(3)

#filter of kernel size 5
filter(5)
