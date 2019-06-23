import cv2
import numpy as np
from matplotlib import pyplot as plt 
import copy
import math

image = cv2.imread('source_image.png')
key = cv2.imread('crop3.png')

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
key = cv2.cvtColor(key, cv2.COLOR_BGR2GRAY)

cv2.imshow("image", image)
cv2.waitKey(0)
cv2.imshow("image", key)
cv2.waitKey(0)


level = 180

def binary(img):
	for i in range(img.shape[0]):
		for j in range(img.shape[1]):
			if img[i, j] > level:
				img[i, j] = 0
			else:
				img[i, j] = 255
	return img

image = binary(image)
key = binary(key)

cv2.imshow("image", image)
cv2.waitKey(0)
cv2.imshow("image", key)
cv2.waitKey(0)


#create template
template = np.zeros((key.shape[0],key.shape[1]))

for i in range(key.shape[0]):
	for j in range(key.shape[1]):
		if key[i, j] == 0:
			template[i, j] = -1
		else:
			template[i, j] = 1

			

#corelate
x = key.shape[0]//2
y = key.shape[1]//2
n = image.shape[0]
m = image.shape[1]

con_image = np.zeros((n,m))

for i in range(x, n-x):
	for j in range(y, m-y):
		value = np.multiply(key, image[ (i-x) : (i+x), (j-y) : (j+y+1)])
		v = np.sum(value)
		con_image[i, j] = v


maximum = np.max(con_image)
minimum = np.min(con_image)
r = maximum - minimum

fin_image = np.zeros((n,m))

for i in range(n):
	for j in range(m):
		a = con_image[i, j]
		a = a + minimum
		a = a*255//r
		fin_image[i, j] = a
		if a == 255:
			print ("peak is at (",i,",",j,")")


final = []
for i in range(fin_image.shape[0]):
	final.append([])
	for j in range(fin_image.shape[1]):
		final[i].append([])
		final[i][j].append(int(abs(fin_image[i, j])))
		final[i][j].append(int(abs(fin_image[i, j])))
		final[i][j].append(int(abs(fin_image[i, j])))

imgplot = plt.imshow(final)
plt.show()



