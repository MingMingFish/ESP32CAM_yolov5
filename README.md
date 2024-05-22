# ESP32CAM_yolov5
 Run yolov5 by ESP32CAM from WAN

# Update Notes:
## Passed updates
- *Data missing*

## 20220828
- Upload Files
- Update esp32_cam.py:
    - Optimize item name printing
    - Only print item which larger than 129600 (close to camera)
    - Only print item when result confidence >= 0.5
## 20220924
- Rename esp32_cam.py to yolo_esp32cam_recv.py
- Create client app code (ESP32CAM_send_no_display.py)
- Updates:
    - Now code will set up a server and recive connection data from client app
    - Change alert size to auto culculate by 1/4 of total volume
    - Took off all of codes about picture process in client app (opencv, PIL, etc.)
    - Made client app available on mobile device.
## 20221002
- Add playsound module to play audio files.
- Uploaded mp3 files of detect objects.
- Made program run with different threads for sending and receiving data.
- When run on Android, playsound module doesn't work, so switch to use sl4a for android app. (kept two version of programs)
- Still got a big bug to fix:
    - mediaPlay is not working:
    - When use parameter: play=True(which is default), the program stocked.
    - If not, the program keep running but no sounds was played.
## 20221002
- esp32 connection bug fix
## 20221123
- Added a simplified version for raspberry pi 
- Use pygame to play sounds

## 20221125
- Update requirements file 
- Update raspi version 
## 20221202
- Add flask to requests 
- Make it can be started by web request
## 20221208
- Issue solve - mkdir video automatically
- Set ESP32CAM a hostname, then find its IP by it.
- run.py - simply run this python code to start program with flask for waiting the request
- wsgi.py - Having selections for running on computer or raspi
## 20221210
- Issue solve - '.local' is requested on raspi when finding the IP by hostname
## 20221219
- Update README.md
- This project has frozen temporary. Contect me if you have any questions.

# Notes:
## Environments
- You need to run this program in Anaconda, setup the environment for yolov5
    - yolov5 only run in Anaconda environments, so I can't help you for that.
## Hardware / Firmware
- ESP32S (For the Cane, nothing about this python code so far)
- ESP32-CAM
    - Arduino Code download: https://github.com/MingMingFish/AIoT_Window_to_the_Soul
    - Android App: https://drive.google.com/file/d/1n-ipW-DTSQYuS5Hc4o0e074lagmyemJ5/view?usp=share_link
- Setup Docs (Zh-TW): https://docs.google.com/document/d/1-WC2XtERjPyeNyG127vGYmuaendjVqWl/edit?usp=share_link&ouid=107249627742763639384&rtpof=true&sd=true

## Missing YOLOv5 File?
- Downloaded yolov5 from:
    - https://github.com/ultralytics/yolov5

- Or change the code below:
    - `model = torch.hub.load(repo_or_dir='yolov5',model='yolov5x',source='local') # s/m/l/x`
    
    to
    - `model = torch.hub.load('ultralytics/yolov5', 'yolov5s') # source = 'github' # as default`

## Object Models
- You can change the model by editing the model name, the program will download the model automatically.
    - yolov5n / yolov5s / yolov5m / yolov5l / yolov5x / etc.

    - Or check on official websites:
        - https://pytorch.org/hub/ultralytics_yolov5/
    
