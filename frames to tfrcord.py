import tensorflow as tf
import cv2
import numpy as np
import os
import mediapipe as mp
# 定義存儲標籤圖像的目錄路徑
frames_dir = 'D:/project/picture/downup/00000'

# 定義 TFRecord 文件的路徑以保存數據集
tfrecord_filename = 'D:/project/tfr/downup/downup00000.tfrecord'

# 定義手勢類別和標籤之間的對應關係
label_map = {
    'downup': 0,
    'point': 1,
    'grab': 2
}

# 定義函數將影格和標籤轉換為TFRecord格式
def create_tfrecord_example(image, label):
    # 將影格轉換為RGB格式
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # 將影格的大小調整為224x224像素
    image = cv2.resize(image, (224, 224))

    # 建立特徵字典
    feature = {
        'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[image.tobytes()])),
        'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
        'keypoints': tf.train.Feature(float_list=tf.train.FloatList(value=keypoints)),
    }


    # 建立TFRecord格式的範例
    example = tf.train.Example(features=tf.train.Features(feature=feature))

    return example


# 循環遍歷標記的圖像並保存為 TFRecord
with tf.io.TFRecordWriter(tfrecord_filename) as writer:
    for image_file in os.listdir(frames_dir):
        
        # 從檔案名稱中提取手勢標籤
        gesture = image_file.split('_')[0]
        label = label_map[gesture]

        # 取得影格檔案路徑
        image_path = os.path.join(frames_dir, image_file)

        # 從檔案讀取影格
        image = cv2.imread(image_path)

        # 將影格的大小調整為224x224像素
        image = cv2.resize(image, (224, 224))

        # 初始化手部偵測模型
        mp_hands = mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)

        # 將影格傳入手部偵測模型進行偵測
        results = mp_hands.process(image)

        # 如果有偵測到手部，就從手部關鍵點中提取21個關鍵點的座標
        if results.multi_hand_landmarks:
            hand_landmarks = results.multi_hand_landmarks[0]
            keypoints = [lmk.x for lmk in hand_landmarks.landmark]
            keypoints.extend([lmk.y for lmk in hand_landmarks.landmark])
            keypoints.extend([lmk.z for lmk in hand_landmarks.landmark])
            keypoints = np.array(keypoints).flatten().tolist()
            
            # 建立TFRecord格式的範例
            example = create_tfrecord_example(keypoints, label)
            
            # 寫入TFRecord檔案
            writer.write(example.SerializeToString())