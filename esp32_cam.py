import cv2
import torch
import numpy as np

#設定攝影機
cap = cv2.VideoCapture(0)
#判定是否有裝攝影機
if not cap.isOpened():
    print("無法打開相機")
    exit()
#設定解析度
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 270)

#模型設定
model = torch.hub.load(repo_or_dir='yolov5',model='yolov5s',source='local')

#執行
while(True):
    #擷取影像
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame (stream end?). Exiting ...")
        break
    
    #模型使用
    results = model(frame)
    new_frame = np.squeeze(results.render())
    #顯示影像
    cv2.imshow('live', new_frame)

    #按下 q 鍵離開迴圈
    if cv2.waitKey(1) == ord('q'):
        break
    
#關閉該攝影機裝置
cap.release()
cv2.destroyAllWindows()