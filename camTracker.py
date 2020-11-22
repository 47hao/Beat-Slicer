import numpy as np
import cv2
import os
import time

from PIL import ImageFilter

def cropImage(image, topBorder, leftBorder):
    height, width, x = image.shape
    crop_img = image[topBorder:height-topBorder, leftBorder:width-leftBorder]
    return crop_img

def filterLight(frame, thresh):
    #idea: adaptive mask? adjust threshold automatically
    
    #also say bad lighting conditions
    lower = np.array([0,0,int(255*thresh)])
    upper = np.array([255,50,255])
    #res = cv2.bitwise_and(frame,frame, mask= mask) colored mask
    
    #mask brightest parts
    #from: pythonprogramming.net/color-filter-python-opencv-tutorial/
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lower, upper)

    #filter mask
    #https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
    kernel = np.ones((5,5),np.uint8)
    #opening = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    opening = mask
    return opening

#returns (x,y) or None
def findLargestLight(im):
    #from: https://docs.opencv.org/master/dd/d49/tutorial_py_contour_features.html
    #1 = return as list no hierarchy, 2nd param is approx mode
    contours,hierarchy = cv2.findContours(im, 1, 1)

    #find largest contour
    maxArea = 0
    foundContour = False
    for cnt in contours:
        if(len(cnt) > 8): #dont bother with single points
            area = cv2.contourArea(cnt)
            if area > maxArea:
                maxArea = area
                largestContour = cnt
                foundContour = True

    if(not foundContour):
        return None

    M = cv2.moments(largestContour) #find centroid
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    return cx/im.shape[1], cy/im.shape[0]

class camTracker(object): #WORKING ON THIS
    def __init__(self):
        self.cap = cv2.VideoCapture(0)
        self.debugImage = None
        self.showFilter = False
    
    def getCoords(self, threshold):
        #print(threshold)
        ret, frame = self.cap.read()
        #frame = cropImage(frame, 0, 0)
        filtered = filterLight(frame, threshold)#process data
        #self.debugImage = filtered
        if self.showFilter:
            cv2.imshow('mask',filtered)
            cv2.imshow('frame',frame)
        return findLargestLight(filtered)
        #addons
        #frame = drawInterface(frame, testBool, capturing)
        #frame150 = rescale_frame(frame, percent=150)
    
    def toggleFilter(self):
        self.showFilter = not(self.showFilter)

    def getDebugMask(self):
        if(self.debugImage != None):
            return self.debugImage
        return None

def rescaleFrameTarget(frame, width, height):
    if(width/height) > frame.shape[1]/frame.shape[0]: #target is wider
        ratio = width/frame.shape[1]
    else:
        ratio = height/frame.height[0]
    return rescaleFrame(frame, ratio*100)
    
def rescaleFrame(frame, percent=50):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

#for static testing
#===============================================================================
def run():
    # is the camera capturing an image
    capturing = False
    cap = cv2.VideoCapture(0)
    threshold = 0.9

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        #frame = cropImage(frame, 0, 0)
        filtered = filterLight(frame, threshold)#process data
        print(findLargestLight(filtered))
        #Display
        cv2.imshow('frame',frame)
        cv2.imshow('mask',filtered)
        #Check for key actions
        k = cv2.waitKey(1)
        up = 105 #i
        down = 111 #o
        if k%256 == up:
            if(threshold <= 0.95):
                threshold += .05
        elif k%256 == down:
            if(threshold >= 0.55):
                threshold -= .05
        elif(k%256 == 113): #q quits
            break
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
#run()


