import os
import shutil
import requests
import zipfile

class UPX():
    def __init__(self, base_dir="."):
        self.version = "4.1.0"
        self.url = f"https://github.com/upx/upx/releases/download/v{self.version}/upx-{self.version}-win64.zip"
        self.base_dir = base_dir

        self.check()
        self.download()
        self.extract()
        self.cleanup()

    def check(self):
        upx_path = os.path.join(self.base_dir, "tools", "upx.exe")
        if os.path.exists(upx_path):
            os.remove(upx_path)

    def download(self):
        response = requests.get(self.url)
        with open(os.path.join(self.base_dir, "upx.zip"), "wb") as f:
            f.write(response.content)

    def extract(self):
        with zipfile.ZipFile(os.path.join(self.base_dir, "upx.zip")) as zip_file:
            zip_file.extractall(self.base_dir)
            shutil.move(os.path.join(self.base_dir, f"upx-{self.version}-win64", "upx.exe"), os.path.join(self.base_dir, "tools"))

    def cleanup(self):
        os.remove(os.path.join(self.base_dir, "upx.zip"))
        shutil.rmtree(os.path.join(self.base_dir, f"upx-{self.version}-win64"))

if __name__ == "__main__":
    upx = UPX(base_dir=os.path.dirname(os.path.abspath(__file__)))
