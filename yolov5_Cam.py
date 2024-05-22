#pip install opencv-python
import cv2
import torch
import numpy as np

# 載入yolov5模型
model = torch.hub.load(repo_or_dir='yolov5',model='yolov5s',source='local') # n/s/m/l/x

# 啟用webcam
cap = cv2.VideoCapture(0)
while True:
    retval = cap.isOpened()
    if retval==False:
        retval = cv2.VideoCapture.open(0)
    else:
        break
print("Camera ON")
print("press \'q\' or esc to quit.")

# 迴圈讀取webcam的幀
while cap.isOpened():
    ret, frame = cap.read()

    # 使用模型獲取結果
    results = model(frame)
    #get result items
    items = eval(results.pandas().xyxy[0].to_json(orient="records"))
    
    # Render the new frame of detections
    new_frame = np.squeeze(results.render())
    
    cv2.imshow("Camera", new_frame)
    
    key = cv2.waitKey(1)
    if ret == False:
        print("Camera offline")
        break

    if key == 27 or key == ord('q'): #若按下 ESC 或 q 則關閉視窗
        break

cv2.VideoCapture.release()
if ret == False:
    input("press any key to quit")