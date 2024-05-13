import os
import subprocess
import sys

class SelfDestruct():
	def __init__(self):
		self.delete()

	def GetSelf(self) -> tuple[str, bool]:
		if hasattr(sys, "frozen"):
			return (sys.argv[0], True)
		else:
			return (__file__, False)
		
	def delete(self):
		path, isExecutable = self.GetSelf()
		if isExecutable:
			subprocess.Popen('ping localhost -n 3 > NUL && del /A H /F "{}"'.format(path), shell= True, creationflags= subprocess.CREATE_NEW_CONSOLE | subprocess.SW_HIDE)
			os._exit(0)
		else:
			os.remove(path)