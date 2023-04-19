import cv2
import os

# 定義影片目錄和影格目錄的路徑
video_dir = 'D:/project/vidoe/downup'
frame_dir = 'D:\project\picture\downup'

# 建立一個子資料夾名稱的清單
#action_names = ['wave', 'downup', 'grab']

#for action_name in action_names:
#    action_path = os.path.join(frame_dir, action_name)
#    os.makedirs(action_path, exist_ok=True)


# Loop through the videos and extract frames
for video_file in os.listdir(video_dir):
    # Load video
    video_path = os.path.join(video_dir, video_file)
    cap = cv2.VideoCapture(video_path)

    # Get the action name from the video file name
    action_name = os.path.splitext(video_file)[0].split('_')[-1]

    # Create a subdirectory for the action if it doesn't exist
    action_path = os.path.join(frame_dir, action_name)
    os.makedirs(action_path, exist_ok=True)

    # Extract frames from the video and save them to the corresponding action directory
    frame_count = 0
    while True:
        # Read frame
        ret, frame = cap.read()
        
        if not ret:
            break
        #Pvideo_file.split(".")[0]}
        # Save frame as image file
        frame_file = f'{video_file.split(".")[0]}_frame_{frame_count:05d}.jpg'
        frame_file_path = os.path.join(action_path, frame_file)
       
        cv2.imwrite(frame_file_path, frame)
        frame_count += 1
        
    cap.release()