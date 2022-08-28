# ESP32CAM_yolov5
 Run yolov5 by ESP32CAM from WAN

# Update Notes:
## Passed updates
- Date missing

## 20220828
- Upload Files
- Update esp32_cam.py:
    - Optimize item name printing
    - Only print item which larger than 129600 (close to camera)
    - Only print item when result confidence >= 0.5

# Notes:
## Environments
- You need to run this program in Anaconda, setup the environment for yolov5
    - yolov5 only run in Anaconda environments, so I can't help you with this.

## lost YOLOv5 File?
- Downloaded yolov5 from:
    - https://github.com/ultralytics/yolov5

- Or change the code below:
    `model = torch.hub.load(repo_or_dir='yolov5',model='yolov5x',source='local') # s/m/l/x`
    to
    `model = torch.hub.load('ultralytics/yolov5', 'yolov5s') # source = 'github' # as default`

## Object Models
- You can change the model by editing the model name, the program will download the model automatically.
    - yolov5s
    - yolov5m
    - yolov5l
    - yolov5x
    - etc.

    - Or check on official websites:
        - https://pytorch.org/hub/ultralytics_yolov5/
    