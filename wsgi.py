from flask import Flask
import os
import GetIP

app = Flask(__name__)
print(GetIP.get_internal_ip())
@app.route("/", host=GetIP.get_internal_ip())
def run():
    os.system('python main.py') # you can just run this line if you are running on a computer
    # os.system('sh run_on_raspi.sh') # use this line instead when running on raspi
    return 'end'
