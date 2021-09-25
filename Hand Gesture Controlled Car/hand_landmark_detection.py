# -*- coding: utf-8 -*-
"""
Created on Sun Apr 25 22:29:50 2021

@author: sayan
"""

import mediapipe as mp
import cv2
import socket
server_ip='192.168.163.238'
server_port=80
soc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
soc.connect((server_ip,server_port))
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
cap=cv2.VideoCapture(0)
with mp_hands.Hands(
    min_detection_confidence=0.7,
    min_tracking_confidence=0.5) as hands:
    count=-1
    while cap.isOpened():
       success,image=cap.read()
       if not success:
           print("Ignoring empty camera frame")
           continue
       #image=cv2.cvtColor(cv2.flip(image,1),cv2.COLOR_BGR2RGB)
       image=cv2.flip(image,1)
       cv2.rectangle(image,(370,150),(570,350),(0,255,0),3)
       
       frame=image[150:351,370:571]
       frame=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
       results=hands.process(frame)
       
       frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
       if results.multi_hand_landmarks:
           #print(results.multi_handedness[0].classification[0].label)
           for hand_landmarks in results.multi_hand_landmarks:
               
               #print(type(hand_landmarks))
               mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
               #thumb
           try:
               count=count+1
               fingers_open=0
               #special case of thumb
               point1=results.multi_hand_landmarks[0].landmark[1].x
               point2=results.multi_hand_landmarks[0].landmark[4].x
               
               if(point2<point1):
                   fingers_open+=1
               #rest of the fingers
               finger_bottom=(7,11,15,19)
               finger_top=(8,12,16,20)
               
               for i,j in zip(finger_bottom,finger_top):
                   point1=results.multi_hand_landmarks[0].landmark[i].y
                   point2=results.multi_hand_landmarks[0].landmark[j].y
                   if point2<point1:
                       fingers_open+=1
               text=str(fingers_open)+"\n"
               if count%10==0:
                   soc.sendall(text.encode('utf-8'))
                   ret=soc.recv(1024).decode()
               #print(ret)
               #print(soc.recv(1024).decode())
               
               cv2.putText(image,f'Count={fingers_open}',(70,70),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0))
           except:
               pass
       #image[350:551,100:301]=frame
       cv2.imshow('MediaPipe Hands', image)
       cv2.imshow('block',frame)
       if cv2.waitKey(5) & 0xFF == 27:
           soc.close()
           break
cap.release()
cv2.destroyAllWindows()
        
    
    