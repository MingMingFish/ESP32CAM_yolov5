import cv2
import torch
import numpy as np

import os
from PIL import ImageFont, ImageDraw, Image
from urllib.request import urlopen
import imutils
import time

#已存video數量:
def fileCount(dir):
    return len(os.listdir(dir))

if not os.path.exists(os.path.join('video')):
    os.mkdir(os.path.join('video'))
cam_mode = 'net-cam'  # 'webcam' / 'net-cam
write_video = False
record_width, record_height = 640,480
video_out = "video/"+"out_"+str(fileCount("video")+1)+".avi"
output_rotate = False
rotate = 180

#ESP32-CAM
url="http://192.168.100.6:81/stream"
CAMERA_BUFFRER_SIZE=4096

#fps count
start = time.time()


def fps_count(num_frames):
    end = time.time()
    seconds = end - start
    fps  = num_frames / seconds;
    print("Estimated frames per second : {0}".format(fps))
    return fps

def printText(bg, txt, color=(0,255,0,0), size=0.7, pos=(0,0), type="Chinese"):
    (b,g,r,a) = color

    if(type=="English"):
        cv2.putText(bg,  txt, pos, cv2.FONT_HERSHEY_SIMPLEX, size,  (b,g,r), 2, cv2.LINE_AA)

    else:
        ## Use simsum.ttf to write Chinese.
        fontpath = "fonts/wt009.ttf"
        font = ImageFont.truetype(fontpath, int(size*10*4))
        img_pil = Image.fromarray(bg)
        draw = ImageDraw.Draw(img_pil)
        draw.text(pos,  txt, font = font, fill = (b, g, r, a))
        bg = np.array(img_pil)

    return bg

def read_stream():
    global bts
    for _ in iter(int, 1):
        bts+=stream.read(CAMERA_BUFFRER_SIZE)
        jpghead=bts.find(b'\xff\xd8')
        jpgend=bts.find(b'\xff\xd9')

        img = None
        height,width = 0,0
        
        if jpghead>-1 and jpgend>-1:
            jpg=bts[jpghead:jpgend+2]
            bts=bts[jpgend+2:]
                
            try:
                img=cv2.imdecode(np.frombuffer(jpg,dtype=np.uint8),cv2.IMREAD_UNCHANGED)    
                #v=cv.flip(img,0)
                #h=cv.flip(img,1)
                #p=cv2.flip(img,-1)    
                #frame=p
                height, width=img.shape[:2]
                # img=cv2.resize(img,(record_width, record_height))
                # print(img.shape)
            except:
                # img = None
                # print("no data received.")
                continue
            break
    return img,(width,height)

if cam_mode == 'webcam':
    #設定攝影機
    cap = cv2.VideoCapture(0)
    #判定是否有裝攝影機
    if not cap.isOpened():
        print("無法打開相機")
        exit()
    #設定解析度
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
elif cam_mode == 'net-cam':
    if(write_video is True):
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(video_out,fourcc, 20.0, (record_width,record_height))
    
    stream=urlopen(url)
    
    frameID = 0
    frame = None

#模型設定
model = torch.hub.load(repo_or_dir='yolov5',model='yolov5x',source='local') # s/m/l/x

#執行
bts=b''
# while(True):
for _ in iter(int, 1): # infinite loop
    if cam_mode == 'webcam':
        #擷取影像
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
    elif cam_mode == 'net-cam':
        frame, (width, height) = read_stream()
        if frame is not None:
            if(output_rotate is True):
                frame = imutils.rotate(frame, rotate)
    
    #模型使用
    results = model(frame)
    
    #紀錄物體
    data = eval(results.pandas().xyxy[0].to_json(orient="records"))
    #物體數量
    item_count = len(data)
    
    #物體名稱
    item_name = []
    while len(data):
        item_name.append(data[0]['name'])
        data.pop(0)
        #顯示名稱
        # print(item_name)
    
    new_frame = np.squeeze(results.render())
    #顯示影像
    cv2.imshow('live', new_frame)

    #按下 q 鍵離開迴圈
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #關閉該攝影機裝置
        if cam_mode == 'webcam':
            cap.release()
        if(write_video is True):
            out.release()
        break
    
cv2.destroyAllWindows()