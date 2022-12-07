import os
import time
import numpy as np
from urllib.request import urlopen
import torch
import cv2
# pygame works better on raspberry pi
import pygame
# pygame has to be initialized before using
pygame.init()

#ESP32-CAM
url = 'http://192.168.1.102'
stream_url= f"{url}:81/stream"
CAMERA_BUFFER_SIZE=4096

# Set shape of video
UXGA = 13 # 1600 * 1200
SXGA = 12 # 1280 * 1024
HD   = 11 # 1280 *  720
XGA  = 10 # 1024 *  768 
SVGA = 9  #  800 *  600
VGA  = 8  #  640 *  480

#set/load yolov5 model
model = torch.hub.load(repo_or_dir='yolov5',model='yolov5s',source='local') # n/s/m/l/x

def read_stream():
    global bts
    for _ in iter(int, 1):
        bts += stream.read(CAMERA_BUFFER_SIZE)
        jpghead = bts.find(b'\xff\xd8')
        jpgend = bts.find(b'\xff\xd9')

        img = None
        height, width = 0, 0
        
        if jpghead >-1 and jpgend >- 1:
            jpg = bts[jpghead:jpgend+2]
            bts = bts[jpgend+2:]

            try:
                img=cv2.imdecode(np.frombuffer(jpg,dtype=np.uint8),cv2.IMREAD_UNCHANGED)
                height, width = img.shape[:2]
            except:
                continue
            break
    return img, (width, height)

timers = {}
bts = b''

if __name__ == "__main__":
    try:
        for _ in iter(int, 1): # infinite loop:
            try:
                print('Connecting ESP32-CAM from',stream_url)
                urlopen(f'{url}/control?var=framesize&val={VGA}') # set graph quality
                stream=urlopen(stream_url)
                break
            except:
                print("Connect Failed.")
                try_again=input('Try again?(Y/[N]):').capitalize()
                if try_again =='Y':
                    continue
                else:
                    os._exit(0)
        print('Connected ESP32 from',stream_url)

        for _ in iter(int, 1): # infinite loop:
            frame, (width, height) = read_stream()
            alert_vol = (width*height)//4

            results = model(frame)
            #get result items
            items = eval(results.pandas().xyxy[0].to_json(orient="records"))
            #Count items
            item_count = len(items)

            items_name =[]
            for item in items:
                # item['xmin', 'name', 'ymin', 'xmax', 'ymax', 'confidence', 'class', 'name']
                volume = int(item['xmax'] - item['xmin']) * int(item['ymax'] - item['ymin'])    # 計算體積
                if volume >= alert_vol and item['confidence'] >= 0.5:
                    items_name.append(item['name'])
                    if time.time() - timers.setdefault(item['name'], time.time()) >= 3:
                        timers[item['name']] = time.time()
                        try:
                            sound = pygame.mixer.Sound(os.path.join('audio', item['name'] + '.mp3'))
                        except FileNotFoundError:
                            print('not found in dictionary')
                            sound = pygame.mixer.Sound(os.path.join('audio', 'others.mp3')) # not added yet
                        finally:
                            sound.play()

            # Show detections (only big enough ones)
            if items_name:
                print(items_name)

            # Render the new frame of detections
            new_frame = np.squeeze(results.render())
            
            # Show frame
            if new_frame is not None:
                cv2.imshow("ESP32-CAM", new_frame)
                k=cv2.waitKey(1)
            
            # Break when press 'q'
            if k & 0xFF==ord('q'):
                cv2.destroyAllWindows()
                break
    # when pressed Ctrl+C
    except KeyboardInterrupt:
        print("Application broke down by user")
        os.system("pause")