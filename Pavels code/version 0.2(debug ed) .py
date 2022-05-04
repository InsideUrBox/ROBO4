import cv2
from cv2 import setTrackbarPos
from cv2 import Canny
from matplotlib import image
import numpy as np
import math
# important libs

Redvalue = int(0)
Bluevalue= int(0)
Greenvalue= int(0)
#important variables

def nothing(x):
    pass
#for debugging createTrackbar

def Redpostion_change(x):
    if cv2.getTrackbarPos('Redmode','image') == 1:
        setTrackbarPos('Bluemode','image',0)
        setTrackbarPos('Greenmode','image',0)
def Bluepostion_change(x):
    if cv2.getTrackbarPos('Bluemode','image') == 1:
        setTrackbarPos('Redmode','image',0)
        setTrackbarPos('Greenmode','image',0)
def Greenpostion_change(x):
    if cv2.getTrackbarPos('Greenmode','image') == 1:
        setTrackbarPos('Redmode','image',0)
        setTrackbarPos('Bluemode','image',0)

#To set the other modes to be off when another mode is operating

# Open the camera
cap = cv2.VideoCapture(0) 
 
# Create a window
cv2.namedWindow('image')
 
# create trackbars for each colour mode with call backs to make the other modes be off
cv2.createTrackbar('Redmode','image',Redvalue,1,Redpostion_change)
cv2.createTrackbar('Bluemode','image',Bluevalue,1,Bluepostion_change)
cv2.createTrackbar('Greenmode','image',Greenvalue,1,Greenpostion_change)


while(True):
    ret, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    if Redvalue ==1:
        lower_hsv = np.array([0, 50, 50])
        higher_hsv = np.array([10, 255, 255])
        mask0 = cv2.inRange(hsv, lower_hsv, higher_hsv)
        lower_red = np.array([170,50,50])
        upper_red = np.array([180,255,255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        mask =  mask1
        #https://stackoverflow.com/questions/30331944/finding-red-color-in-image-using-python-opencv
        # Apply the mask for red colour note values are found experinemtanlly so can vary from camera to camera and red seems to pick up a lot of cyan 
    elif Bluevalue ==1:
        lower_hsv = np.array([76, 159, 162])
        higher_hsv = np.array([179, 255, 255])
        mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
        # Apply the mask for Blue colour note values are found experinemtanlly so can vary from camera to camera 

    elif Greenvalue ==1:
        lower_hsv = np.array([68, 51, 108])
        higher_hsv = np.array([96, 255, 255])
        mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
        # Apply the mask for Green colour nqote values are found experinemtanlly so can vary from camera to camera 

    else:
        lower_hsv = np.array([0, 0, 0])
        higher_hsv = np.array([179, 255, 255])
        mask = cv2.inRange(hsv, lower_hsv, higher_hsv)
        # Apply no mask for regular video 
        
    foo_canny =cv2.getTrackbarPos('Redmode', 'image')
    
    frame = cv2.bitwise_and(frame, frame, mask=mask)
    median = cv2.medianBlur(frame,5) #cleans image
    edge = cv2.Canny(median,600,700,3) #shows edges.
    cdst = cv2.cvtColor(edge, cv2.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)

    lines = cv2.HoughLines(edge, 1, np.pi / 180, 150, None, 0, 0)
    
    if lines is not None:
        for i in range(0, len(lines)):
            rho = lines[i][0][0]
            theta = lines[i][0][1]
            a = math.cos(theta)
            b = math.sin(theta)
            x0 = a * rho
            y0 = b * rho
            pt1 = (int(x0 + 1000*(-b)), int(y0 + 1000*(a)))
            pt2 = (int(x0 - 1000*(-b)), int(y0 - 1000*(a)))
            cv2.line(cdst, pt1, pt2, (0,0,255), 3, cv2.LINE_AA)

    linesP = cv2.HoughLinesP(edge, 1, np.pi / 180, 50, None, 50, 10)
    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            cv2.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 3, cv2.LINE_AA)

    cv2.imshow('image', edge)
    cv2.imshow("Detected Lines (in red) - Standard Hough Line Transform", cdst)
    cv2.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
    #https://docs.opencv.org/3.4/d9/db0/tutorial_hough_lines.html

    gray_img = cv2.cvtColor(median, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for cnt in cnts:
        approx = cv2.contourArea(cnt)
        #print(approx)
    #https://www.delftstack.com/howto/python/opencv-detect-rectangle/

    cv2.imshow('Binary',thresh_img)

    Redvalue =cv2.getTrackbarPos('Redmode', 'image')
    Bluevalue =cv2.getTrackbarPos('Bluemode', 'image')
    Greenvalue =cv2.getTrackbarPos('Greenmode', 'image')
    #print (f'Blue value = {Bluevalue}, Red value = {Redvalue}, Green value = {Greenvalue}')
    # Press q to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()