import numpy as np
import cv2
import matplotlib.pyplot as plt
import os, sys
from ImageConversionClass import ImageConversion

#-----------------------------------------         
#image = "2.png"
image = "2.jpg"
#image = "water.jpg"
svg = "./"

# create an ImageConversion object
imgConvert = ImageConversion(image, svg)

# print class documentation
#print ("ImageConversion.__doc__:", ImageConversion.__doc__)

# print info
imgConvert.printImgInfo()

# load in image
#imgGray = imgConvert1.readImageGrayscale(image) # turn on for regular
img = imgConvert.readImageOriginal(image) # turn on for background removal

# show image
#imgConvert1.showImage("Original Image", img)

# get image ready
#eroImg = imgConvert1.getImageReady(imgGray)     # regular
eroImg = imgConvert.getImageReadyNoBackground(img) # background removal - need orig image
imgResize = imgConvert.resizeImageByHeightAndWidth(eroImg, None, None, desiredImgHeight = 400, desiredImgWidth = None)


# find contour lines
conImgNoEdgeOld, conImgNoEdge, conNoEdgePoints = imgConvert.createContours(imgResize)

# compare three images - original, edges found, final contour image 
#imgConvert1.showThreeImages(img, conImgNoEdgeOld, conImgNoEdge, "Original", "Edges Found", "Final Contour")

# close all windows
#imgConvert1.closeAllWindows()

#-----------------------------------------
