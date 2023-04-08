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

    # 繪製方框
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks)

    # 轉換為BGR格式
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    
    return frame
    
# 處理影片
def process_video(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    while cap.isOpened():
        ret, frame = cap.read()

        if ret:
            processed_frame = process_frame(frame)
            out.write(processed_frame)

            cv2.imshow('frame', processed_frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# 資料夾中的所有影格進行處理
for file_name in os.listdir('D:\project\picture\dowmup00000'):
    if file_name.endswith('.jpg') or file_name.endswith('.png'):
        file_path = os.path.join('D:\project\picture\dowmup00000', file_name)
        

        folder_path = 'D:/project/upup'
        
        


        



       
            
        output_path = os.path.join(folder_path, file_name)
        frame = cv2.imread(file_path)
        processed_frame = process_frame(frame)
        cv2.imwrite(output_path, processed_frame)
        print(file_name)


