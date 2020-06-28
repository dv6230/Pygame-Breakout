# -*- coding: utf-8 -*-
"""
Created on Sun Sep 22 13:14:00 2019

@author: Administrator
"""

import pygame as pg
import random
import cv2
import numpy as np
import game_14_2 as opencv
import game_14_3 as speed
import time
import os 



pg.init()


#設定視窗背景
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (2,32)
width, height = 1531,792                     #設定視窗大小    
screen = pg.display.set_mode((width, height))   #視窗大小設定與建立
pg.display.set_caption("Sean's game")   #標題   
     
bg = pg.Surface(screen.get_size())  #建立背景繪圖區   
bg.fill((255,255,255,0))    # 填滿顏色

ball_image = pg.image.load('opt.png').convert_alpha()
ball = pg.Surface((40,40))     #建立球矩形繪圖區
ball.fill((0,0,0,255))             #矩形區塊背景為白色
pg.draw.circle(ball, (0,0,255), (10,10),10, 0)  #畫藍色球 (繪圖區位置,顏色,座標,直徑,邊框大小)
ball_rect = ball.get_rect()         #取得繪圖的區塊
ball_rect.center = (750,350)        #設定球起初始位置
ball_long = 15 

image = pg.image.load("pad2.png").convert_alpha()
pad = pg.Surface((225,30))     #建立繪圖
pad.fill((255,255,255))       #繪圖塊背景為白色
pg.draw.rect(pad, (255,0,0), (0,0,100,20))  #畫紅色板子
pad_rect = pad.get_rect()         #取得繪圖的區塊
pad_rect.center = (500,700)        #設定板子的初始位置
pad_long = 225


earth = pg.image.load('earth_in_space.jpg').convert_alpha()
earth.convert_alpha()


score = 0
life = 10
life_line = 770 #生命線，低於此數值會扣生命
level = 1
blk = []

brick_img = pg.image.load('blocks_2.png').convert_alpha()
blk_width = 75 #磚塊寬度
blk_high = 38  #磚塊高度
blk_1 = 3 #幾列
blk_2 = 9 #幾行

for j in range (0,blk_1):   #用迴圈儲存磚塊的定位
    for i in range (0,blk_2):    
        blk.append(((i*150)+100,100+(j*75)))  #磚塊長寬

    
        
def blk_add():
    if (level == 2):
        for j in range(0,blk_1):
            for i in range (0,blk_2):
                blk.append(((i*150)+100,100+(j*75)))
    else:
        for j in range(0,5):  #列
            for i in range (0,8):   #行
                blk.append(((i*100)+400,100+(j*50)))

font1 = pg.font.SysFont('Comic Sans MS', 20)  #預設字體
font2 = pg.font.Font("C:\WINDOWS\Fonts\msjh.ttc",128)  #開啟畫面字體
font3 = pg.font.Font("C:\WINDOWS\Fonts\msjh.ttc", 32 )
font4 = pg.font.Font("C:\WINDOWS\Fonts\msjh.ttc", 48 )
font5 = pg.font.Font("C:\WINDOWS\Fonts\msjh.ttc", 64 )

font6 = pg.font.SysFont('Comic Sans MS', 34)  #預設字體

px , py = pad_rect.center       #板子的左上角x , y 

ball_x, ball_y = ball_rect.center           #球的左上角x , y 
xmove = 0                     #初始球移動速度
ymove = 4
clock = pg.time.Clock()        #建立時間元件
ishit = 0


def DrawText(text, font, surface, x, y): 
    text_obj = font.render(text, 1, (255,255,255))
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)   # surface.blit 繪製覆蓋視窗介面 (背景變數,繪製位置)
    
game_state = 'Gaming'

def Choice_Exit():  #退出遊戲
    pg.quit()


# 按下任意按鍵開始
def user_key():
    while True:
        for ev in pg.event.get():
            if ev.type == pg.QUIT:   #按下視窗的 離開按鈕則退出遊戲
                Choice_Exit()
            if ev.type == pg.KEYDOWN:
                
                return


bg2 = pg.Surface(screen.get_size())  #建立背景繪圖區 
bg2.fill((0,0,0))
screen.blit(bg2, (0,0))
            
def draw_time_text(x):
    if (x < 1):
        bg2.fill((0,0,0))
        bg2.blit(earth,(0,0))
        DrawText('開始', font2 , bg2 ,(width/2 - 120 ), (height/2 - 100 ))
        screen.blit(bg2, (0,0))
        pg.display.update()     #更新視窗        
    else:
        bg2.fill((0,0,0))
        bg2.blit(earth,(0,0))
        DrawText(str(x), font2 , bg2 ,(width/2 - 60 ), (height/2 - 150 ))
        DrawText('遊戲準備開始 請距離電腦一大步', font3 , bg2 ,(width/2 - 240), (height/2 + 50 ))
        screen.blit(bg2, (0,0))
        pg.display.update()     #更新視窗
       
            
def wait_fundtion():
    clock_wait = pg.time.Clock()
    timer = 20
    while True:
        for event in pg.event.get():
        # This allows the user to quit by pressing the X button.
            if event.type == pg.QUIT:
                break
        if (timer < 1):
            break
        else :
            timer -= 1
            draw_time_text(timer)
        clock_wait.tick(1)   
    

soundyeil = pg.mixer.Sound("yisell.wav")   
soundwav = pg.mixer.Sound("彈板子.wav") 
sound_dead = pg.mixer.Sound("死亡.wav")
sound_drop = pg.mixer.Sound("掉地上.wav")
sound_level_up = pg.mixer.Sound("過關用.wav")


black_hole = pg.image.load('blackhole2.png').convert_alpha()
black_bg = pg.Surface((20,20))     #建立球矩形繪圖區
black_bg.fill((0,0,0,255))  
black_bg_loc = black_bg.get_rect()  
black_hole_rect = black_hole.get_rect()  
random_x = random.randint(50,550)  # 黑洞 x 
random_y = random.randint(50,250)  # 黑洞 y 
black_hole_diameter = 60   #黑洞直徑
black_hole_diameter_helf = 30 #黑洞半徑
deliver = False # 是否傳送(傳送後，球撞到板子才能進行傳送)

black_hole_tup = [(40,40),(1400,40),(40,250),(1400,250)]
#black_hole_tup.clear()

def random_black_hole():
    if (level != 2):
        black_hole_tup.clear()
        for mk in range(6):
            while True:
                random_point_x = random.randint(40,1400)
                random_point_y = random.randint(40,300)
                if( (random_point_x > 1200 or random_point_x < 400 )):
                    black_hole_tup.append((random_point_x,random_point_y))
                    break
                
                    
                    
            
        
#random_black_hole() 
                    
    
   
wait_fundtion()

bg1 = pg.Surface(screen.get_size())  #建立背景繪圖區   
bg1.fill((0,0,0))    # 填滿顏色
bg1.blit(earth,(0,0))
DrawText('舉起雙手後開始', font4 , bg1 , 
         (width/2 - 180), (height/2 + 30 ))
DrawText('指導教授 蔡賢亮', font3 , bg1 , 
         (width/2 - 300), (height/2 - 50 ))
DrawText('義守大學資管系 組員: 洪奕生 李念庭 徐伯嘉', font3 , bg1 , 
         (width/2 - 300), (height/2 - 100))
screen.blit(bg1, (0,0))
pg.display.update()     #更新視窗


'''
user_key()
'''

#關閉程式的程式碼
running = True   #設定執行 == true 為 false 則跳出迴圈關閉
#開始的偵測
start_catch = False
gt_value_x = opencv.move()



kick_off = False
black_hole_num = -1

video = cv2.VideoCapture(0)
_, first_frame = video.read()
opencv_x = 280 
opencv_y = 250
opencv_width = 120
opencv_height = 240
roi = first_frame[opencv_y: opencv_y + opencv_height, opencv_x: opencv_x + opencv_width]
hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
roi_hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])
roi_hist = cv2.normalize(roi_hist, roi_hist, 0, 255, cv2.NORM_MINMAX)
term_criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)

move_rate = (width-pad_long)/(640-opencv_width)
time_tick = 0

while running:
            
    bg.fill((0,0,0,0)) 
    bg.blit(earth,(0,0))
    
    #-----------------------------------------------   
    
    _, frame = video.read()
    frame = cv2.flip(frame,1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.calcBackProject([hsv], [0], roi_hist, [0, 180], 1)
    _, track_window = cv2.meanShift(mask, (opencv_x, opencv_y, opencv_width, opencv_height), term_criteria)
    opencv_x, opencv_y, opencv_w, opencv_h = track_window
    cv2.rectangle(frame, (opencv_x, opencv_y), (opencv_x + opencv_w, opencv_y + opencv_h), (0, 255, 0), 2)
    #print((opencv_x +opencv_w)/2)  
    cX = opencv_x + (opencv_w/2)
    cY = opencv_y + (opencv_h/2)
    cv2.putText(frame, "X", (int(cX),int(cY)),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)
    cv2.imshow("Frame", frame)
    
    
    if (cY < 250):
        kick_off = False

    #-----------------------------------------------
    
    mus = pg.mouse.get_pos()   #抓取滑鼠坐標
    px = (cX-(opencv_width/2)) * move_rate + (pad_long/2) #mus[0]  #(cX-(opencv_width/2)) * move_rate + (pad_long/2) #mus[0] 
    
    '''
    if (px > width - 50 ):    #滑鼠的x>視窗-板子長，則板子的x設定為視窗-板子長，板子不會繼續往左走 
        px = width - 50 
    if (px < 70*2.5 ):    #滑鼠的x<0，板子不會繼續往左走
        px = 50
    '''
    clock.tick(120)        #每秒執行120次
    
    for event in pg.event.get():       #視窗關閉
        if event.type == pg.QUIT:
            running = False            
            
    if (game_state == 'Gaming'):
        ball_y += ymove                 #改變位置y
        ball_x += xmove                 #改變位置x    
    
        ball_rect.center = (ball_x,ball_y)        #更新座標
        
        ball_cx = ball_rect.center[0]
        ball_cy = ball_rect.center[1]
        pad_rect.center = (px,py)

  
        for n in range(len(blk)): 
                if( blk[n][0]+blk_width >= ball_cx
                   and ball_cx >= blk[n][0] and blk[n][1] + blk_high >= ball_cy  
                   and ball_cy >= blk[n][1] ): 
                    black_hole_num = -1 #黑洞入口重置        
                    ymove = ymove*-1
                    blk.remove((blk[n][0],blk[n][1])) 
                    score = score + 100
                    soundyeil.play()
                    if (xmove <= 0):
                        xmove = speed.call(level) * -1 #random.randint(5,8) * -1
                    elif (xmove >= 0) :
                        xmove = speed.call(level) 
                    break
                
                elif(blk[n][0]+blk_width >= ball_cx + ball_long
                     and ball_cx + ball_long >= blk[n][0] and blk[n][1] + blk_high >= ball_cy + ball_long
                     and ball_cy + ball_long >= blk[n][1]):
                        black_hole_num = -1 #黑洞入口重置        
                        ymove = ymove*-1
                        blk.remove((blk[n][0],blk[n][1])) 
                        score = score + 100
                        soundyeil.play()
                        if (xmove <= 0):
                            xmove = speed.call(level) * -1
                        elif (xmove >= 0) :
                            xmove = speed.call(level)
                        break
                elif(blk[n][0]+blk_width >= ball_cx + ball_long
                    and ball_cx + ball_long >= blk[n][0] and blk[n][1] + blk_high >= ball_cy - ball_long
                    and ball_cy - ball_long >= blk[n][1]):
                       black_hole_num = -1 #黑洞入口重置        
                       ymove = ymove*-1
                       blk.remove((blk[n][0],blk[n][1])) 
                       score = score + 100
                       soundyeil.play()
                       if (xmove <= 0):
                            xmove = speed.call(level) * -1
                       elif (xmove >= 0) :
                            xmove = speed.call(level)
                       break
                elif(blk[n][0]+blk_width >= ball_cx - ball_long
                    and ball_cx - ball_long >= blk[n][0] and blk[n][1] + blk_high >= ball_cy - ball_long
                    and ball_cy - ball_long >= blk[n][1]):
                       black_hole_num = -1 #黑洞入口重置        
                       ymove = ymove*-1
                       blk.remove((blk[n][0],blk[n][1])) 
                       score = score + 100
                       soundyeil.play()
                       if (xmove <= 0):
                            xmove = speed.call(level) * -1
                       elif (xmove >= 0) :
                            xmove = speed.call(level)
                       break
                elif(blk[n][0]+blk_width >= ball_cx - ball_long
                    and ball_cx - ball_long >= blk[n][0] and blk[n][1] + blk_high >= ball_cy + ball_long
                    and ball_cy + ball_long >= blk[n][1]):
                       black_hole_num = -1 #黑洞入口重置        
                       ymove = ymove*-1
                       blk.remove((blk[n][0],blk[n][1])) 
                       score = score + 100
                       soundyeil.play()
                       if (xmove <= 0):
                            xmove = speed.call(level) * -1
                       elif (xmove >= 0) :
                            xmove = speed.call(level)
                       break
            
        if(ball_rect.left <= 0): 
            black_hole_num = -1 #黑洞入口重置        
            xmove = speed.call(level)        #球向右 
        if(ball_rect.right >= width ):   
            black_hole_num = -1 #黑洞入口重置        
            xmove = speed.call(level) * -1   #球向左 
        if(ball_rect.top <= 0):
            ymove = speed.call(level)        #球向下
            black_hole_num = -1 #黑洞入口重置        
            if (xmove <= 0):
                 xmove = speed.call(level) * -1
            elif (xmove >= 0) :
                 xmove = speed.call(level)
        if(ball_rect.bottom >= height ):
            ymove = speed.call(level) * -1   # 球向上
            black_hole_num = -1 #黑洞入口重置        
                
        if(ball_x < px+(pad_long/2) and ball_x > px-(pad_long/2) and py+20 > ball_rect.bottom > py):  #球的 x 介於 板子內的 x和 球底部的y 等於板子的y 
            ymove = speed.call(level) * -1  # 球向上   (速度介於 -2 到 -1)
            if (xmove == 0 ):
                 xmove = speed.call(level) * random.choice([-1, 1])
            soundwav.play()
            black_hole_num = -1 #黑洞入口重置        
            if ( len(blk) == 0 ):
                level += 1
                random_black_hole()
                sound_level_up.play()
                blk_add()
                time_tick = 0
        if (level == 2 and time_tick < 80 ):
            DrawText('第二關', font4 , bg , 677, 350)   #遊戲結束
            DrawText('速度加快', font4 , bg , 655, 450)   #遊戲結束
        if (level == 3 and time_tick < 80 ):
            DrawText('第三關', font4 , bg , 677, 350)   #遊戲結束
            DrawText('速度加快', font4 , bg , 655, 450)   #遊戲結束
           
        if (abs(xmove) == abs(ymove) == abs(-1)):
            xmove = xmove * 2
            ymove = ymove * 2
        
        if (ball_rect.bottom >= life_line ):
            life = life - 1 
            ball_x = 750 #random.randint(ball_rect.center[0]-50,ball_rect.center[0]+50)
            ball_y = 375
            xmove = 0            
            kick_off = True
            black_hole_num = -1 #黑洞入口重置        
            sound_drop.play()
            if (life <= 0):   #生命註解
                sound_dead.play()
                game_state = 'Game Fail'
          
        for i in range (len(blk)):
            #pg.draw.rect(bg, (200,20,0), (blk[i][0],blk[i][1],blk_width,blk_high))  #畫磚塊  (磚塊的寬 , 高)   
            bg.blit(brick_img,(blk[i][0],blk[i][1]))
        
            
        if( level >= 2 ):  #黑洞
            for i in range (len(black_hole_tup)):
                bg.blit(black_hole,black_hole_tup[i])
            
            for d in range (len(black_hole_tup)):
                if ( black_hole_tup[d][0] + black_hole_diameter >= ball_cx and
                     ball_cx >= black_hole_tup[d][0] and
                     black_hole_tup[d][1] + black_hole_diameter >= ball_cy  and 
                     ball_cy >= black_hole_tup[d][1] and black_hole_num != d ):
                     while True:
                         black_hole_num = random.randint(0,len(black_hole_tup)-1)
                         if (black_hole_num != d ):
                             break
                     ymove = ymove * -1
                     ball_x = black_hole_tup[black_hole_num][0] + 30
                     ball_y = black_hole_tup[black_hole_num][1] + 30
                     break
        
        if (len(blk)==0 and level == 3):
            game_state = 'Game Win'
       
    elif (game_state == 'Game Fail'):
        DrawText('GAME OVER', font6 , bg ,675, 325)   #遊戲結束 
        DrawText('此次獲得的分數:  '+str(score), font5 , bg , 490, 450)   #遊戲結束 
    elif (game_state == 'Game Win'):
        DrawText('恭喜過關', font4 , bg ,675, 325)   #遊戲結束 
        DrawText('此次獲得的分數:  '+str(score), font5 , bg , 490, 450)   #遊戲結束         
    ##----------------------- 
    DrawText('Score '+str(score), font1 , bg , 10 , 10)  
    DrawText('Life '+str(life), font1 , bg , 350 , 10)  
    screen.blit(bg, (0,0))   #繪製主頁面 
    ##-----------------------
    if ( kick_off == False):
        screen.blit(ball_image, ball_rect.topleft)  #繪製球，從球的左上方定位
    else:
        ball_x = 750 #random.randint(ball_rect.center[0]-50,ball_rect.center[0]+50)
        ball_y = 375
        screen.blit(ball_image, ball_rect.topleft)  #繪製球，從球的左上方定位
        if (life > 0):
            DrawText('跳起後繼續', font4 , screen , (width/2 - 139 ), (height/2 + 30 ))
    ##-----------------------
    screen.blit(image, pad_rect.topleft) #繪製板子，從板子的左上方定位
    ##-----------------------

    ##-----------------------
    '''
    if ishit != 1:
        screen.blit(brick,bk1.center)   #如果 ishit 不等於 1 在視窗上畫出磚塊
    '''    
    
    #print(clock.get_fps())    
    
    time_tick += 1
    
    pg.display.update()     #更新視窗
    
    
cv2.destroyAllWindows()
video.release()  
pg.quit()