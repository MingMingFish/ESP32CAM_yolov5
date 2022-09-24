import os
from PIL import ImageFont, ImageDraw, Image
from urllib.request import urlopen
import cv2
import imutils
import time
import numpy as np

connect_server=True
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
    vcount = 0
    for path in os.listdir(dir):
        if os.path.isfile(os.path.join(dir, path)):
            vcount += 1
    return vcount

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
    
    while True:
        bts+=stream.read(CAMERA_BUFFER_SIZE)
        jpghead=bts.find(b'\xff\xd8')
        jpgend=bts.find(b'\xff\xd9')
        #print(f"jpghead: {jpghead}, jpgend: {jpgend}")
        img = None
        height,width = 0,0

        if jpghead>-1 and jpgend>-1:
            jpg=bts[jpghead:jpgend+2]
            bts=bts[jpgend+2:]
            #print('Found JPG')
            try:
                img=cv2.imdecode(np.frombuffer(jpg,dtype=np.uint8),cv2.IMREAD_UNCHANGED)    
                #v=cv.flip(img,0)
                #h=cv.flip(img,1)
                #p=cv2.flip(img,-1)    
                #frame=p
                height,width=img.shape[:2]
                img=cv2.resize(img,(record_width, record_height))
                print(img.shape)
            except:
                img = None
                print("img error")

            break
        # else:
        #     print('Finding JPG...')
        #     if jpghead==-1:
        #         print('jpghead not found')
        #     if jpgend==-1:
        #         print('jpgend not found')


    return img,(width,height)

bts=b''
if __name__ == "__main__":
    if(write_video is True):
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        out = cv2.VideoWriter(f'{outputdir}/record_{video_num}.avi',fourcc, 20.0, (record_width,record_height))
    #stream=object()
    while True:
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

    frameID = 0
    img = None

    if connect_server:
        #!/usr/bin/env python3
        # -*- coding: utf-8 -*-

        HOST = '192.168.100.7' #get_ip() #Server IP
        PORT = 7000
        
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            print(f'Connecting Server "{HOST}:{PORT}" ...')
            server.connect((HOST, PORT))
        except:
            print("Server Connection Failed, leaving program...")
            os._exit(0) #強制結束
    while True:
        img, (width, height) = read_stream()
        if img is not None:
            if(output_rotate is True):
                img = imutils.rotate(img, rotate)

            if connect_server:
                outdata=img
                outdata=np.array(cv2.imencode('.jpg',img)[1])
                
                #print(len(outdata))
                server.send(outdata)

                # try:
                #     indata = server.recv(1024)
                #     print('recv: ' + indata.decode())
                # except:
                #     print('No answer from server')
                #     # # connection closed
                #     # server.close()
                #     # print('server closed connection.')
                #     # break

            cv2.imshow("Camara", img)

            #跳出迴圈
            k=cv2.waitKey(1)
            if k & 0xFF==ord('q'):
                if(write_video is True):
                    out.release()
                if connect_server:
                    server.send('close'.encode())
                cv2.destroyAllWindows()
                break
                
            frameID += 1
            fps_count(frameID)

            if(write_video is True):
                out.write(img)
