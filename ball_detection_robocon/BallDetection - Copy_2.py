import urllib
from collections import deque
import numpy as np
import imutils
import argparse
import cv2
import time
count_frames = 1

def nothing(x):
    pass

    ##cv2.namedWindow('image', cv2.WINDOW_AUTOSIZE)
##cv2.namedWindow('image',0)
##
##cv2.createTrackbar('h1','image',0,255,nothing)
##cv2.createTrackbar('v1','image',0,255,nothing)
##cv2.createTrackbar('s1','image',0,255,nothing)
##cv2.createTrackbar('h2','image',255,255,nothing)
##cv2.createTrackbar('v2','image',255,255,nothing)
##cv2.createTrackbar('s2','image',255,255,nothing)


cap=cv2.VideoCapture(0)
focalLength=1076
knownWidth=2.09

while True:
    ret, frame = cap.read()
    #imgResp=urllib.urlopen(url)
    #imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    #frame=cv2.imdecode(imgNp,-1)
    #ret,blurred=cv2.threshold(frame,0,255,cv2.THRESH_BINARY)
    #cv2.imshow('blurred',blurred)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    '''
##    hsv = blurred
##    H1 = cv2.getTrackbarPos('h1','image')
##    V1 = cv2.getTrackbarPos('v1','image')
##    S1 = cv2.getTrackbarPos('s1','image')
##    H2 = cv2.getTrackbarPos('h2','image')
##    V2 = cv2.getTrackbarPos('v2','image')
##    S2 = cv2.getTrackbarPos('s2','image')
##    lower = np.array([H1,V1,S1])
##    upper = np.array([H2,V2,S2])
    ######AVERAGE COLOR [  36.14864865   48.86811495  167.30875813]  ###### CLOSE UP
    ######AVERAGE COLOR [  55.99764982   71.6484528   161.54778692]  ###### FAR
    lower = (100,120,0)
    upper = (160,250,180)
    pts = deque(maxlen=args["buffer"])
    counter = 0
    (dX, dY) = (0, 0)
    direction = ""
    mask = cv2.inRange(hsv, lower, upper)
    
##    cv2.imshow('MASK',mask)
    kernel = np.ones((3,4),np.uint8)
    mask_1 = cv2.erode(mask, kernel, iterations=2)
    mask_2 = cv2.dilate(mask_1, kernel, iterations=2)
    img = cv2.bitwise_and(frame,frame, mask = mask)
    cv2.imshow('IMG',img)

'''
# find contours in the mask and initialize the current
    # (x, y) center of the ball
    cnts = cv2.findContours(blurred, cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)[2]
    print len(cnts)
##    cv2.drawContours(img, cnts, -1, (0,255,0), 3)
    
    center = None
    
    # only proceed if at least one contour was found
    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

        print(radius)
        distance = ((knownWidth * focalLength) / (radius))
        dist_cm = (distance*2.5)
##        print (dist_cm )
        Mf = ((dist_cm)/3.185)
        print (dist_cm + Mf)
        

        # only proceed if the radius meets a minimum size
        if radius > (5):
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
            cv2.circle(frame, (int(x), int(y)), int(radius),
                    (0, 255, 255), 2)
            cv2.circle(frame, center, 3, (0, 0, 255), -1)

            # update the points queue
            pts.appendleft(center)
            ##print center
#############################TRY##################################
##            dX = pts[-10][0] - pts[i][0]dY = pts[-10][1] - pts[i][1]
##            thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
##            cv2.line(frame, pts[x - 1], pts[x], (0, 0, 255), 1)
       	# loop over the set of tracked points
##	for i in np.arange(1, len(pts)):
##		# if either of the tracked points are None, ignore
##		# them
##		if pts[i - 1] is None or pts[i] is None:
##			continue
##		    cv2.line(frame,pts[x - 1], pts[x],(255,0,0),5)
    
    for i in np.arange(1, len(pts)):
        if pts[i - 1] is None or pts[i] is None:
            continue

    if counter >= 10 and i == 1 and pts[-10] is not None:
# compute the difference between the x and y
# coordinates and re-initialize the direction
# text variables
        dX = pts[-10][0] - pts[i][0]
        dY = pts[-10][1] - pts[i][1]
        thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
        cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)          
###########################TRY#################################			

    # show the frame to our screen
    cv2.imshow("Blur",mask)
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    
    
    

# cleanup the camera and close any open windows

cv2.destroyAllWindows()



