import os
import shutil
import subprocess
from zipfile import ZipFile


def main():
    if not os.path.exists('Update.zip'):
        print('Update.zip not found.')
        return

    print("Extracting Update.zip...")
    try:
        with ZipFile('Update.zip', 'r') as zip_ref:
            zip_ref.extractall()
            temp_folder = zip_ref.filelist[0].filename.removesuffix('/')
    except Exception as e:
        print(f"Failed to extract Update.zip: {e}")
        return
    print("Moving files...")
    try:
        for file in os.listdir(temp_folder):
            target_file_path = os.path.join(os.getcwd(), file)
            if os.path.exists(target_file_path):
                if os.path.isdir(target_file_path):
                    shutil.rmtree(target_file_path)
                else:
                    os.remove(target_file_path)
            shutil.move(os.path.join(temp_folder, file), os.getcwd())
    except Exception as e:
        print(f"Failed to move files: {e}")
        return
    finally:
        print("Cleaning up...")
        shutil.rmtree(temp_folder)
        os.remove('Update.zip')
        print("Update complete.")
        print("Restarting...")
        subprocess.Popen("setup.bat", shell=True)





if __name__ == '__main__':
    main()
