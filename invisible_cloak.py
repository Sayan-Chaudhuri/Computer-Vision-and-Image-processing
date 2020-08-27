# -*- coding: utf-8 -*-
"""
Created on Sat Jul  4 23:06:06 2020

@author: LENOVO
"""


import cv2
import numpy as np

redlower=(140,150,0)
redupper=(180,255,255)
cap=cv2.VideoCapture(cv2.CAP_DSHOW)
img=cv2.imread("C://Users//LENOVO//Pictures//Camera Roll//test_image1(2).jpg")
img=cv2.flip(img,1)
while True:
    ret,frame=cap.read()
    frame=cv2.flip(frame,1)
    
    blurred=cv2.GaussianBlur(frame,(5,5),0)
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    resized_image=cv2.resize(img,(frame.shape[1],frame.shape[0]))
    cv2.imshow('still_pic',resized_image)
    mask=cv2.inRange(hsv,redlower,redupper)
    kernel=np.ones((7,7),np.uint8)
    fine_tuned=cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    
    cv2.imshow('maksed',fine_tuned)
    image,contours,hierarchy=cv2.findContours(fine_tuned,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    if contours is not None:
        cnt=sorted(contours,key=cv2.contourArea,reverse=True)[0:]
        white_points=cv2.findNonZero(fine_tuned)
        if white_points is not None:
            white_points=white_points.reshape(white_points.shape[0],2)
            s1=white_points.sum(axis=1)
            
            top_left=white_points[np.argmin(s1)]
            bottom_right=white_points[np.argmax(s1)]
            d1=np.diff(white_points,axis=1)
            top_right=white_points[np.argmin(d1)]
            bottom_left=white_points[np.argmax(d1)]
            frame[top_left[1]:bottom_right[1]+1,top_left[0]:bottom_right[0]+1]=\
                img[top_left[1]:bottom_right[1]+1,top_left[0]:bottom_right[0]+1]
        
    cv2.imshow('Frame',frame)
    
    if cv2.waitKey(1) & 0xFF==ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
