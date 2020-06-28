# -*- coding: utf-8 -*-
"""
Created on Sun Nov 10 12:27:24 2019

@author: Administrator
"""
import random

class call():
    
    def __new__(self , lv):        
        speed = 0
        self.lv = lv
        if (lv == 1):
            speed = random.randint(7,10) # 7,10
        elif ( lv == 2 ):
            speed = random.randint(10,13) #10,13
        else :
            speed = random.randint(14,16)
            
        return speed
        