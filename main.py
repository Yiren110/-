import cv2
import time
import os

def record_video(output_dir, resolution=(640, 480)):
    # 選擇第一個攝像頭
    cap = cv2.VideoCapture(0)

    # 設置攝像頭的解析度
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])

    # 定義視頻的編碼
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    recording = False  # 初始時未開始錄製
    out = None  # 初始 VideoWriter 為 None

    while(cap.isOpened()):
        # 讀取攝像頭的畫面
        ret, frame = cap.read()
        if ret:
            # 顯示 frame
            cv2.imshow('frame', frame)

            # 檢查是否有按鍵被按下
            key = cv2.waitKey(1) & 0xFF
            
            # 如果按下 'q'，則結束程式
            if key == ord('q'):
                break
            # 如果按下 'r'，則開始或停止錄製
            elif key == ord('r'):
                if recording:
                    # 如果已在錄製，則停止錄製
                    recording = False
                    out.release()
                    out = None
                else:
                    # 如果未在錄製，則開始錄製
                    recording = True
                    filename = time.strftime("%Y%m%d-%H%M%S") + ".mp4"
                    output_path = os.path.join(output_dir, filename)
                    print(filename)
                    out = cv2.VideoWriter(output_path, fourcc, 20.0, resolution)

            # 如果正在錄製，則將 frame 寫入輸出視頻檔案
            if recording:
                out.write(frame)
        else:
            break

    # 釋放攝像頭和 VideoWriter 的資源
    cap.release()
    if out is not None:
        out.release()
    cv2.destroyAllWindows()

# 使用上面的函數，只需替換為您要輸出的資料夾路徑
record_video("D:\\project\\mp4")
