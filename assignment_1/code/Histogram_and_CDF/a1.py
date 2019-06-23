import cv2
import numpy as np
from matplotlib import pyplot as plt 
  
# reads an input image 
img = cv2.imread('b1.png') 

colors = ['#ff0000','#00ff00','#0000ff']
count = []
l = []
for i in range(256):
	count.append(0)
	l.append(i)

fig, ax = plt.subplots(1,3, sharey=True)

# find frequency of pixels in range 0-255 and create bar graphs
for i in range(0,3):
	for j in range(len(img)):
		for k in range(len(img[0])):
			x = img[j][k][i]
			count[x] = count[x]+1
	ax[i].bar(l, count, color = colors[i])
plt.show()

#create black and white image
img2 = []
for i in range(0, len(img)):
	img2.append([])
	for j in range(0, len(img[i])):
		img2[i].append([])
		s = 0.0
		s = round(img[i][j][0] * 0.3 + img[i][j][1] * 0.59 + img[i][j][2] * 0.11)
		img2[i][j].append(int(s))
		img2[i][j].append(int(s))
		img2[i][j].append(int(s))
img2 = np.array(img2)

#find frequency in B&W image
count2 = []
for i in range(256):
	count2.append(0)
for j in range(len(img2)):
	for k in range(len(img2[0])):
		x = img2[j][k][0]
		count2[x] = count2[x]+1

#plot B&W image
plt.bar(l, count2, color = '#bbbbbb')
plt.show()

#print B&W image	
imgplot = plt.imshow(img2)
plt.show()


#calculate pdf
pdf_count = []
pixels = len(img)*len(img[0])
cdf_count = []
for i in range(256):
	pdf_count.append(count2[i]/pixels)

#plot PDF
plt.plot(l, pdf_count)
plt.show()

#calculate cdf
cdf_count.append(pdf_count[0])
for i in range(1,256):
	cdf_count.append(cdf_count[i-1]+pdf_count[i])

#plot CDF
plt.plot(l, cdf_count)
plt.show()

#Histogram Equalization

H = count2
f = 0
gmin = -1
for i in range(0, 256):
	if f == 0:
		if H[i] > 0:
			gmin = i
			f = 1
	else:
		if H[i] < H[gmin]:
			gmin = i


cumulative_count = []
cumulative_count.append(count2[0])
for i in range(1,256):
	cumulative_count.append(cumulative_count[i-1]+count2[i])

Hmin = cumulative_count[gmin]


T = []
for i in range(256):
	T.append(0)

for i in range(256):
	num = (cumulative_count[i] - Hmin)*255
	den = pixels - Hmin
	T[i] = round(num/den)



#equalize image
img3 = []
for i in range(0, len(img)):
	img3.append([])
	for j in range(0, len(img[i])):
		img3[i].append([])
		s = T[img2[i][j][0]]
		img3[i][j].append(int(s))
		img3[i][j].append(int(s))
		img3[i][j].append(int(s))
img3 = np.array(img3)

#print equalized image	
imgplot = plt.imshow(img3)
plt.show()

#find frequency in equalized image
count3 = []
for i in range(256):
	count3.append(0)
for j in range(len(img3)):
	for k in range(len(img3[0])):
		x = img3[j][k][0]
		count3[x] = count3[x]+1

#plot equalized image
plt.bar(l, count3, color = '#bbbbbb')
plt.show()





