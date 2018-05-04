import cv2
import imutils
import numpy as np

def show_image(image,s):
    cv2.imshow(str(s),image)
    if (cv2.waitKey(0) & 0xFF == ord('q')):
        cv2.destroyAllWindows()

def find_contours(image):
    gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)

    blur=cv2.GaussianBlur(gray,(7,7),0)

    ret,thresh = cv2.threshold(blur,200,255,cv2.THRESH_BINARY_INV)
    contours = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]
    return contours
def side(contours):
    shape='Unidentified'
    perimeter=cv2.arcLength(contours,True)
    num_side=cv2.approxPolyDP(contours,0.02*perimeter,True)
    return num_side
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
def Color(pixel):

    r=pixel[2]
    g=pixel[1]
    b=pixel[0]
    
    if (b>240 and g<50 and r<50):
        col='Blue'
    elif(b<50 and g>240 and r<50):
        col='Green'
    elif(b<50 and g<50 and r>240):
        col='Red'
    else:
        col='Orange'

    return col


img=cv2.imread('test2.png')
img1=np.copy(img)
cnts=find_contours(img)
for c in cnts:
    num_side=side(c)
    shape=shape_of(num_side)
    M = cv2.moments(c)
    
    cY = int(M["m10"] / M["m00"])
    cX = int(M["m01"] / M["m00"])

    pixel=img[cX][cY]
    col=Color(pixel)
    print (pixel)
    cv2.drawContours(img1,[c], -1, (0, 0, 0), 5)
    cv2.circle(img1, (cY, cX), 4, (255, 255, 255), -1)
    cv2.putText(img1,col+shape, (cY - 45, cX - 25),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)     
    cv2.putText(img1, "("+str(cY)+","+str(cX)+")", (cY-40, cX-10),
        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 0), 1)     
	
    cv2.imshow("Image", img1)
    cv2.waitKey(0)
