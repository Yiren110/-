import cv2
import mediapipe as mp
import os

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(static_image_mode=False, max_num_hands=2, min_detection_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils
# 處理影格
def process_frame(frame):
    # 轉換為RGB格式
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 檢測手部關節
    results = hands.process(frame)

    
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


    # 轉換為BGR格式
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    return frame
    
# 處理所有子資料夾中的圖片
def process_directory(input_dir, output_dir):
    for root, dirs, files in os.walk(input_dir):
        for file_name in files:
            if file_name.endswith('.jpg') or file_name.endswith('.png'):
                input_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(input_path, input_dir)
                output_path = os.path.join(output_dir, relative_path)
                
                # 建立輸出資料夾
                os.makedirs(os.path.dirname(output_path), exist_ok=True)

                frame = cv2.imread(input_path)
                processed_frame = process_frame(frame)
                cv2.imwrite(output_path, processed_frame)
                print(file_name)
# 使用函數，只需替換為你的輸入和輸出資料夾路徑
process_directory('D:/project/picture/downtoup', 'D:/project/picture plus points/downtoup')
# 資料夾中的所有影格進行處理
#for file_name in os.listdir('D:/project/picture/downup/00000'):
#    if file_name.endswith('.jpg') or file_name.endswith('.png'):
 #       file_path = os.path.join('D:/project/picture/downup/00000', file_name)
#

 #       folder_path = 'D:/project/picture plus points/downup/00000'
  #      if not os.path.isdir(folder_path):
   #         os.mkdir(folder_path)
    #        
     #   output_path = os.path.join(folder_path, file_name)
      # processed_frame = process_frame(frame)
       # cv2.imwrite(output_path, processed_frame)
        #print(file_name)


