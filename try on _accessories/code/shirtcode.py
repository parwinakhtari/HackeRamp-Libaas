# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 19:38:52 2020

@author: ASUS
"""

 

# -*- coding: utf-8 -*-


import cv2
import numpy as np
import settings
from pose.estimator import TfPoseEstimator
from pose.networks import get_graph_path

img1 = cv2.imread('target1.jpeg')
img1=cv2.resize(img1,(640,480),interpolation=cv2.INTER_CUBIC)
cv2.imshow("product",img1)
#cv.imshow('necklace',img1)
model=cv2.imread("gir.jpg")
model=cv2.resize(model,(640,480),interpolation=cv2.INTER_CUBIC)
cv2.imshow("targetmodel",model)
ix,iy = 0,0
r=300
c=295
poseEstimator = None

poseEstimator = TfPoseEstimator(get_graph_path('mobilenet_thin'), target_size=(432, 368))
def maskf(image):
    
    mask = np.zeros(image.shape[:2],np.uint8)
    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    rect = (1,2,image.shape[1],image.shape[0])
    
    mask, bgModel, fgModel=cv2.grabCut(image,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)
    outputMask = np.where((mask == cv2.GC_BGD) | (mask == cv2.GC_PR_BGD),0, 1)

# scale the mask from the range [0, 1] to [0, 255]
    outputMask = (outputMask * 255).astype("uint8")
    return outputMask
  
def fit_object(img2,x1,y1,x2,y2,x3,y3):
    

    try:
        
        print("s")
        
        dim = (x2-x1,y3-y1)
        img1_rs = cv2.resize(img1,dim,interpolation = cv2.INTER_CUBIC)
        print("s")
        rows,cols = img1_rs.shape[:2]
        roi = (img2[y1-25:y3,x1-50:x2+60])
        print("s")
        cv2.imshow("roi",roi)
        print("s")
        print(roi.shape)
        print("s")
        mask=maskf(img1_rs)
        cv2.imshow("mask1",mask)
        j=roi.shape[0]
        t=roi.shape[1]
        mask_inv = cv2.bitwise_not(mask)
        mask_inv = cv2.resize(mask_inv,(t,j),interpolation = cv2.INTER_CUBIC)
        
        mask=cv2.resize(mask,(img1_rs.shape[1],img1_rs.shape[0]),interpolation = cv2.INTER_CUBIC)            
        cv2.imshow("maskinv",mask_inv)
        img1_bo = cv2.bitwise_and(roi,roi,mask=mask_inv)
        cv2.imshow("bg",img1_bo)
        
        img2_fg = cv2.bitwise_and(img1_rs,img1_rs,mask=mask)
        
        img2_fg=cv2.resize(img2_fg,(t,j),interpolation = cv2.INTER_CUBIC)
        
        final = cv2.add(img1_bo,img2_fg)
        cv2.imshow("final1",final)
        img2[y1-25:y3,x1-50:x2+60] = final
    
        cv2.imshow('final',img2)
        cv2.imwrite("fit.jpg",img2)
        return img2
    except:
        return img2
        
   
    
cap=cv2.VideoCapture(0)
'''
these are the keypoint values stored in the 2D list Values
Nose = 0
Neck = 1
RShoulder = 2
RElbow = 3
RWrist = 4
LShoulder = 5
LElbow = 6
LWrist = 7
RHip = 8
RKnee = 9
RAnkle = 10
LHip = 11
LKnee = 12
LAnkle = 13
REye = 14
LEye = 15
REar = 16
LEar = 17
Background = 18
'''

while True:
    
    ret,frame=cap.read()
    model=cv2.resize(model,(640,480),interpolation=cv2.INTER_CUBIC)
    Values=[]
    img3=[]
    
    if ret :
        print(ret)
        show = cv2.resize(model, (settings.winWidth, settings.winHeight))
        
        humans = poseEstimator.inference(show)
                   
        show,Values = TfPoseEstimator.draw_humans(show, humans, imgcopy=False)
        flag1=0
        flag2=0
        flag3=0
        for val in Values:
            if val[0]==2:
                flag1=1
                x1=val[1]
                y1=val[2]
            if val[0]==5:
                x2=val[1]
                y2=val[2]
                
                flag2=1
                
            if val[0]==8:
                print("Rhip")
                x3=val[1]
                y3=val[2]
                flag3=1
                print(val[1])
                print(val[2])
            if val[0]==11:
                print("Lhip")
                
                print(val[1])
                print(val[2])
    if flag1 and flag2 and flag3:
        print(x1,y1,x2,y2,x3,y3)
        print("True1")
        trans=model.copy()
        img3=fit_object(trans,x1,y1,x2,y2,x3,y3)
#        cv2.imshow("model",img3)
    if flag1 and flag2 and flag3:
         cv2.imshow("frame",img3)
    else:
        cv2.imshow("frame",show)
    cv2.imshow("original",show)
        
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
    