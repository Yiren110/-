import tensorflow as tf
import cv2
import numpy as np
import os
import mediapipe as mp
from pathlib import Path

# 定義手勢類別和標籤之間的對應關係
label_map = {
    'downtoup': 0,
    'point': 1,
    'grab': 2
}

def create_tfrecord_example(image, keypoints, label):
    # 建立特徵字典
    feature = {
        'image': tf.train.Feature(bytes_list=tf.train.BytesList(value=[tf.io.encode_jpeg(image).numpy()])),
        'keypoints': tf.train.Feature(float_list=tf.train.FloatList(value=keypoints)),
        'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
    }

    # 建立TFRecord格式的範例
    example = tf.train.Example(features=tf.train.Features(feature=feature))

    return example

def write_frames_to_tfrecord(frames_dir, tfrecord_filename, gesture):
    frames_dir = Path(frames_dir)
    label = label_map[gesture]
    # 建立TFRecord檔案
    tfrecord_filename = tfrecord_filename.with_name(f"{gesture}_{frames_dir.name}.tfrecord")
    with tf.io.TFRecordWriter(str(tfrecord_filename)) as writer:
        # 循環遍歷子文件夾中的每個影像
        for image_file in sorted(os.listdir(frames_dir)):
            # 從檔案讀取影像
            image_path = frames_dir / image_file
            image = cv2.imread(str(image_path))
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (640, 480))

            # 初始化手部偵測模型
            mp_hands = mp.solutions.hands.Hands(static_image_mode=True, max_num_hands=1, min_detection_confidence=0.5)

            # 將影像傳入手部偵測模型進行偵測
            results = mp_hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

            # 如果有偵測到手部，就從手部關鍵點中提取21個關鍵點的座標
            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks[0]
                keypoints = [lmk.x for lmk in hand_landmarks.landmark]
                keypoints.extend([lmk.y for lmk in hand_landmarks.landmark])
                keypoints.extend([lmk.z for lmk in hand_landmarks.landmark])
                keypoints = np.array(keypoints).flatten().tolist()

                # 建立TFRecord格式的範例
                example = create_tfrecord_example(image, keypoints, label)

                # 寫入TFRecord檔案
                writer.write(example.SerializeToString())
    print(f'TFRecord file created: {tfrecord_filename}')

# 定義存儲影片分解成影像的資料夾
frames_dirs = [Path('D:/project/picture_plus_points/downtoup'), Path('D:/project/picture_plus_points/point'), Path('D:/project/picture_plus_points/grab')]
# 定義保存TFRecord檔案的資料夾
tfrecord_dirs = [Path('D:/project/tfr/downtoup'), Path('D:/project/tfr/grab'), Path('D:/project/tfr/point')]

for frames_dir, tfrecord_dir in zip(frames_dirs, tfrecord_dirs):
    gesture = frames_dir.name
    video_dirs = os.listdir(frames_dir)
    for video_dir in video_dirs:
        tfrecord_filename = tfrecord_dir / f"{gesture}_{video_dir}.tfrecord"
        video_frames_dir = frames_dir / video_dir
        if video_frames_dir.is_dir():
            write_frames_to_tfrecord(video_frames_dir, tfrecord_filename, gesture)
