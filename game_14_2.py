# -*- coding: utf-8 -*-
"""
Created on Sat Mar  9 23:54:12 2019

@author: Administrator
"""

import cv2
import numpy as np

class move():
    
    def __new__(self):        
        cap = cv2.cv2.VideoCapture(0)
        es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(9,4))
        #kernel = np.ones((5,5),np.uint8)
        #background = None
        #bg_knn_2 = None
        bg_k = cv2.createBackgroundSubtractorKNN(detectShadows = True)
        bg_k = cv2.createBackgroundSubtractorMOG2()
        cap.set(cv2.CAP_PROP_FPS, 120)
        object_move = False
        first = True
        cX = 0
        cY = 0
        while cap.isOpened():
            ret,frame = cap.read()
    
            bg_knn = bg_k.apply(frame)
            bg_knn = cv2.GaussianBlur(bg_knn,(23,23),0)
            bg_knn = cv2.threshold(bg_knn,25,255,cv2.THRESH_BINARY)[1]
            bg_knn = cv2.dilate(bg_knn,es,iterations=2)
            bg_knn = cv2.flip(bg_knn,1)
            frame = cv2.flip(frame,1)
            cnts,_ = cv2.findContours(bg_knn.copy(),
                        cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
    
            for c in cnts:
                if cv2.contourArea(c)<25000:
                    object_move = False
                    continue
                (x,y,w,h) = cv2.boundingRect(c)
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                M = cv2.moments(c)
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                object_move = True
                if (first == True):
                    object_move = False
                    first = False
    
            cv2.putText(frame, "center", (cX - 20, cY - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.imshow("contours",frame)
            #cv2.imshow("dif",bg_knn)
            '''
            print("Center=", cX, cY)
            '''
            k = cv2.waitKey(50)
            if k ==ord('0'):
                break
            if (cY < 270 and object_move == True):
                break
        print('cv close')    
        cv2.destroyAllWindows()
        cap.release()
        


        

    