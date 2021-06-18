# -*- coding: utf-8 -*-
"""
Created on Tue May 11 00:27:06 2021

@author: sayan
"""
import cv2
import numpy as np
import dlib
import imutils
from imutils import face_utils
from imutils.video import VideoStream
from imutils.video import FPS
import time

#stacking the pictures of two sunglasses horizontally
def hconcat_resize(img_list, interpolation 
                   = cv2.INTER_CUBIC):
    h_min = 100
      
    # image resizing 
    im_list_resize = [cv2.resize(img,
                       (int(img.shape[1] * h_min / img.shape[0]),
                        h_min), interpolation
                                 = interpolation) 
                      for img in img_list]
    # return final image
    return cv2.hconcat(im_list_resize)

img1=cv2.imread("C:\\Users\\sayan\\Downloads\\IMG_20210312_013532.jpg",-1)
img2=cv2.imread("C:\\Users\\sayan\\Downloads\\dwCsXFzMweqW1JEcXMq9hIj46B1WLVB7CaGpvbHw.jpeg",-1)

img_v_resize = hconcat_resize([img1, img2])
list_of_sunglasses=[]

list_of_sunglasses.append(img1)
list_of_sunglasses.append(img2)

#this will prepare the sunglass image so that it can be placed correctly on the eyes
def preprocess_sunglass(choice,width,height,expected_distance_between_ends):
    
    # the sunglass image chosen by the user
    sunglass_image=list_of_sunglasses[choice-1]
    #taking the blue channel of the image---I found this channel good for thresholding the images
    alpha_image=sunglass_image[:,:,0]
    ret,threshold=cv2.threshold(alpha_image,170,255,cv2.THRESH_BINARY_INV)
    inverted_mask=cv2.bitwise_not(threshold)
    contours,hierarchy=cv2.findContours(inverted_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            
    if contours is not None:
        
        contours=sorted(contours,key=cv2.contourArea,reverse=True)
        test_mask=np.zeros((sunglass_image.shape[0],sunglass_image.shape[1]),dtype="uint8")
        
        imp_contours=[]
        for seq,i in enumerate(contours):
            if seq!=0:
                imp_contours.append(i)
                
        cv2.drawContours(test_mask,imp_contours,-1,255,1)
        
        cv2.fillPoly(test_mask,[imp_contours[0].astype('int32')],255)
        cv2.fillPoly(test_mask,[imp_contours[3].astype('int32')],0)
        try:
            test_mask=imutils.resize(test_mask,width=max(width,1),height=max(height,1))
            resized_sunglasses=imutils.resize(sunglass_image,width=width,height=height)
        except:
            return (None,None,None,None)
        anded=cv2.bitwise_and(resized_sunglasses,resized_sunglasses,mask=test_mask)
        thresh=test_mask
        x, y, w, h = cv2.boundingRect(thresh)
       
        mask_for_stretching=test_mask[y:y+h,x:x+w]
        bbox_sunglass=anded[y:y+h,x:x+w]
        mask_for_stretching=imutils.resize(mask_for_stretching,width=expected_distance_between_ends,inter=cv2.INTER_CUBIC)
        bbox_sunglass=imutils.resize(bbox_sunglass,width=expected_distance_between_ends,inter=cv2.INTER_CUBIC)
        test_mask[:,:]=0
        anded[:,:,:]=(0,0,0)
        
        try:
            test_mask[0:mask_for_stretching.shape[0],0:0+mask_for_stretching.shape[1]]=mask_for_stretching
            anded[0:0+mask_for_stretching.shape[0],0:mask_for_stretching.shape[1],:]=bbox_sunglass
        except:
            return (None,None,None,None)
        x, y, w, h = cv2.boundingRect(test_mask)
        left = (x, np.argmax(test_mask[:, x]))  
        
        small_cnts,hierarchy=cv2.findContours(test_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        if small_cnts is not None:
        
            small_cnts=sorted(small_cnts,key=cv2.contourArea,reverse=True)[0:]
            M=cv2.moments(small_cnts[0])
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            
            diff_with_center_x=width/2-1-cx
            test_mask_copy=test_mask
            test_mask_copy[:,:]=0
            M=np.float32([[1,0,diff_with_center_x],[0,1,0]])
            shifted=cv2.warpAffine(anded, M,(test_mask.shape[1],test_mask.shape[0]))
            y,x,z=np.nonzero(shifted)
            #print("nonzero coords",y_values.shape,x_values.shape)
            test_mask_pixels=[[(j,i)] for i,j in zip(y,x)]
            mask_pixels=np.array(test_mask_pixels)
            return (test_mask,shifted,mask_pixels,left)
        else:
            return (None,None,None,None)
            
        

detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("D:\\Downloads\\shape_predictor_68_face_landmarks.dat")

#this defines the region where the glass will be placed and places the glass
def mark_ROI(image,choice):
    
    image=imutils.resize(image,width=500)
    if choice is not None:
        gray=cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        rects=detector(gray,0)
        vertical_line_reference_coords=0
        horizontal_line_reference_coords=0
        x_left=0
        x_right=0
        y_bottom=0
        y_top=0
        left_reference_extrema=0
        expected_left_end_glasses=0
        expected_right_end_glasses=0
        if rects is not None:
            for (i, rect) in enumerate(rects):
            
                shape = predictor(gray, rect)
                shape = face_utils.shape_to_np(shape)
                
                (x, y, w, h) = face_utils.rect_to_bb(rect)
                
                
                vertical_line_reference_coords=shape[30]
                horizontal_line_reference_coords=shape[27]
                distance_right_eye_nose_middle=abs(shape[17][0]-shape[28][0])
                
                x_left=shape[28][0]-distance_right_eye_nose_middle-10
                x_right=shape[28][0]+distance_right_eye_nose_middle+10
                y_top=min((shape[19][1],shape[24][1]))
                y_bottom=shape[30][1]
                
               
                
                expected_left_end_glasses=shape[36][0]-15
                expected_right_end_glasses=shape[45][0]+15
                
                left_reference_extrema=(shape[17][0]-x_left,shape[17][1]+10-y_top)
          
            sunglass_frame_width=x_right-x_left
            sunglass_frame_height=y_bottom-y_top
            mask,overlay_glasses,mask_pixels,left_extrema=preprocess_sunglass(choice,sunglass_frame_width,sunglass_frame_height,expected_right_end_glasses-expected_left_end_glasses)
            if mask is not None:
                shift_y=left_reference_extrema[1]-left_extrema[1]
                
                for i in mask_pixels:
                    val1=image[y_top+i[0][1]+shift_y,x_left+i[0][0]]
                    val2=overlay_glasses[i[0][1],i[0][0]]
                    image[y_top+i[0][1]+shift_y,x_left+i[0][0]]=val1
                    
            
    cv2.imshow("shifted_mask",image)
    
    

cv2.imshow("available sunglasses",img_v_resize)
vs=cv2.VideoCapture(0,cv2.CAP_DSHOW)

ch=None
while True:
    ret,frame=vs.read()
    
    if frame is None:
        continue
    else:
        
        frame=cv2.flip(frame,1)
        
       
        #frame[:100,599-339:599]=img_v_resize
       
        key = cv2.waitKey(1) & 0xFF
        mark_ROI(frame,ch)
        
        if key == ord('r'):
            print("Pressed 1")
            ch=1
            
        elif key ==ord('q'):
            break
        elif key ==ord('2'):
            print("Pressed 2")
            ch=2
        else:
            pass
        

cv2.destroyAllWindows()

vs.release()


    


    
    


