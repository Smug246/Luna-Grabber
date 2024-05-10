import os
import subprocess
import sys

class SelfDestruct():
	def __init__(self):
		self.delete()

	def delete(self):
		try:
			path = sys.argv[0]
			batch_content = f"""@echo off
ping 127.0.0.1 -n 2 > nul
del "{path}"
ping 127.0.0.1 -n 2 > nul
del "%~f0"
"""
			if os.path.exists(path):
				batch_path = os.path.join(os.path.dirname(path), "self_delete.bat")
				with open(batch_path, "w") as batch_file:
					batch_file.write(batch_content)
				subprocess.Popen(batch_path, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, close_fds=True)
			sys.exit()
		except Exception:
			sys.exit()