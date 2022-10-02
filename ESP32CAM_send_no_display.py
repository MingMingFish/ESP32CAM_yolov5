from msilib.schema import Directory
import os
from urllib.request import urlopen
import time
import socket
from concurrent import futures  # threads module
#pip install playsound==1.2.2   ## 1.3.0 doesn't work properly
from playsound import playsound

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
url = 'http://192.168.100.8'
stream_url= f"{url}:81/stream"
CAMERA_BUFFER_SIZE=4096

#Server
HOST = '192.168.100.7' #get_ip() # The Server IP
PORT = 7000

# Set shape of video
UXGA = 13 # 1600 * 1200
SXGA = 12 # 1280 * 1024
HD   = 11 # 1280 *  720
XGA  = 10 # 1024 *  768 
SVGA = 9  #  800 *  600
VGA  = 8  #  640 *  480
urlopen(f'{url}/control?var=framesize&val={HD}')

#fps count
start = time.time()

def fps_count(num_frames):
    end = time.time()
    seconds = end - start
    fps  = num_frames / seconds;
    print("Estimated frames per second : {0}".format(fps))
    return fps

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

def get_result():
    string = ''
    for _ in iter(int, 1): # infinite loop:
        data = server_send.recv(1).decode()
        if data =='\n':
            break
        else:
            string += data
    return string

def play_audio():
    temp = []
    timer = time.time()
    for _ in iter(int, 1): # infinite loop:
        play = get_result()
        if play != 'None':
            print('Having:', temp)
            if not play in temp:
                temp.append(play)
                playsound(os.path.join('audio', play+'.mp3'))
                print(f'Detect: {play}')
            elif time.time() - timer >= 5:
                temp.remove(play)
                timer = time.time()
        elif play == 'None':
            print('None')
        else:
            print('Exception:', play)

def send_stream():
    for _ in iter(int, 1): # infinite loop:
            data = read_stream()
            server_recv.send(data)
            # fps count:
            # frameID += 1
            # fps_count(frameID)

bts=b''
if __name__ == "__main__":
    try:
        for _ in iter(int, 1): # infinite loop:
            try:
                print('Connecting ESP32-CAM from ',stream_url)
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

        # frameID = 0 #fps count
        img = None

        if connect_server:
            server_recv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_send = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            print(f'Connecting Server "{HOST}:{PORT}" ...')

            for i in range(10):
                try:
                    server_recv.connect((HOST, PORT))
                    server_send.connect((HOST, PORT+1))
                    break
                except:
                    print(f'Server Connection Failed, Trying again...({i})')
                    if i == 9:
                        print("Server Connection Failed, leaving program...")
                        os._exit(0) #強制結束
            print('Server Connected, data streaming...')
        
        future_list = []
        with futures.ThreadPoolExecutor() as executor: #max_workers=2
            future = executor.submit(send_stream)
            future_list.append(future)
            future = executor.submit(play_audio)
            future_list.append(future)
        threads = futures.as_completed(fs=future_list)
    except KeyboardInterrupt:
        server_recv.close()
        server_send.close()
        print("Application broke down by user")
