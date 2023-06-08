import os
import subprocess
import sys
import re
import time
import random
import threading
import hashlib
import json
import requests
from urllib3.exceptions import InsecureRequestWarning
from http import cookiejar
from enum import Enum


requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)


class BlockCookies(cookiejar.CookiePolicy):
    return_ok = set_ok = domain_return_ok = path_return_ok = lambda self, *args, **kwargs: False
    netscape = True
    rfc2965 = hide_cookie2 = False


class Gorgon:
    def __init__(self, params: str, data: str, cookies: str, unix: int) -> None:
        self.unix = unix
        self.params = params
        self.data = data
        self.cookies = cookies

    def hash(self, data: str) -> str:
        try:
            _hash = hashlib.md5(data.encode()).hexdigest()
        except Exception:
            _hash = hashlib.md5(data).hexdigest()
        return _hash

    def get_base_string(self) -> str:
        base_str = self.hash(self.params)
        base_str = base_str + self.hash(self.data) if self.data else base_str + '0' * 32
        base_str = base_str + self.hash(self.cookies) if self.cookies else base_str + '0' * 32
        return base_str

    def get_value(self) -> dict[str, str]:
        base_str = self.get_base_string()
        return self.encrypt(base_str)

    def encrypt(self, data: str) -> dict[str, str]:
        unix = self.unix
        length = 20
        key = [
            223, 119, 185, 64, 185, 155, 132, 131, 209, 185, 203, 209, 247, 194, 185, 133, 195, 208, 251, 195
        ]
        param_list = []

        for i in range(0, 12, 4):
            temp = data[8 * i:8 * (i + 1)]
            for j in range(4):
                H = int(temp[j * 2:(j + 1) * 2], 16)
                param_list.append(H)

        param_list.extend([0, 6, 11, 28])
        H = int(hex(unix), 16)
        param_list.append((H & 4278190080) >> 24)
        param_list.append((H & 16711680) >> 16)
        param_list.append((H & 65280) >> 8)
        param_list.append((H & 255) >> 0)
        eor_result_list = []

        for (A, B) in zip(param_list, key):
            eor_result_list.append(A ^ B)

        for i in range(length):
            C = self.reverse(eor_result_list[i])
            D = eor_result_list[(i + 1) % length]
            E = C ^ D
            F = self.rbit_algorithm(E)
            H = (F ^ 4294967295 ^ length) & 255
            eor_result_list[i] = H

        result = ''
        for param in eor_result_list:
            result += self.hex_string(param)

        return {'X-Gorgon': '0404b0d30000' + result, 'X-Khronos': str(unix)}

    def rbit_algorithm(self, num):
        result = ''
        tmp_string = bin(num)[2:]
        while len(tmp_string) < 8:
            tmp_string = '0' + tmp_string

        for i in range(0, 8):
            result = result + tmp_string[7 - i]

        return int(result, 2)

    def hex_string(self, num):
        tmp_string = hex(num)[2:]
        if len(tmp_string) < 2:
            tmp_string = '0' + tmp_string
        return tmp_string

    def reverse(self, num):
        tmp_string = self.hex_string(num)
        return int(tmp_string[1:] + tmp_string[:1], 16)


class Colors(Enum):
    green_to_white = 1


class Colorate:
    @staticmethod
    def Horizontal(color: Colors, text: str) -> str:
        return text


def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    except subprocess.CalledProcessError:
        pass



    def get_proxy(config, proxies):
    if config['proxy']['use-proxy']:
        proxy = random.choice(proxies)
        proxy_format = f'{config["proxy"]["proxy-type"].lower()}://{proxy}'
        return {"http": proxy_format, "https": proxy_format}
    else:
        return {}


def send(did, iid, cdid, openudid, __aweme_id, proxies, config, _lock):
    global fails, reqs, success
    params = f"device_id={did}&iid={iid}&device_type=SM-G973N&app_name=musically_go&host_abi=armeabi-v7a&channel=googleplay&device_platform=android&version_code=160904&device_brand=samsung&os_version=9&aid=1340"
    payload = f"item_id={__aweme_id}&play_delta=1"
    sig = Gorgon(params=params, cookies=None, data=None, unix=int(time.time())).get_value()

    proxy = get_proxy(config, proxies)

    try:
        response = requests.post(
            url=f"https://api16-va.tiktokv.com/aweme/v1/aweme/stats/?{params}",
            data=payload,
            headers={
                'cookie': 'sessionid=90c38a59d8076ea0fbc01c8643efbe47',
                'x-gorgon': sig['X-Gorgon'],
                'x-khronos': sig['X-Khronos'],
                'user-agent': 'okhttp/3.10.0.1'
            },
            verify=False,
            proxies=proxy
        )
        with _lock:
            print(Colorate.Horizontal(Colors.green_to_white, f"+ - sent views {response.json()['log_pb']['impr_id']} {__aweme_id} {reqs}"))
            success += 1
    except Exception as e:
        with _lock:
            print(f"Error sending views: {e}")
            fails += 1



def rpsm_loop():
    global rps, reqs
    while True:
        initial = reqs
        time.sleep(1.5)
        rps = round((reqs - initial) / 1.5, 1)


def title_loop():
    global rps, rpm, success, fails, reqs

    if os.name == "nt":
        while True:
            os.system(f'title TikTok Viewbot by @Practicer45 ^| success: {success} fails: {fails} reqs: {reqs} rps: {rps} rpm: {rpm}')
            time.sleep(0.1)


if __name__ == "__main__":
    os.system("cls" if os.name == "nt" else "clear")
    os.system("title TikTok Viewbot by Practicer45 " if os.name == "nt" else "")
    txt = """\n\n╦  ╦╦╔═╗╦ ╦╔╗ ╔═╗╔╦╗\n╚╗╔╝║║╣ ║║║╠╩╗║ ║ ║ \n ╚╝ ╩╚═╝╚╩╝╚═╝╚═╝ ╩ \n"""

    try:
        link = str(input("\n\n            ? - Video Link > "))
        __aweme_id = str(
            re.findall(r"(\d{18,19})", link)[0]
            if len(re.findall(r"(\d{18,19})", link)) == 1
            else re.findall(
                r"(\d{18,19})",
                requests.head(link, allow_redirects=True, timeout=5).url
            )[0]
        )
    except:
        os.system("cls" if os.name == "nt" else "clear")
        input("x - Invalid link, try inputting video id only")
        sys.exit(0)

    os.system("cls" if os.name == "nt" else "clear")
    print("Loading devices...")
    devices = []
    with open('devices.txt', 'r') as f:
        devices = f.read().splitlines()
    print("Devices loaded successfully.")

    print("Loading config...")
    config = {}
    with open('config.json', 'r') as f:
        try:
            config = json.load(f)
        except Exception as e:
            print(f"Error loading config: {e}")
            sys.exit(1)
    print("Config loaded successfully.")

    print("Loading proxies...")
    proxies = []
    if config['proxy']['use-proxy']:
        with open('proxies.txt', 'r') as f:
            proxies = f.read().splitlines()
    print("Proxies loaded successfully.")

    print("Viewbot initialized successfully.")
    print("Starting viewbot...")
    _lock = threading.Lock()
    reqs = 0
    success = 0
    fails = 0
    rpm = 0
    rps = 0
    time_start = time.time()

    threading.Thread(target=rpsm_loop).start()
    threading.Thread(target=title_loop).start()

    while True:
        device = random.choice(devices)
        did, iid, cdid, openudid = device.split(" ")

        if config['proxy']['rotate-proxy']:
            proxy = random.choice(proxies) if config['proxy']['use-proxy'] else ""
            proxy_format = f'{config["proxy"]["proxy-type"].lower()}://{proxy}' if config['proxy']['use-proxy'] else ''

        t = threading.Thread(
            target=send,
            args=(did, iid, cdid, openudid, __aweme_id, proxies, config, _lock)
        )
        t.start()
        reqs += 1
        rpm = round(reqs / (time.time() - time_start) * 60, 1)
        time.sleep(0.01)
