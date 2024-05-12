import ctypes

def fakeerror():
	ctypes.windll.user32.MessageBoxW(None, 'Error code: 0x80070002\nAn internal error occurred while importing modules.', 'Fatal Error', 0)