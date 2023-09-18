import cv2
import mediapipe as mp
import math
import pyautogui
import numpy as np
cap=cv2.VideoCapture(0)
mpHands=mp.solutions.hands
hands=mpHands.Hands()
mpDraw=mp.solutions.drawing_utils

def vector_2d_angle(v1,v2):
    v1_x = v1[0]
    v1_y = v1[1]
    v2_x = v2[0]
    v2_y = v2[1]
    try:
        angle_= math.degrees(math.acos((v1_x*v2_x+v1_y*v2_y)/(((v1_x**2+v1_y**2)**0.5)*((v2_x**2+v2_y**2)**0.5))))
    except:
        angle_ = 180
    return angle_
def hand_angle(hand_):
    angle_list = []
    # thumb 大拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[2][0])),(int(hand_[0][1])-int(hand_[2][1]))),
        ((int(hand_[3][0])- int(hand_[4][0])),(int(hand_[3][1])- int(hand_[4][1])))
        )
    angle_list.append(angle_)
    # index 食指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])-int(hand_[6][0])),(int(hand_[0][1])- int(hand_[6][1]))),
        ((int(hand_[7][0])- int(hand_[8][0])),(int(hand_[7][1])- int(hand_[8][1])))
        )
    angle_list.append(angle_)
    # middle 中指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[10][0])),(int(hand_[0][1])- int(hand_[10][1]))),
        ((int(hand_[11][0])- int(hand_[12][0])),(int(hand_[11][1])- int(hand_[12][1])))
        )
    angle_list.append(angle_)
    # ring 無名指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[14][0])),(int(hand_[0][1])- int(hand_[14][1]))),
        ((int(hand_[15][0])- int(hand_[16][0])),(int(hand_[15][1])- int(hand_[16][1])))
        )
    angle_list.append(angle_)
    # pink 小拇指角度
    angle_ = vector_2d_angle(
        ((int(hand_[0][0])- int(hand_[18][0])),(int(hand_[0][1])- int(hand_[18][1]))),
        ((int(hand_[19][0])- int(hand_[20][0])),(int(hand_[19][1])- int(hand_[20][1])))
        )
    angle_list.append(angle_)
    return angle_list
def hand_pos(finger_angle):
    f1 = finger_angle[0]   # 大拇指角度
    f2 = finger_angle[1]   # 食指角度
    f3 = finger_angle[2]   # 中指角度
    f4 = finger_angle[3]   # 無名指角度
    f5 = finger_angle[4]   # 小拇指角度

    # 小於 50 表示手指伸直，大於等於 50 表示手指捲縮
    if f1>50 and f2<50 and f3>=50 and f4>=50  and f5<50 :
        return 'rouk'
    elif f1>50 and f2<50 and f3>=50 and f4>=50 and f5>50:
        return 'point'
    elif f2<50 and f3<50 and f4<50 and f5<50:
        return 'open'
    elif f1>50 and f2>50 and f3>=50 and f4>=50 and f5>50:
        return'close'
    elif f1>=50 and f2>=50 and f3<50 and f4<50 and f5<50:
        return 'ok'
    elif f2<=50 and f3<50 and f4<50 and f5>50:
        return 'fouropen'
    else:
        return ''
strokes = []  # 保存所有筆畫的列表
current_stroke = []  # 保存當前筆畫的列表

def handle_open_hand(handLms, img, canvas, last_point,leftpointX,leftpointY,rightpointX,rightpointY):
    global current_stroke  # 使用全局變量
    thumbX = int(handLms.landmark[4].x * img.shape[1])
    thumbY = int(handLms.landmark[4].y * img.shape[0])

    if leftpointX <= thumbX <= rightpointX and leftpointY <= thumbY <= rightpointY:
        current_point = (thumbX, thumbY)
        current_stroke.append(current_point)
        if last_point is not None:
            cv2.line(canvas, last_point, current_point, (0, 255, 0), 5)
        last_point = current_point
    else:
        if current_stroke:
            strokes.append(current_stroke)
        current_stroke = []
        last_point = None
        print('hi nice to meet you')
    return last_point    
    

def save_strokes_to_txt(strokes, filename="D:/project/for2/strokes.txt"):
    print("Saving strokes to file...")  # 調試信息
    print("Number of strokes:", len(strokes))  # 顯示筆劃的數量
    f = open(filename, "a")
    try:
        for stroke in strokes:
            stroke_str = ";".join([f"({x},{y})" for x, y in stroke])
            f.write(stroke_str + "\n")
    finally:
        f.close()

            
            
canvas = None
last_point = None
rectangle_coordinates = None
rectangle_fixed = False
doing_open_hand_actions = False  # 新增狀態變量
while 1:
    ret , img=cap.read()
    screenWidth, screenHeight = pyautogui.size()#螢幕大小
    imgheight=int(img.shape[0])#攝像頭畫面大小
    imgwidth=int(img.shape[1])
    rx=screenWidth / imgwidth
    ry=screenHeight/imgheight
    img = cv2.flip(img, 1)
    
    if rx>ry :
        rx=ry
    elif rx<ry:
        ry=rx
    if ret:
        imgRGB=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        result=hands.process(imgRGB)
        #print(result.multi_hand_landmarks)
        
        if canvas is None:
            canvas = np.zeros(shape=[img.shape[0], img.shape[1], 3], dtype=np.uint8)
            
        if result.multi_hand_landmarks:
            for index, handLms in enumerate(result.multi_hand_landmarks):
                # 新增：識別左手或右手
                handedness = result.multi_handedness[index].classification[0].label
                print("Handedness: ", handedness)
                
                mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
                
                 # 取得手勢所回傳的內容
                
                for i ,lm in enumerate(handLms.landmark):
                    xpos=int(lm.x*screenWidth)#在螢幕上的座標screenWidth
                    ypos=int(lm.y*screenHeight)
                    #print(i,xpos,ypos)
                    
                finger_points = []                   # 記錄手指節點座標的串列
                for i in handLms.landmark:
                    # 將 21 個節點換算成座標，記錄到 finger_points
                    x = i.x*imgheight
                    y = i.y*imgwidth#在畫面上的座標
                    finger_points.append((x,y))
                
                finger_angle = hand_angle(finger_points) # 計算手指角度，回傳長度為 5 的串列
                    #print(finger_angle)                     # 印出角度 ( 有需要就開啟註解 )
                text=hand_pos(finger_angle) # 取得手勢所回傳的內容
                fingerX=(1920-handLms.landmark[7].x *screenWidth)#食指末端座標
                fingerY=handLms.landmark[7].y*screenHeight 
                    
                    
                if text == 'open':
                    doing_open_hand_actions = True  # 更新狀態變量
                    if handedness=='Right':
                        leftpointX = int((handLms.landmark[6].x * img.shape[1]) - 50)  # 矩形左上角的座標
                        leftpointY = int((handLms.landmark[6].y * img.shape[0]) - 50)
                        rightpointX = int(handLms.landmark[17].x * img.shape[1])  # 矩形右下角的座標
                        rightpointY = int((handLms.landmark[17].y * img.shape[0]) + 50)
                        last_point = handle_open_hand(handLms, img, canvas, last_point,leftpointX,leftpointY,rightpointX,rightpointY)
                        
                        if not rectangle_fixed:  # 如果矩形還沒有固定，則更新座標
                            # ... 更新 rectangle_coordinates ...
                            rectangle_coordinates = (leftpointX, leftpointY, rightpointX, rightpointY)
                        rectangle_fixed = True  # 固定矩形
                    else :
                        leftpointX = int((handLms.landmark[20].x * img.shape[1]) - 50)  # 矩形左上角的座標
                        leftpointY = int((handLms.landmark[20].y * img.shape[0]) - 50)
                        rightpointX = int(handLms.landmark[5].x * img.shape[1])  # 矩形右下角的座標
                        rightpointY = int((handLms.landmark[5].y * img.shape[0]) + 50)
                        last_point = handle_open_hand(handLms, img, canvas, last_point,leftpointX,leftpointY,rightpointX,rightpointY)
                        if not rectangle_fixed:  # 如果矩形還沒有固定，則更新座標
                            # ... 更新 rectangle_coordinates ...
                            rectangle_coordinates = (leftpointX, leftpointY, rightpointX, rightpointY)
                        rectangle_fixed = True  # 固定矩形
                elif text == 'close':
                    doing_open_hand_actions = False  # 更新狀態變量
                    rectangle_coordinates = None # 清空矩形座標
                    rectangle_fixed = False  # 解除矩形固定
                    canvas = np.zeros(shape=[img.shape[0], img.shape[1], 3], dtype=np.uint8)
                    strokes.clear()
                # ...（您原本握拳時要做的事，例如清空矩形座標）
                if doing_open_hand_actions:
                    if text=='rouk':
                        if strokes:  # 檢查 strokes 列表是否不為空
                            strokes.pop()  # 刪除最後一個筆劃
                        current_stroke = []  # 清空當前筆劃
                        print('it is pop')
                    elif text=='fouropen':
                        if current_stroke:  # 檢查當前筆劃是否不為空
                            strokes.append(current_stroke)  # 將當前筆劃添加到 strokes 列表中
                        current_stroke = []  # 清空當前筆劃
                        print('it is append')
                    elif text=='ok':
                        save_strokes_to_txt(strokes)
                        strokes = []  # 清空筆畫列表以便於下次繪圖
                        print ('it is save')
                elif text=='rouk':
                    pyautogui.moveTo(100, 100, duration = 1.5)
                elif fingerX < 10 or fingerX > screenWidth - 10 or fingerY < 10 or fingerY > screenHeight - 10:
                    pyautogui.moveTo(screenWidth / 2, screenHeight / 2)
                elif text=='point':
                    pyautogui.moveTo(fingerX, fingerY, duration = 0.3)
                
                    # 如果有有效的矩形座標，則繪製矩形
                if rectangle_coordinates is not None:
                    cv2.rectangle(img, (rectangle_coordinates[0], rectangle_coordinates[1]),(rectangle_coordinates[2], rectangle_coordinates[3]), (0, 0, 255), 5)
                        
                   
        # 將 canvas 上的繪圖加到原始圖像上
        img = cv2.add(img, canvas)            
        #img = cv2.addWeighted(img, 0.5, canvas, 0.5, 0) 
        cv2.imshow('img',img)
    if cv2.waitKey(10)==ord('q'):
        break
cv2.destroyAllWindows()
    
    
    