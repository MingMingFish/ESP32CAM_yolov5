from flask import Flask
import os
import GetIP

app = Flask(__name__)
print(GetIP.get_internal_ip())
@app.route("/", host=GetIP.get_internal_ip())
def run():
    os.system('python ESP32CAM_raspi.py')
    return 'end'