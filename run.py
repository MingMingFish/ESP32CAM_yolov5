from os import system
import GetIP
ip = GetIP.get_internal_ip()
port = 5000

system(f'flask run --host={ip} --port={port}')
