import cv2
import numpy as np
from matplotlib import pyplot as plt 
import copy
  
# reads an input image 
img = cv2.imread('b2_a.png')
img2 = copy.deepcopy(img)

def gausianfilter(f):
	x = int(len(f)/2)
	n = len(img)
	m = len(img[0])	
	img9 = copy.deepcopy(img)

	#horizontal filter
	for i in range(0,n):
		for j in range(x,m-x):
			sum = 0
			for a in range(0,len(f)):
				sum = sum + img[i][j-x+a][0]*f[a]
			img9[i][j][0] = int(sum)
			img9[i][j][1] = int(sum)
			img9[i][j][2] = int(sum)

	#vertical filter
	for i in range(x,n-x):
		for j in range(0,m):
			sum = 0
			for a in range(0,len(f)):
				sum = sum + img9[i-x+a][j][0]*f[a]
			img2[i][j][0] = int(sum)
			img2[i][j][1] = int(sum)
			img2[i][j][2] = int(sum)

#LAplacian filter
def filter():
	f = [[0,-1,0],[-1,4,-1],[0,-1,0]]
	x = 1
	n = len(img)
	m = len(img[0])
	img3 = np.zeros((n,m,3))
	img5 = copy.deepcopy(img)
	img7 = np.zeros((n,m,3))

	min = img2[0][0][0]
	max = img2[0][0][0]
	
	for i in range(x,n-x):
		for j in range(x,m-x):
			sum = 0
			for a in range(0,3):
				for b in range(0,3):
					sum = sum + img2[i-x+a][j-x+b][0]*f[a][b]
			img3[i][j][0] = sum
			img3[i][j][1] = sum
			img3[i][j][2] = sum

			if sum < 0:
				img5[i][j][0] = 0
				img5[i][j][1] = 0
				img5[i][j][2] = 0
				
				img7[i][j][0] = 0
				img7[i][j][1] = 0
				img7[i][j][2] = 0

			else:
				img5[i][j][0] = 255
				img5[i][j][1] = 255
				img5[i][j][2] = 255

				img7[i][j][0] = 1
				img7[i][j][1] = 1
				img7[i][j][2] = 1

			if sum > max:
				max = sum
			if sum < min:
				min = sum

	scale = min*(-1)
	r = max - min

	img4 = copy.deepcopy(img2)
	for i in range(0,n):
		for j in range(0,m):
			a = img3[i][j][0] + scale
			a = int((a*128)/r)
			img4[i][j][0] = a
			img4[i][j][1] = a
			img4[i][j][2] = a
	#LoG image
	imgplot = plt.imshow(img4)
	plt.show()

	#binarized image
	imgplot = plt.imshow(img5)
	plt.show()


	#zero crossing
	img6 = np.zeros((n,m,3))
	for i in range(2,n-1):
		for j in range(2,m-1):
			s = 0
			s = img7[i-1][j-1][0] + img7[i][j-1][0] + img7[i+1][j-1][0] + img7[i-1][j][0] + img7[i][j][0] + img7[i+1][j][0] + img7[i-1][j+1][0] + img7[i][j+1][0] + img7[i+1][j+1][0]
			if s == 9:
				img6[i][j][0] = 0
				img6[i][j][1] = 0
				img6[i][j][2] = 0
			else:
				img6[i][j][0] = 255
				img6[i][j][1] = 255
				img6[i][j][2] = 255
	imgplot = plt.imshow(img6)
	plt.show()
	
fil = [0.03,0.07,0.12,0.18,0.20,0.18,0.12,0.07,0.03]
gausianfilter(fil)

filter()



