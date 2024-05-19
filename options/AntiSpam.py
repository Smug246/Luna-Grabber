import os
import time

class AntiSpam:
	def __init__(self):
		if self.check_time():
			os._exit(0)

	def check_time(self) -> bool:
		current_time = time.time()
		file_path = os.path.join(temp, "dd_setup.txt")
		try:
			if os.path.exists(file_path):
				file_modified_time = os.path.getmtime(file_path)
				if current_time - file_modified_time > 60:
					os.utime(file_path, (current_time, current_time))
					return False
				else:
					return True
			else:
				with open(file_path, "w") as f:
					f.write(str(current_time))
				return False
		except Exception:
			return False