import os
from PIL import ImageFont, ImageDraw, Image
from urllib.request import urlopen
import cv2
import time
import numpy as np
import socket

#獲取本機ip
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip

#已存video數量:
def fileCount(dir):
    return len(os.listdir(dir))

connect_server=True
write_video = False
record_width, record_height = 640,480

output_rotate = False
rotate = 180

if(write_video is True):
    outputdir = 'video'
    if not os.path.exists(outputdir):
        os.mkdir(outputdir)
    video_num = str(fileCount("video")+1)

#ESP32-CAM
url="http://192.168.100.11:81/stream"
CAMERA_BUFFER_SIZE=4096
UXGA = 13 # 1600 * 1200
SXGA = 12 # 1280 * 1024
HD   = 11 # 1280 *  720
XGA  = 10 # 1024 *  768 
SVGA = 9  #  800 *  600
VGA  = 8  #  640 *  480
urlopen(f'http://192.168.100.11/control?var=framesize&val={HD}')

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
                print('Connecting ESP32-CAM from ',url)
                stream=urlopen(url)
                break
            except:
                print("Connect Failed.")
                tryagain=input('Try again?(Y/[N]): ').capitalize()
                if tryagain =='Y':
                    continue
                else:
                    os._exit(0)

        print('Connected ESP32 from ',url)

        frameID = 0 #fps count
        img = None

        if connect_server:
            #!/usr/bin/env python3
            # -*- coding: utf-8 -*-

            HOST = '192.168.100.7' #get_ip() #Server IP
            PORT = 7000

            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f'Connecting Server "{HOST}:{PORT}" ...')
            for i in range(10):
                try:
                    server.connect((HOST, PORT))
                    break
                except:
                    print(f'Server Connection Failed, Trying again...({i})')
                    if i == 9:
                        print("Server Connection Failed, leaving program...")
                        os._exit(0) #強制結束
            print('Server Connected, data streaming...')
        for _ in iter(int, 1): # infinite loop:
            data = read_stream()
            
            #print(len(outdata))
            server.send(data)

            # try:
            #     indata = server.recv(1024)
            #     print('recv: ' + indata.decode())
            # except:
            #     print('No answer from server')
            #     # # connection closed
            #     # server.close()
            #     # print('server closed connection.')
            #     # break

            # fps count
            # frameID += 1
            # fps_count(frameID)
    except KeyboardInterrupt:
        print("Application broke down by user")
