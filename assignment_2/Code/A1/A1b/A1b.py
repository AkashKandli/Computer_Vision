import cv2
import numpy as np
from matplotlib import pyplot as plt 
import copy
  
# reads an input image 
img = cv2.imread('b2_a.png')

def filter(f):
	x = int(len(f)/2)
	n = len(img)
	m = len(img[0])
	img2 = copy.deepcopy(img)

	#horizontal filter
	for i in range(0,n):
		for j in range(x,m-x):
			sum = 0
			for a in range(0,len(f)):
				sum = sum + img[i][j-x+a][0]*f[a]
			img2[i][j][0] = int(sum)
			img2[i][j][1] = int(sum)
			img2[i][j][2] = int(sum)
	imgplot = plt.imshow(img2)
	plt.show()

	#vertical filter
	img3 = copy.deepcopy(img)
	for i in range(x,n-x):
		for j in range(0,m):
			sum = 0
			for a in range(0,len(f)):
				sum = sum + img2[i-x+a][j][0]*f[a]
			img3[i][j][0] = int(sum)
			img3[i][j][1] = int(sum)
			img3[i][j][2] = int(sum)
	imgplot = plt.imshow(img3)
	plt.show()

fil = [0.03,0.07,0.12,0.18,0.20,0.18,0.12,0.07,0.03]
filter(fil)
