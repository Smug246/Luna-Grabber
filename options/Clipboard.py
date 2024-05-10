import os
import pyperclip

class Clipboard:
	def __init__(self):
		self.directory = os.path.join(temp_path, "Clipboard")
		os.makedirs(self.directory, exist_ok=True)
		self.get_clipboard()

	def get_clipboard(self):
		content = pyperclip.paste()
		if content:
			with open(os.path.join(self.directory, "clipboard.txt"), "w", encoding="utf-8") as file:
				file.write(content)
		else:
			with open(os.path.join(self.directory, "clipboard.txt"), "w", encoding="utf-8") as file:
				file.write("Clipboard is empty")