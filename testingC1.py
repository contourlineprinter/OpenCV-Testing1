import numpy as np
import cv2
import matplotlib.pyplot as plt

# load in image
picUsed = "1.jpg"               # picture 
img = cv2.imread(picUsed, 0)    # read in image grayscale

#-----------------------------------------

# Gaussian Blur
blur = cv2.GaussianBlur(img,(5,5),0)

# adaptive threshold
# image, max pixel value, type of threshold,
# neighborhood parameter indicating how far or what the localization of where the adaptive thresholding will act over,
# mean subtraction from the end result
# only the threshold picture
thres_adapt = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 295, 1)

# Taking a matrix of size 5 as the kernel 
kernel = np.ones((5,5), np.uint8) 

#dilation
img_dil = cv2.dilate(thres_adapt, kernel, iterations=1)
cv2.imshow("Dilation", img_dil)

#erosion
img_ero = cv2.erode(img_dil, kernel, iterations=1)
cv2.imshow("Erosion", img_ero)

#-----------------------------------------

# canny edge detection
edges = cv2.Canny(img_ero,100,200)

# find countour
contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

print("Found %d objects." % len(contours)) # length of the contour list

# set up things for processing points in contour
x = []
y = []
pointC = []
xsave = -1
ysave = -1
count = 0

range = 50 # range - change to get different number of points

# process points in contour - remove some
for i in contours:
    for j in i:
        for k in j:           
            xget = k[0] #get x
            yget = k[1] #get y
            #print(xget)
            #print(yget)

            # if x and y found is within range of saved x and y, don't save it
            if (abs(xsave-xget) <= range) or xget == xsave:
                #print("got here - no")
                continue
            elif (abs(ysave-yget) <= range) or yget == ysave:
                #print("got here - no")
                continue
            else:
                #print("got here - yes")
                xsave = xget
                ysave = yget
                pointC.append(k)
                count+=1

print(xsave) # last save x
print(ysave) # last save y
print(count) # number of points


height, width = img.shape[:2]   # get image size

vec = np.array([pointC])        # make a numpy array with the new points for contour image


#don't sort - doesn't work?
#vec = np.sort(np.array([pointC]))

# draw the new contour image
img4 = 255*np.ones((height, width, 3), np.uint8)        # make blank canvas
iwcv = cv2.drawContours(img4, vec, -1, (0,255,0), 2)    # draw the contour image with new point (2 at the end is line thickness)


#-----------------------------------------
# this is the contours found with the unprocessed points

img2 = img.copy()                                           # make copy of image
img3 = 255*np.ones((height, width, 3), np.uint8)            # make blank canvas
iwc = cv2.drawContours(img3, contours, -1, (0,255,0), 3)    # draw contour
# 0, 255, 0 is the color
# 3 at the end is thickness

#-----------------------------------------


# show original image and final contour image with matplotlib
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])

plt.subplot(122),plt.imshow(iwcv,cmap = 'gray')
plt.title('Vector Image'), plt.xticks([]), plt.yticks([])

plt.show()
