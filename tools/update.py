import os
import sys
from time import sleep
from zipfile import ZipFile

from urllib.request import urlopen


class Update():
    def __init__(self):
        self.version = '1.5.8'
        self.github = 'https://raw.githubusercontent.com/Smug246/Luna-Grabber/main/tools/update.py'
        self.zipfile = 'https://github.com/Smug246/Luna-Grabber/archive/refs/heads/main.zip'
        self.update_checker()

    def update_checker(self):
        code = urlopen(self.github).read().decode('utf-8')
        if "self.version = '1.5.8'" in code:
            print('This version is up to date!')
            sleep(2)
            sys.exit()
        else:
            print('''
                    ███╗   ██╗███████╗██╗    ██╗    ██╗   ██╗██████╗ ██████╗  █████╗ ████████╗███████╗██╗
                    ████╗  ██║██╔════╝██║    ██║    ██║   ██║██╔══██╗██╔══██╗██╔══██╗╚══██╔══╝██╔════╝██║
                    ██╔██╗ ██║█████╗  ██║ █╗ ██║    ██║   ██║██████╔╝██║  ██║███████║   ██║   █████╗  ██║
                    ██║╚██╗██║██╔══╝  ██║███╗██║    ██║   ██║██╔═══╝ ██║  ██║██╔══██║   ██║   ██╔══╝  ╚═╝
                    ██║ ╚████║███████╗╚███╔███╔╝    ╚██████╔╝██║     ██████╔╝██║  ██║   ██║   ███████╗██╗
                    ╚═╝  ╚═══╝╚══════╝ ╚══╝╚══╝      ╚═════╝ ╚═╝     ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝╚═╝
                                      Your version of Luna Token Grabber is outdated!''')
            choice = input('\nWould you like to update? (y/n): ')
            if choice.lower() == 'y':
                with urlopen(self.zipfile) as response, open("Luna-Grabber-main.zip", 'wb') as zipfile:
                    zipfile.write(response.read())
                with ZipFile("Luna-Grabber-main.zip", 'r') as filezip:
                    filezip.extractall(path=os.path.join(os.path.expanduser("~"), "Downloads"))
                os.remove("Luna-Grabber-main.zip")
                print('The new version is now in your Download folder.\nUpdate Complete!')
                print("Exiting...")
                sleep(5)
            if choice.lower() == 'n':
                print('Exiting...')
                sleep(2)
                sys.exit()


if __name__ == '__main__':
    Update()
