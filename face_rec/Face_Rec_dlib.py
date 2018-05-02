from imutils import face_utils
import dlib
import cv2
import timeit
import numpy as np


faces_folder_path = "images\\"
cam=cv2.VideoCapture(1)

detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor("shape_predictor_5_face_landmarks.dat")
facerec = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

win = dlib.image_window()
def comp(face):
    image=cv2.imread(faces_folder_path+"test_image.jpg")
    detect=detector(image,1)
    shap=sp(image,d)
    s=0
    face_desp=facerec.compute_face_descriptor(image, shap)
    for i in range(128):
        s=s+face_desp[i]-face[i]
    s=abs(s)/128
    print("confidence = {}".format(100-s))
while 1:
    start_time=timeit.default_timer()
    _,img=cam.read()
    img=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)

    win.clear_overlay()
    win.set_image(img)

    dets = detector(img, 1)
    print("Number of faces detected: {}".format(len(dets)))

    for k, d in enumerate(dets):
        #print("Detection {}: Left: {} Top: {} Right: {} Bottom: {}".format(
        #    k, d.left(), d.top(), d.right(), d.bottom()))
        shape = sp(img, d)
        win.clear_overlay()
        win.add_overlay(d)
        win.add_overlay(shape)
        
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        comp(face_descriptor)
        elapsed = timeit.default_timer() - start_time
        print ("FPS= {}".format(1/elapsed))

        #dlib.hit_enter_to_continue()
