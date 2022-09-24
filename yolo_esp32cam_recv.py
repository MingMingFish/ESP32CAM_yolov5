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

write_video = False
record_width, record_height = 640,480
video_out = "video/"+"out_"+str(fileCount("video")+1)+".avi"
output_rotate = False
rotate = 180

#ESP32-CAM
url="http://192.168.100.9:81/stream"
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
    if item_count:
        item_name = []
        for item in data:
            # item['xmin', 'name', 'ymin', 'xmax', 'ymax', 'confidence', 'class', 'name']
            volume = int(item['xmax'] - item['xmin']) * int(item['ymax'] - item['ymin'])    # 計算體積
            if volume >= 129600 and item['confidence'] >= 0.5:                              # 只記錄 體積大於[360*360=129600] & 可信度>=0.5 的物件
                item_name.append(item['name'])
                # print(f"{item['name']}: {int(item['xmax'] - item['xmin']) * int(item['ymax'] - item['ymin'])}")
        if item_name:
            print(item_name)
    
    new_frame = np.squeeze(results.render())
    #顯示影像
    cv2.imshow('live', new_frame)

    #按下 q 鍵離開迴圈
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #結束錄影
        if(write_video is True):
            out.release()
        break

cv2.destroyAllWindows()