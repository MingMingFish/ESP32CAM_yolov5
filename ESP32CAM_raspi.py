import os
import time
from urllib.request import urlopen
import torch
import cv2
# pygame works better on raspberry pi
import pygame
# pygame has to be initialized before using
pygame.init()

#ESP32-CAM
url = 'http://192.168.1.101'
stream_url= f"{url}:81/stream"
CAMERA_BUFFER_SIZE=4096

# Set shape of video
UXGA = 13 # 1600 * 1200
SXGA = 12 # 1280 * 1024
HD   = 11 # 1280 *  720
XGA  = 10 # 1024 *  768 
SVGA = 9  #  800 *  600
VGA  = 8  #  640 *  480

#模型設定
model = torch.hub.load(repo_or_dir='yolov5',model='yolov5n',source='local') # s/m/l/x

def read_stream():
    global bts

    for _ in iter(int, 1): # infinite loop:
        bts+=stream.read(CAMERA_BUFFER_SIZE)
        jpghead=bts.find(b'\xff\xd8')
        jpgend=bts.find(b'\xff\xd9')
        #print(f"jpghead: {jpghead}, jpgend: {jpgend}")

        if jpghead>-1 and jpgend>-1:
            jpg=bts[jpghead:jpgend+2]
            bts=bts[jpgend+2:]
            break
    return jpg

bts=b''
if __name__ == "__main__":
    try:
        for _ in iter(int, 1): # infinite loop:
            try:
                print('Connecting ESP32-CAM from ',stream_url)
                urlopen(f'{url}/control?var=framesize&val={HD}') # set graph quality
                stream=urlopen(stream_url)
                break
            except:
                print("Connect Failed.")
                tryagain=input('Try again?(Y/[N]): ').capitalize()
                if tryagain =='Y':
                    continue
                else:
                    os._exit(0)
        print('Connected ESP32 from ',stream_url)

        timers =    {'person': 0, 'bicycle': 0, 'car': 0, 'motorcycle': 0, 'airplane': 0, 'bus': 0, 'train': 0, 'truck': 0, 'boat': 0, 'traffic light': 0, 'fire hydrant': 0, 'stop sign': 0, 
                    'parking meter': 0,'bench': 0, 'bird': 0, 'cat': 0, 'dog': 0, 'horse': 0, 'sheep': 0, 'cow': 0, 'elephant': 0, 'bear': 0,'zebra': 0, 'giraffe': 0, 'backpack': 0, 
                    'umbrella': 0, 'handbag': 0, 'tie': 0, 'suitcase': 0, 'frisbee': 0, 'skis': 0, 'snowboard': 0, 'sports ball': 0, 'kite': 0, 'baseball bat': 0, 'baseball glove': 0, 
                    'skateboard': 0, 'surfboard': 0, 'tennis racket': 0,'bottle': 0, 'wine glass': 0, 'cup': 0, 'fork': 0, 'knife': 0, 'spoon': 0, 'bowl': 0, 'banana': 0, 'apple': 0,
                    'sandwich': 0, 'orange': 0, 'broccoli': 0, 'carrot': 0,'hot dog': 0, 'pizza': 0, 'donut': 0, 'cake': 0, 'chair': 0, 'couch': 0, 'potted plant': 0, 'bed': 0, 'dining table': 0,
                    'toilet': 0, 'tv': 0, 'laptop': 0, 'mouse': 0, 'remote': 0, 'keyboard': 0, 'cell phone': 0, 'microwave': 0, 'oven': 0, 'toaster': 0, 'sink': 0, 'refrigerator': 0, 
                    'book': 0, 'clock': 0, 'vase': 0, 'scissors': 0, 'teddy bear': 0, 'hair drier': 0, 'toothbrush': 0}
        for _ in iter(int, 1): # infinite loop:
            frame = read_stream()
            results = model(frame)
            for r in results:
                if time.time - timers[r] >= 5:
                        timers[r] = time.time()
                        sound = pygame.mixer.Sound(os.path.join('audio', r))
                        sound.play()

            if frame is not None:
                cv2.imshow("ESP32-CAM", frame)
                k=cv2.waitKey(1)
            if k & 0xFF==ord('q'):
                cv2.destroyAllWindows()
                break
    except KeyboardInterrupt:
        print("Application broke down by user")
        os.system("pause")