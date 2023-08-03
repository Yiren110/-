import tensorflow as tf
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, LSTM, Dense
from tensorflow.keras.models import Sequential
from tensorflow.data import TFRecordDataset

# 解析 TFRecord 檔案
def parse_tfrecord_fn(example):
    feature_description = {
        'image': tf.io.FixedLenFeature([], tf.string),  # 影像數據
        'keypoints': tf.io.FixedLenFeature([63], tf.float32),  # 關鍵點
        'label': tf.io.FixedLenFeature([], tf.int64),  # 標籤
    }
    example = tf.io.parse_single_example(example, feature_description)  # 解析單一樣本
    image = tf.io.decode_jpeg(example['image'])  # 解碼 jpeg 影像
    image = tf.image.resize(image, [240, 320])  # 調整影像大小
    image = image / 255.0  # 將影像標準化到 [0,1] 的範圍
    keypoints = example['keypoints']  # 獲取關鍵點
    label = example['label']  # 獲取標籤
    return image, keypoints, label

# 建立模型
def create_model():
    model = Sequential()
    model.add(Conv2D(32, (3, 3), activation='relu', input_shape=(240, 320, 3)))  # 卷積層
    model.add(MaxPooling2D((2, 2)))  # 最大池化層
    model.add(Conv2D(64, (3, 3), activation='relu'))  # 卷積層
    model.add(MaxPooling2D((2, 2)))  # 最大池化層
    model.add(Conv2D(64, (3, 3), activation='relu'))  # 卷積層
    model.add(Flatten())  # 拉平層
    model.add(Dense(64, activation='relu'))  # 全連接層
    model.add(LSTM(32, return_sequences=True))  # LSTM 層
    model.add(LSTM(32))  # LSTM 層
    model.add(Dense(3, activation='softmax'))  # 輸出層

    model.compile(optimizer='adam',
                  loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True),
                  metrics=['accuracy'])  # 編譯模型

    return model

# 訓練模型
def train_model(model, dataset, epochs=10):
    history = model.fit(dataset, epochs=epochs)  # 訓練模型
    return history

# 儲存模型
def save_model(model, model_path):
    model.save(model_path)  # 儲存模型

# 讀取所有 TFRecord 檔案
tfrecord_files = tf.io.gfile.glob('D:/project/tfr/*/*.tfrecord')  # 獲取所有 TFRecord 檔案的路徑
dataset = TFRecordDataset(tfrecord_files)  # 讀取 TFRecord 檔案
dataset = dataset.map(parse_tfrecord_fn)  # 解析資料
dataset = dataset.batch(32)  # 批次化資料

# 建立和訓練模型
model = create_model()  # 建立模型
history = train_model(model, dataset, epochs=10)  # 訓練模型

# 儲存模型
save_model(model, 'D:/project/model/my_model')  # 儲存模型
