import cv2
import argparse
import numpy as np
from collections import deque
def nothing(x):
    pass
cv2.namedWindow('image',0)

Col={'Blue':[83,67,35,123,250,180],'Red':[157,102,73,187,186,180],
     'Gold':[0,33,112,60,92,225]}
## one needs to find the indivial hsv values range for the different colour balls and put them here
## the order is h0,s0,v0, h1,s1,v1
cam=cv2.VideoCapture(1)

while 1:
    ret,fram=cam.read()
    if ret== True :
        fram1=fram.copy()
        
        cropped=fram[220:400,160:320]
        cv2.rectangle(fram,(220,160),(400,320),(0,0,0),3)
        blurred=cv2.medianBlur(cropped,19)
        for i in Col.keys():
            col_lst=Col[i]
            hsv=cv2.cvtColor(blurred,cv2.COLOR_BGR2HSV)
            lower=np.array(col_lst[0:3])
            upper=np.array(col_lst[3:6])
            mask=cv2.inRange(hsv,lower,upper)
            img = cv2.bitwise_and(cropped,cropped, mask =mask)
            cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE)[1]
            if len(cnts) > 0:
                # find the largest contour in the mask, then use
                # it to compute the minimum enclosing circle and
                # centroid
                c = max(cnts, key=cv2.contourArea)
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                M = cv2.moments(c)
                if (M["m00"] != 0):
                    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                    if (radius >5 and radius < 100 and cv2.contourArea(c) > 500):
                        # draw the circle and centroid on the frame,
                        # then update the list of tracked points
                        cv2.circle(fram, (int(x)+220, int(y)+160), int(radius),
                                (0, 255, 255), 2)
                        cv2.circle(fram, center, 3, (0, 0, 255), -1)
                        ext=1
                        print (i)

        cv2.imshow('s',fram)
    k=cv2.waitKey(1) & 0xFF
    if k==ord('q'):
        break
cv2.destroyAllWindows()
