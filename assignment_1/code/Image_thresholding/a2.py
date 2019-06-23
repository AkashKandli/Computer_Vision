import cv2
import numpy as np
from matplotlib import pyplot as plt

count_hist = []
for i in range(0,256):
	count_hist.append(0)


def print_img(img,threshold):
	img2 = []
	for i in range(0,256):
		count_hist[i] = 0

	for j in range(len(img)):
		img2.append([])
		for k in range(len(img[0])):
			img2[j].append([])
			for i in range(0,3):
				if img[j][k][i] > threshold:
					img2[j][k].append(255)
					count_hist[255] = count_hist[255]+1
				else:
					img2[j][k].append(0)
					count_hist[0] = count_hist[0]+1

	imgplot = plt.imshow(img2)
	plt.show()


def print_hist(l):
	plt.bar(l, count_hist)
	plt.show()

imgarr = []
imgarr.append(cv2.imread('b2_a.png'))
imgarr.append(cv2.imread('b2_b.png'))
imgarr.append(cv2.imread('b2_c.png'))

for i in range(3):
	img = imgarr[i]
	#binarization with 25% threshold
	print_img(img, 63)
	#binarization with 50% threshold
	print_img(img, 127)
	#binarization with 75% threshold
	print_img(img, 191)

	#Otsu method to find threshold
	count = []
	bin_values = []
	for i in range(256):
		count.append(0)
		bin_values.append(i)

	for i in range(len(img)):
		for j in range(len(img[0])):
			count[img[i][j][0]] = count[img[i][j][0]]+1
	total = len(img)*len(img[0])

	#we find the threshold value and store it as level
	sumB = 0
	wB = 0
	maximum = 0
	level = 0
	var = []
	sum1 = np.dot(bin_values, count);
	for i in range(0,256):
		wB = wB+count[i]
		wF = total - wB
		if (wB == 0 or wF == 0):
			var.append(0)
			continue
		sumB = sumB + (i)*count[i]
		mF = (sum1 - sumB)/wF
		bet = wB*wF*((sumB/wB)-mF)*((sumB/wB)-mF)
		var.append(bet)
		if (bet >= maximum):
			level = i
			maximum = bet
	print("inter-class variance:")
	print(maximum)

	#binarization with threshold got from Otsu's method
	print_img(img, level)

	#finding the variance for the image
	l = []
	for i in range(256):
		l.append(i)
	plt.plot(l, var)
	plt.show()
	print ("Chosen Threshold:")
	print (level)
	print_hist(l)
