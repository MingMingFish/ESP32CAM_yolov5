# ESP32CAM_yolov5
 Run yolov5 by ESP32CAM from WAN

# Update Notes:
## Passed updates
- Data missing

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

# Notes:
## Environments
- You need to run this program in Anaconda, setup the environment for yolov5
    - yolov5 only run in Anaconda environments, so I can't help you with this.

## Missing YOLOv5 File?
- Downloaded yolov5 from:
    - https://github.com/ultralytics/yolov5

- Or change the code below:
    - `model = torch.hub.load(repo_or_dir='yolov5',model='yolov5x',source='local') # s/m/l/x`
    
    to
    - `model = torch.hub.load('ultralytics/yolov5', 'yolov5s') # source = 'github' # as default`

## Object Models
- You can change the model by editing the model name, the program will download the model automatically.
    - yolov5s / yolov5m / yolov5l / yolov5x / etc.

    - Or check on official websites:
        - https://pytorch.org/hub/ultralytics_yolov5/
    
