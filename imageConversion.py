import numpy as np
import cv2
import matplotlib.pyplot as plt

class ImageConversion:
    
    "Class to perform image conversion to contour, svg, and robot instructions\n"
#-----------------------------------------
    # constructor
    # parameters: orignal image name, orignal image path
    def __init__(self, origImgName, origImgPath):

        try:
            self.origImgName = origImgName
            self.origImgPath = origImgPath
        except:
            print(sys.exc_info()[0])
#-----------------------------------------
    # print the image information
    def printImgInfo(self):

        try:
            print("Image Name: %s\n" \
                "Image Path: %s \n" % (self.origImgName, self.origImgPath))
        except:
            print(sys.exc_info()[0])
#-----------------------------------------
    # read in an image in with original colors
    # return: original image
    def readImageOriginal(self, image):
        imgOriginal = cv2.imread(image, 1)  # read in image original colors
        return imgOriginal                      
#-----------------------------------------
    # read in an image in as grayscale
    # return: image in grayscale
    def readImageGrayscale(self, image):
        imgGray = cv2.imread(image, 0)  # read in image grayscale
        return imgGray   
#-----------------------------------------     
    # show image
    # parameters: name of the window, image to show
    def showImage(self, title, image):
        cv2.namedWindow(title, cv2.WINDOW_NORMAL)   # create a resizable window
        cv2.imshow(title, image)                    # show the image inside the window
#-----------------------------------------
    # close all windows
    def closeAllWindows(self):
        cv2.waitKey(0)      # wait till any key is press
        cv2.destroyAllWindows() # destroy all windows
#-----------------------------------------
    # show two images with matplotlib
    # paramters: image 1, image 2, image 1 window name, image 2 window name
    def showTwoImages(self, image1, image2, title1, title2):

        # convert images to RGB for matplotlib - OpenCV uses BGR
        RGB_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        RGB_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

        # display image 1
        plt.subplot(1,2,1)      # index 1 in 1 row, 2 columns
        plt.title(title1)       # set image 1 title
        plt.imshow(RGB_image1)  # set image 1
        plt.xticks(list(plt.xticks()[0]))
        plt.yticks(list(plt.yticks()[0]))

        # display image 2
        plt.subplot(1,2,2)      # index 2 in 1 row, 2 columns
        plt.title(title2)       # set image 2 title
        plt.imshow(RGB_image2)  # set image 2 
        plt.xticks(list(plt.xticks()[0]))
        plt.yticks(list(plt.yticks()[0]))

        plt.show() # show both image
#-----------------------------------------
    # show three images with matplotlib
    # paramters: image 1, image 2, image 3, image 1 window name, image 2 window name, image 3 window name
    def showThreeImages(self, image1, image2, image3, title1, title2, title3):

        # convert images to RGB for matplotlib - OpenCV uses BGR
        RGB_image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)
        RGB_image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
        RGB_image3 = cv2.cvtColor(image3, cv2.COLOR_BGR2RGB)

        # display image 1
        plt.subplot(1,3,1)      # index 1 in 2 row, 2 columns
        plt.title(title1)       # set image 1 title
        plt.imshow(RGB_image1)  # set image 1
        plt.xticks(list(plt.xticks()[0]))
        plt.yticks(list(plt.yticks()[0]))

        # display image 2
        plt.subplot(1,3,2)      # index 2 in 2 row, 2 columns
        plt.title(title2)       # set image 2 title
        plt.imshow(RGB_image2)  # set image 2 
        plt.xticks(list(plt.xticks()[0]))
        plt.yticks(list(plt.yticks()[0]))

        # display image 3
        plt.subplot(1,3,3)      # index 3 in 2 row, 2 columns
        plt.title(title3)       # set image 3 title
        plt.imshow(RGB_image3)  # set image 3
        plt.xticks(list(plt.xticks()[0]))
        plt.yticks(list(plt.yticks()[0]))

        plt.show() # show both image
#-----------------------------------------
    # preprocess the image to find better edges
    # parameter: image to process
    # return: processed image
    def getImageReady(self, image):
        
        # Gaussian Blur
        blurImage = cv2.GaussianBlur(image,(5,5),0)
        cv2.imshow("Blur Image", blurImage)

        # check if image is grayscale
        rows, columns, channels = image.shape # find shape of image

        # if channel is greater 0 - not grayscale
        if channels > 0:
            grayImage = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) # convert to grayscale
            
        # adaptive threshold
        # image, max pixel value, type of threshold,
        # neighborhood parameter indicating how far or what the localization of where the adaptive thresholding will act over,
        # mean subtraction from the end result
        # only the threshold picture
        adaptThresImage = cv2.adaptiveThreshold(grayImage, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 295, 1)
        cv2.imshow("Threshold Image", adaptThresImage)

        # Taking a matrix of size 3 as the kernel 
        kernel = np.ones((3,3), np.uint8) 

        #dilation
        dilationImage = cv2.dilate(adaptThresImage, kernel, iterations=1)
        cv2.imshow("Dilation Image", dilationImage)

        #erosion
        erosionImage = cv2.erode(dilationImage, kernel, iterations=1)
        cv2.imshow("Erosion Image", erosionImage)

        return erosionImage
#-----------------------------------------
    # find the edges using Canny edge detection
    # return: edge image
    def getEdges(self, image):
        edgeImge = cv2.Canny(image, 100, 200)
        return edgeImge
#-----------------------------------------
    # find the contour of the image based on specific range of x and y coordinates
    # range is used to filter out some points in contour image:
    #   smaller range - more points, more lines in the image 
    #   larger range - less points, less lines in the image
    # parameters: image, range for x, range for y, line thickness in pixel
    def createContours(self, image, rangeForX = 5, rangeForY = 5, lineThickness = 2):

        # find countour
        contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        print("Found %d objects in intial contour list." % len(contours)) # length of the contour list

        # set up things for processing points in contour
        x = y = pointC = []
        xsave = -1
        ysave = -1
        count = 0

        # process points in contour - remove some
        for i in contours:
            for j in i:
                for k in j:
                    xget = k[0] #get x
                    yget = k[1] #get y
                    #print(xget)
                    #print(yget)

                    # if x and y found is within range of saved x and y, don't save it
                    if (abs(xsave-xget) <= rangeForX) or xget == xsave:
                        #print("got here - no")
                        continue
                    elif (abs(ysave-yget) <= rangeForY) or yget == ysave:
                        #print("got here - no")
                        continue
                    else:
                        #print("got here - yes")
                        xsave = xget
                        ysave = yget
                        pointC.append(k)
                        count+=1

        print("Last saved x: %d" % xsave) # last save x
        print("Last saved y: %d" % ysave) # last save y
        print("Number of points in contour image: %d" % count) # number of points

        height, width = image.shape[:2]     # get image size
        newContours = np.array([pointC])            # make a numpy array with the new points for contour image

        #don't sort - doesn't work?
        #vec = np.sort(np.array([pointC]))

        # draw the contour images
        blankCanvas1 = 255*np.ones((height, width, 3), np.uint8)                                        # make blank canvas
        blankCanvas2 = 255*np.ones((height, width, 3), np.uint8)                                        # make blank canvas
        imageContourOld = cv2.drawContours(blankCanvas1, contours, -1, (0,255,0), lineThickness)        # draw the contour image with old point
        imageContourNew = cv2.drawContours(blankCanvas2, newContours, -1, (0,255,0), lineThickness)     # draw the contour image with new point

        self.showTwoImages(imageContourOld, imageContourNew, "Contour Old", "Contour New")

        return imageContourNew
    
#-----------------------------------------

# create an ImageConversion object
imgConvert1 = ImageConversion("1.jpg", "./1.jpg")

# print class documentation
print ("ImageConversion.__doc__:", ImageConversion.__doc__)

# print employee
imgConvert1.printImgInfo()

# load in image
img = imgConvert1.readImageOriginal("1.jpg")
imgGray = imgConvert1.readImageGrayscale("1.jpg")

# show image
#imgConvert1.showImage("Original Image", img)
#imgConvert1.showImage("Gray Image", imgGray)

# show two images - original and gray
#imgConvert1.showTwoImages(img, imgGray, "Original Image", "Gray Image")

# get image ready
eroImg = imgConvert1.getImageReady(img)
eroImg2 = eroImg.copy()

# find edges of image
edgeImg = imgConvert1.getEdges(eroImg)
imgConvert1.showImage("Edge Image", edgeImg)

# find contour lines using Canny edges
conImgEdge = imgConvert1.createContours(edgeImg, 6, 6)

# find contour lines not using Canny edges
conImgNoEdge = imgConvert1.createContours(eroImg2, 6, 6)

# compare two images - using edge pic and not using edge pic
imgConvert1.showThreeImages(img, conImgEdge, conImgNoEdge, "Original Image", "Contour with Canny", "Contour without Canny")

# close all windows
#imgConvert1.closeAllWindows()


