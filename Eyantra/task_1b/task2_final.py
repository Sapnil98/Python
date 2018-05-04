import cv2
import imutils
import numpy as np
from math import exp

def find_contours(image):
    gray=image.copy()
    blur=cv2.GaussianBlur(gray,(7,7),0)

    ret,thresh = cv2.threshold(blur,200,255,cv2.THRESH_BINARY)
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]
    return contours
def side(contours):
    perimeter=cv2.arcLength(contours,True)
    num_side=cv2.approxPolyDP(contours,0.02*perimeter,True)
    return num_side
def area_of(contours):
    Area=cv2.contourArea(contours)
    return Area

def size_of(Area):
    area=Area
    if area>=(5000.00):
        size='large'
    elif area<=(3500.00):
        size='small'
    else:
        size='medium'
    return size

def shape_of(num_side):
    num_of_side=len(num_side)
    if num_of_side==3:
        shape='Triangle'
    elif num_of_side==4:
        z=cv2.boundingRect(num_side)
        ar=z[2]/z[3]
        shape='Square' if ar>=0.95 and ar<=1.05 else 'Rectangle'
    elif num_of_side==5:
        shape='Pentagon'
    elif num_of_side==6:
        shape='Hexagon'
    else:
        shape='Circle'
    return shape

def show(cnts,img1,colour,m):
    for c in cnts:
        x=np.ceil(np.random.randn(3)*200)
        y=0
        num_side=side(c)
        area=area_of(c)
        size=size_of(area)
        shape=shape_of(num_side)
        M = cv2.moments(c)

        cY = int(M["m10"] / M["m00"])
        cX = int(M["m01"] / M["m00"])
        col=colour
        cv2.drawContours(img2,[c], -1, x, 5)
        cv2.circle(img2, (cY, cX), 4, (255, 255, 255), -1)
        cv2.putText(img2,col+size+shape, (cY - (m*10)+10, cX - (m*10)-10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5,y, 1)     
        cv2.putText(img2, "("+str(cY)+","+str(cX)+")", (cY-(m*10)+5, cX-(m*10)+10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5,y, 1)     
	
        cv2.imshow("Image", img2)
        cv2.waitKey(10000)
    

img=cv2.imread('test1.png')
img2=np.copy(img)
count=0
col_dic={'Red':([0,0,230],[0,0,255]),
         'Green':([0,230,0],[0,255,0]),
         'Blue':([230,0,0],[255,0,0]),
         'Yellow':([0,230,230],[0,255,255]),
         'Orange':([0,130,0],[0,150,255])}
col=['Red','Green','Blue','Yellow','Orange']
for m in range(5):
    colour=col[m]
    print (colour)
    (l,u)=col_dic[colour]
    img1=np.copy(img)
    img1=cv2.inRange(img1,np.array(l),np.array(u))
    cnts=np.array(find_contours(img1))
    lst=show(cnts,img2,colour,int((1/(1+exp(-m)))))
    
print ('COmplete')
cv2.destroyAllWindows()
