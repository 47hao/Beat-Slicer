import numpy as np
import cv2
import os
import time

def drawInterface(image, testBool, capturing):
    
    try:
        if(image == None):
            return
    except:
        pass

    height, width, x = image.shape
    indicatorHeight = height//35

    if(testBool):
        color = (50,210,50)
    else:
        color = (30,30,200)

    cv2.rectangle(image, (0, 0), (width, indicatorHeight), color, -1)

    if (capturing):
        s_img = cv2.imread("faceOverlayCornersGreen.png", -1)
    else:
        s_img = cv2.imread("faceOverlayFull.png", -1)

    x_offset=y_offset=0

    y1, y2 = y_offset, y_offset + s_img.shape[0]
    x1, x2 = x_offset, x_offset + s_img.shape[1]

    alpha_s = s_img[:, :, 3] / 255.0
    alpha_l = 1.0 - alpha_s

    for c in range(0, 3):
        image[y1:y2, x1:x2, c] = (alpha_s * s_img[:, :, c] +
                              alpha_l * image[y1:y2, x1:x2, c])

    return image

def cropImage(image, topBorder, leftBorder):
    height, width, x = image.shape
    crop_img = image[topBorder:height-topBorder, leftBorder:width-leftBorder]
    return crop_img

def run():
    # is the camera capturing an image
    capturing = False

    cap = cv2.VideoCapture(0)
    
    testBool = False

    #for naming the images in the image folder
    img_counter = 0

    counter=0

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Frame Operations
        frame = drawInterface(frame, testBool, capturing)
        #frame150 = rescale_frame(frame, percent=150)
        frame = cropImage(frame, 0, 0)

        #Show frame
        cv2.imshow('frame',frame)

        if (capturing):
            counter+=1
            
        if(counter>50):
            capturing=False
            counter=0

        #Check for key actions
        k = cv2.waitKey(1)
        if(k%256 == 32):
            testBool = not(testBool)
        elif(k%256 == 113):
            break
        elif k%256 == ord('f'):
            # SPACE pressed
            capturing = True
            img_name = "opencv_frame_{}.png".format(img_counter)
            path = "C:/Users/Daniel/Desktop/CMUHacks/cmu-hacks20/images"
            cv2.imwrite(os.path.join(path, img_name), frame)
            print("{} written!".format(img_name))
            img_counter += 1

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()

def rescale_frame(frame, percent=75):
    width = int(frame.shape[1] * percent/ 100)
    height = int(frame.shape[0] * percent/ 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation =cv2.INTER_AREA)

run()


