#pip install beautifulsoup4
#pip install html5lib
from bs4 import BeautifulSoup
import requests
import socket

def get_external_ip(url = 'https://www.whatismyip.com.tw'):
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7,ja-JP;q=0.6,ja;q=0.5",
        "cache-control": "max-age=0",
        "cookie": "_ga=GA1.3.1948899637.1651821665; _gid=GA1.3.171603135.1651821665",
        "sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
        "sec-ch-ua-mobile": '?0',
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36"
    }
    print(f'Waitting response from {url} ...')
    
    website = requests.get(url,headers=headers)
    soup = BeautifulSoup(website.text, 'html5lib')
    tags_span = soup.span
    ip = tags_span.get('data-ip')
    return ip

def get_internal_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]
    s.close()
    return ip